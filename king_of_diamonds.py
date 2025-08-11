#!/usr/bin/env python3
"""
King of Diamonds Game - Alice in Borderland
A strategic number guessing game with evolving rules.
"""

import random
import time
from typing import List, Dict, Tuple, Optional

class Player:
    def __init__(self, name: str):
        self.name = name
        self.points = 10  # Start with 10 points instead of 0
        self.is_alive = True
        self.current_choice = None
    
    def choose_number(self, number: int):
        """Player chooses a number between 0 and 100"""
        if not (0 <= number <= 100):
            raise ValueError("Number must be between 0 and 100")
        self.current_choice = number
    
    def lose_points(self, points: int):
        """Deduct points from player"""
        self.points -= points
        if self.points <= 0:
            self.is_alive = False
            print(f"XX {self.name} has been eliminated! (GAME OVER)")
    
    def __str__(self):
        status = "ALIVE" if self.is_alive else "DEAD"
        return f"{self.name}: {self.points} points ({status})"

class KingOfDiamondsGame:
    def __init__(self):
        self.players: List[Player] = []
        self.round_number = 1
        self.eliminated_count = 0
        self.game_over = False
        self.winner = None
        
    def add_player(self, name: str) -> bool:
        """Add a player to the game (max 10 players)"""
        if len(self.players) >= 10:
            print("ERROR: Maximum 10 players allowed!")
            return False
        
        if any(p.name == name for p in self.players):
            print(f"ERROR: Player name '{name}' already exists!")
            return False
            
        self.players.append(Player(name))
        print(f"OK: {name} joined the game!")
        return True
    
    def display_rules(self):
        """Display current game rules based on elimination count"""
        print("\n" + "="*60)
        print("*** KING OF DIAMONDS - CURRENT RULES ***")
        print("="*60)
        print(">> Base Rules:")
        print("  * Choose a number between 0 and 100")
        print("  * Average of all numbers x 0.8 = target")
        print("  * Closest to target wins, others lose 1 point")
        print("  * Reach 0 points = GAME OVER (eliminated)")
        print("  * Last player standing = GAME CLEAR")
        
        if self.eliminated_count >= 1:
            print("\n!! RULE 1 (1+ eliminated):")
            print("  * Duplicate numbers are INVALID")
            print("  * Players with duplicate numbers lose 1 point")
            
        if self.eliminated_count >= 2:
            print("\n!! RULE 2 (2+ eliminated):")
            print("  * Exact correct guess makes others lose 2 points instead of 1")
            
        if self.eliminated_count >= 3:
            print("\n!! RULE 3 (3+ eliminated):")
            print("  * If one player chooses 0, another can win by choosing 100")
        
        print("="*60)
    
    def get_alive_players(self) -> List[Player]:
        """Get list of players still alive"""
        return [p for p in self.players if p.is_alive]
    
    def collect_choices(self) -> Dict[int, List[Player]]:
        """Collect number choices from all alive players"""
        alive_players = self.get_alive_players()
        choices = {}
        
        print(f"\n>> ROUND {self.round_number} - Number Selection")
        print("-" * 40)
        
        for player in alive_players:
            while True:
                try:
                    choice = int(input(f"{player.name} ({player.points} pts), choose 0-100: "))
                    if 0 <= choice <= 100:
                        player.choose_number(choice)
                        if choice not in choices:
                            choices[choice] = []
                        choices[choice].append(player)
                        break
                    else:
                        print("ERROR: Number must be between 0 and 100!")
                except ValueError:
                    print("ERROR: Please enter a valid number!")
        
        return choices
    
    def calculate_target(self, choices: Dict[int, List[Player]]) -> float:
        """Calculate target number (average × 0.8)"""
        all_numbers = []
        for number, players in choices.items():
            all_numbers.extend([number] * len(players))
        
        if not all_numbers:
            return 0.0
            
        average = sum(all_numbers) / len(all_numbers)
        target = average * 0.8
        return target
    
    def apply_special_rules(self, choices: Dict[int, List[Player]], target: float) -> Tuple[Optional[Player], bool]:
        """Apply special rules and return winner if any, and if exact match occurred"""
        alive_players = self.get_alive_players()
        exact_match = False
        
        # Rule 1: Duplicate numbers are invalid (1+ eliminated)
        if self.eliminated_count >= 1:
            for number, players in choices.items():
                if len(players) > 1:
                    print(f"WARNING: Number {number} chosen by multiple players - INVALID!")
                    for player in players:
                        player.lose_points(1)
                        print(f"   {player.name} loses 1 point for duplicate choice")
        
        # Rule 3: Special 0-100 rule (3+ eliminated)
        if self.eliminated_count >= 3:
            zero_players = choices.get(0, [])
            hundred_players = choices.get(100, [])
            
            if len(zero_players) == 1 and len(hundred_players) == 1:
                # If one chooses 0 and another chooses 100, the 100 player wins
                winner = hundred_players[0]
                print(f">> Special Rule 3 activated! {winner.name} wins by choosing 100 while someone chose 0!")
                return winner, False
        
        # Find valid choices (not duplicates if rule 1 is active)
        valid_choices = {}
        for number, players in choices.items():
            if self.eliminated_count >= 1 and len(players) > 1:
                continue  # Skip duplicates
            valid_choices[number] = players
        
        if not valid_choices:
            print("ERROR: No valid choices this round!")
            return None, False
        
        # Find closest to target
        closest_distance = float('inf')
        winners = []
        
        for number, players in valid_choices.items():
            distance = abs(number - target)
            if distance < closest_distance:
                closest_distance = distance
                winners = players
            elif distance == closest_distance:
                winners.extend(players)
        
        # Check for exact match
        if closest_distance == 0:
            exact_match = True
            print(f">> EXACT MATCH! Target was {target:.2f}")
        
        # If multiple winners, pick randomly (shouldn't happen with rule 1)
        if len(winners) > 1:
            winner = random.choice(winners)
        else:
            winner = winners[0] if winners else None
            
        return winner, exact_match
    
    def play_round(self):
        """Play a single round"""
        alive_players = self.get_alive_players()
        
        if len(alive_players) <= 1:
            self.game_over = True
            if alive_players:
                self.winner = alive_players[0]
            return
        
        print(f"\n{'='*20} ROUND {self.round_number} {'='*20}")
        
        # Show current status
        print("\n>> Current Status:")
        for player in alive_players:
            print(f"  {player}")
        
        # Display rules (especially important for new rules)
        if self.round_number == 1 or any(p.points != 10 for p in self.players if not p.is_alive):
            self.display_rules()
            if self.round_number == 1 or self.eliminated_count > len([p for p in self.players if not p.is_alive]):
                print("\n>> 5 minutes to study the rules...")
                time.sleep(2)  # Shortened for demo purposes
        
        # Collect choices
        choices = self.collect_choices()
        
        # Calculate target
        target = self.calculate_target(choices)
        print(f"\n>> Target number: {target:.2f}")
        
        # Show all choices
        print("\n>> All choices:")
        for number in sorted(choices.keys()):
            players_str = ", ".join([p.name for p in choices[number]])
            print(f"  {number}: {players_str}")
        
        # Apply rules and find winner
        winner, exact_match = self.apply_special_rules(choices, target)
        
        if winner:
            print(f"\n*** {winner.name} wins this round! ***")
            
            # Apply penalties to losers
            penalty = 2 if (exact_match and self.eliminated_count >= 2) else 1
            penalty_msg = f"{penalty} point{'s' if penalty > 1 else ''}"
            
            for player in alive_players:
                if player != winner:
                    player.lose_points(penalty)
                    print(f"   {player.name} loses {penalty_msg}")
        
        # Update elimination count
        current_alive = len(self.get_alive_players())
        initial_alive = len(alive_players)
        if current_alive < initial_alive:
            self.eliminated_count = len(self.players) - current_alive
        
        self.round_number += 1
        
        # Check win condition
        final_alive = self.get_alive_players()
        if len(final_alive) <= 1:
            self.game_over = True
            if final_alive:
                self.winner = final_alive[0]
    
    def start_game(self):
        """Start the game"""
        print("*** Welcome to King of Diamonds! ***")
        print("Based on Alice in Borderland")
        print("-" * 40)
        
        # Add players
        while len(self.players) < 10:
            name = input(f"Enter player {len(self.players) + 1} name (or 'start' to begin): ").strip()
            if name.lower() == 'start':
                if len(self.players) < 2:
                    print("ERROR: Need at least 2 players!")
                    continue
                break
            if name:
                self.add_player(name)
        
        if len(self.players) < 2:
            print("ERROR: Not enough players to start!")
            return
        
        print(f"\n>> Game starting with {len(self.players)} players!")
        
        # Game loop
        while not self.game_over:
            self.play_round()
            
            if not self.game_over:
                input("\nPress Enter to continue to next round...")
        
        # Game end
        print("\n" + "="*50)
        if self.winner:
            print(f"*** GAME CLEAR! {self.winner.name} is the winner! ***")
        else:
            print("XX All players eliminated! No winner!")
        print("="*50)

def main():
    """Main function to run the game"""
    game = KingOfDiamondsGame()
    game.start_game()

if __name__ == "__main__":
    main()
