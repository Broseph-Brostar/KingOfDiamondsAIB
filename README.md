# King of Diamonds Game 🃏

A Python implementation of the King of Diamonds game from Alice in Borderland, featuring strategic number guessing with evolving rules.

## Game Overview

Players compete in a psychological strategy game where they must guess numbers closest to a calculated target while navigating increasingly complex rules as players are eliminated.

## Rules

### Base Rules
- **Players**: 2-10 players can join
- **Starting Points**: Each player starts with 10 points
- **Number Selection**: Choose a number between 0 and 100
- **Target Calculation**: Average of all chosen numbers × 0.8
- **Winning**: Player closest to the target wins the round
- **Losing**: All other players lose 1 point
- **Elimination**: Reach 0 points = GAME OVER
- **Victory**: Last player standing = GAME CLEAR

### Evolving Rules

As players are eliminated, new rules are introduced:

#### Rule 1 (1+ players eliminated)
- **Duplicate Penalty**: If multiple players choose the same number, that number becomes invalid
- **Consequence**: All players who chose the duplicate number lose 1 point

#### Rule 2 (2+ players eliminated)  
- **Exact Match Bonus**: If a player guesses the exact target number
- **Consequence**: Other players lose 2 points instead of 1

#### Rule 3 (3+ players eliminated)
- **Special 0-100 Rule**: If one player chooses 0 and another chooses 100
- **Consequence**: The player who chose 100 automatically wins the round

## How to Play

1. **Setup**: Run the game and add 2-10 players
2. **Each Round**:
   - View current rules and player status
   - Each player secretly chooses a number (0-100)
   - Target is calculated and revealed
   - Winner is determined based on current rules
   - Points are deducted from losers
3. **Game End**: Continue until only one player remains

## Strategy Tips

- **Early Game**: Focus on predicting the average behavior
- **Mid Game**: Watch for duplicate number patterns
- **Late Game**: Consider the special rules and psychological warfare
- **Advanced**: Use the 0.8 multiplier to your advantage - the target will always be lower than the average

## Installation & Running

```bash
# Navigate to the game directory
king_of_diamonds

# Run the game
python king_of_diamonds.py
```

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Example Gameplay

```
🃏 Welcome to King of Diamonds! 🃏
Enter player 1 name: Alice
✅ Alice joined the game!
Enter player 2 name: Bob
✅ Bob joined the game!
Enter player 3 name: start

🎮 Game starting with 2 players!

==================== ROUND 1 ====================

📊 Current Status:
  Alice: 10 points (ALIVE)
  Bob: 10 points (ALIVE)

🎯 ROUND 1 - Number Selection
Alice (10 pts), choose 0-100: 50
Bob (10 pts), choose 0-100: 60

🎯 Target number: 44.00

📋 All choices:
  50: Alice
  60: Bob

🏆 Alice wins this round!
   Bob loses 1 point
```

## Features

- **Interactive CLI**: Easy-to-use command line interface
- **Rule Visualization**: Clear display of current active rules
- **Real-time Status**: Track player points and elimination status
- **Strategic Depth**: Multiple layers of psychological gameplay
- **Faithful Adaptation**: Based on the original Alice in Borderland rules

## Game Theory

This game combines elements of:
- **Game Theory**: Nash equilibrium considerations
- **Psychology**: Reading opponents and bluffing
- **Mathematics**: Statistical analysis of number distributions
- **Risk Management**: Point conservation vs. aggressive play

Enjoy the psychological thriller of King of Diamonds! 🃏
