# Sports Betting Tracker

A command-line application for tracking sports bets, calculating profits, and analyzing betting performance.

## Features

- Track individual sports bets with:
  - Sport type
  - Team name
  - Betting odds (American format: +150, -110)
  - Wager amount
- Record bet outcomes (win/loss)
- View comprehensive betting statistics:
  - Total bets placed
  - Win/loss record
  - Win rate percentage
  - Total amount wagered
  - Pending wagers
  - Completed wagers
  - Total profit/loss
  - Break-even analysis

## Requirements

- Python 3.11 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/din77/bets.git
cd bets
```

2. Run the program:
```bash
python main.py
```

## Usage

Choose from the following options:
- Enter a new bet (1)
- Update bet result (2)
- View statistics (3)
- Exit (4)

### Entering a Bet

When entering a bet, you'll need to provide:
- Sport name
- Team name
- Odds in American format (e.g., +150 for 3/2 odds, -110 for 10/11 odds)
- Amount wagered

### Viewing Statistics

The statistics view provides:
- Betting performance metrics
- Detailed financial summary
- Break-even analysis (if currently at a loss)

## Example

```
Betting Statistics:
Total bets placed: 5
Completed bets: 3 (2 wins, 1 loss)
Win rate: 66.7%

Financial Summary:
Total amount wagered: $500.00
Pending wagers: $200.00
Completed wagers: $300.00
Total profit/loss: -$50.00
Amount needed to break even: $50.00
```


