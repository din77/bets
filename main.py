#!/usr/bin/env python3

from datetime import datetime
from typing import List, Optional
import sys

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

    def set_result(self, won: bool):
        self.result = won

    def get_profit(self) -> float:
        if self.result is None:
            return 0
        if self.result:
            return self.potential_win
        return -self.amount

class BettingTracker:
    def __init__(self):
        self.bets: List[Bet] = []

    def add_bet(self, bet: Bet):
        self.bets.append(bet)

    def get_win_rate(self) -> float:
        completed_bets = [bet for bet in self.bets if bet.result is not None]
        if not completed_bets:
            return 0.0
        wins = sum(1 for bet in completed_bets if bet.result)
        return (wins / len(completed_bets)) * 100

    def get_total_wagered(self) -> float:
        return sum(bet.amount for bet in self.bets)

    def get_total_completed_wagers(self) -> float:
        return sum(bet.amount for bet in self.bets if bet.result is not None)

    def get_pending_wagers(self) -> float:
        return sum(bet.amount for bet in self.bets if bet.result is None)

    def get_total_profit(self) -> float:
        return sum(bet.get_profit() for bet in self.bets)

    def get_completed_bets_count(self) -> tuple[int, int]:
        completed = [bet for bet in self.bets if bet.result is not None]
        wins = sum(1 for bet in completed if bet.result)
        return wins, len(completed)

    def get_break_even_amount(self) -> float:
        total_profit = self.get_total_profit()
        if total_profit >= 0:
            return 0
        return abs(total_profit)

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

def main():
    tracker = BettingTracker()
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
            tracker.add_bet(bet)
            print(f"\nBet recorded! Potential win: ${bet.potential_win:.2f}")
            
        elif choice == '2':
            if not tracker.bets:
                print("\nNo bets to update!")
                continue
                
            print("\nPending bets:")
            pending_bets = [bet for bet in tracker.bets if bet.result is None]
            if not pending_bets:
                print("No pending bets to update!")
                continue
                
            for i, bet in enumerate(pending_bets, 1):
                print(f"{i}. {bet.sport} - {bet.team} (${bet.amount:.2f} @ {bet.odds:+})")
            
            bet_idx = int(input("\nEnter bet number to update: ")) - 1
            if 0 <= bet_idx < len(pending_bets):
                result = get_yes_no_input("Did the bet win? (y/n): ")
                pending_bets[bet_idx].set_result(result)
                print("Bet updated successfully!")
            else:
                print("Invalid bet number!")
                
        elif choice == '3':
            if not tracker.bets:
                print("\nNo bets recorded yet!")
                continue
                
            wins, completed = tracker.get_completed_bets_count()
            print("\nBetting Statistics:")
            print(f"Total bets placed: {len(tracker.bets)}")
            print(f"Completed bets: {completed} ({wins} wins, {completed - wins} losses)")
            print(f"Win rate: {tracker.get_win_rate():.1f}%")
            print("\nFinancial Summary:")
            print(f"Total amount wagered: ${tracker.get_total_wagered():.2f}")
            print(f"Pending wagers: ${tracker.get_pending_wagers():.2f}")
            print(f"Completed wagers: ${tracker.get_total_completed_wagers():.2f}")
            print(f"Total profit/loss: ${tracker.get_total_profit():.2f}")
            if tracker.get_break_even_amount() > 0:
                print(f"Amount needed to break even: ${tracker.get_break_even_amount():.2f}")
            
        elif choice == '4':
            print("\nThank you for using Sports Betting Tracker!")
            sys.exit(0)
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 