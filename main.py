#!/usr/bin/env python3

from datetime import datetime
import sqlite3
from typing import List, Optional
import sys
import os

class Database:
    def __init__(self):
        self.db_path = "bets.db"
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sport TEXT NOT NULL,
                    team TEXT NOT NULL,
                    odds REAL NOT NULL,
                    amount REAL NOT NULL,
                    potential_win REAL NOT NULL,
                    result INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_bet(self, bet: 'Bet') -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bets (sport, team, odds, amount, potential_win, date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (bet.sport, bet.team, bet.odds, bet.amount, bet.potential_win, bet.date))
            conn.commit()
            return cursor.lastrowid

    def update_bet_result(self, bet_id: int, result: bool):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bets
                SET result = ?
                WHERE id = ?
            ''', (1 if result else 0, bet_id))
            conn.commit()

    def get_pending_bets(self) -> List[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, sport, team, odds, amount, potential_win
                FROM bets
                WHERE result IS NULL
                ORDER BY date DESC
            ''')
            return cursor.fetchall()

    def get_statistics(self) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total bets
            cursor.execute('SELECT COUNT(*) FROM bets')
            total_bets = cursor.fetchone()[0]
            
            # Completed bets
            cursor.execute('SELECT COUNT(*), SUM(CASE WHEN result = 1 THEN 1 ELSE 0 END) FROM bets WHERE result IS NOT NULL')
            completed_row = cursor.fetchone()
            completed_bets = completed_row[0] or 0
            wins = completed_row[1] or 0
            
            # Financial calculations
            cursor.execute('''
                SELECT 
                    SUM(amount) as total_wagered,
                    SUM(CASE WHEN result IS NULL THEN amount ELSE 0 END) as pending_wagers,
                    SUM(CASE WHEN result IS NOT NULL THEN amount ELSE 0 END) as completed_wagers,
                    SUM(CASE 
                        WHEN result = 1 THEN potential_win 
                        WHEN result = 0 THEN -amount 
                        ELSE 0 
                    END) as total_profit
                FROM bets
            ''')
            financial = cursor.fetchone()
            
            return {
                'total_bets': total_bets,
                'completed_bets': completed_bets,
                'wins': wins,
                'total_wagered': financial[0] or 0,
                'pending_wagers': financial[1] or 0,
                'completed_wagers': financial[2] or 0,
                'total_profit': financial[3] or 0
            }

class Bet:
    def __init__(self, sport: str, team: str, odds: float, amount: float):
        self.sport = sport
        self.team = team
        self.odds = odds
        self.amount = amount
        self.result: Optional[bool] = None
        self.potential_win = self._calculate_potential_win()
        self.date = datetime.now()

    def _calculate_potential_win(self) -> float:
        if self.odds >= 0:
            return (self.odds / 100) * self.amount
        else:
            return (100 / abs(self.odds)) * self.amount

def get_valid_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def get_yes_no_input(prompt: str) -> bool:
    while True:
        response = input(prompt).lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'.")

def display_statistics(stats: dict):
    print("\nBetting Statistics:")
    print(f"Total bets placed: {stats['total_bets']}")
    if stats['completed_bets'] > 0:
        win_rate = (stats['wins'] / stats['completed_bets']) * 100
        print(f"Completed bets: {stats['completed_bets']} ({stats['wins']} wins, {stats['completed_bets'] - stats['wins']} losses)")
        print(f"Win rate: {win_rate:.1f}%")
    
    print("\nFinancial Summary:")
    print(f"Total amount wagered: ${stats['total_wagered']:.2f}")
    print(f"Pending wagers: ${stats['pending_wagers']:.2f}")
    print(f"Completed wagers: ${stats['completed_wagers']:.2f}")
    print(f"Total profit/loss: ${stats['total_profit']:.2f}")
    
    if stats['total_profit'] < 0:
        print(f"Amount needed to break even: ${abs(stats['total_profit']):.2f}")

def main():
    db = Database()
    print("Welcome to the Sports Betting Tracker!")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Enter a new bet")
        print("2. Update bet result")
        print("3. View statistics")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            print("\nEnter bet details:")
            sport = input("Sport: ")
            team = input("Team: ")
            odds = float(input("Odds (use +150 or -110 format): "))
            amount = get_valid_float("Amount wagered: $")
            
            bet = Bet(sport, team, odds, amount)
            bet_id = db.add_bet(bet)
            print(f"\nBet recorded! Potential win: ${bet.potential_win:.2f}")
            
        elif choice == '2':
            pending_bets = db.get_pending_bets()
            if not pending_bets:
                print("\nNo pending bets to update!")
                continue
                
            print("\nPending bets:")
            for i, bet in enumerate(pending_bets, 1):
                bet_id, sport, team, odds, amount, potential_win = bet
                print(f"{i}. {sport} - {team} (${amount:.2f} @ {odds:+})")
            
            bet_idx = int(input("\nEnter bet number to update: ")) - 1
            if 0 <= bet_idx < len(pending_bets):
                result = get_yes_no_input("Did the bet win? (y/n): ")
                db.update_bet_result(pending_bets[bet_idx][0], result)
                print("Bet updated successfully!")
            else:
                print("Invalid bet number!")
                
        elif choice == '3':
            stats = db.get_statistics()
            if stats['total_bets'] == 0:
                print("\nNo bets recorded yet!")
                continue
            
            display_statistics(stats)
            
        elif choice == '4':
            print("\nThank you for using Sports Betting Tracker!")
            sys.exit(0)
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 