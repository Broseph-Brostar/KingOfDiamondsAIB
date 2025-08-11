#!/usr/bin/env python3
"""
Demo script for King of Diamonds Game
Shows how the game mechanics work with simulated players
"""

from king_of_diamonds import KingOfDiamondsGame, Player
import random

def simulate_game():
    """Simulate a game with AI players"""
    print("*** KING OF DIAMONDS DEMO ***")
    print("Simulating a game with AI players")
    print("=" * 50)
    
    # Create game and add players
    game = KingOfDiamondsGame()
    player_names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    
    for name in player_names:
        game.add_player(name)
    
    print(f"\n>> Game starting with {len(game.players)} players!")
    
    # Simulate rounds
    round_count = 0
    while not game.game_over and round_count < 20:  # Safety limit
        alive_players = game.get_alive_players()
        if len(alive_players) <= 1:
            break
            
        print(f"\n{'='*20} ROUND {game.round_number} {'='*20}")
        
        # Show current status
        print("\n>> Current Status:")
        for player in alive_players:
            print(f"  {player}")
        
        # Display rules for first round or when new rules are introduced
        if game.round_number == 1 or any(p.points != 10 for p in game.players if not p.is_alive):
            game.display_rules()
        
        # Simulate player choices with some strategy
        choices = {}
        print(f"\n>> ROUND {game.round_number} - Number Selection")
        print("-" * 40)
        
        # Special demonstration when Rule 3 is active and only 2 players left
        if game.eliminated_count >= 3 and len(alive_players) == 2:
            print("\n*** DEMONSTRATING RULE 3 ***")
            print("With 3+ eliminated and 2 players left, let's show both scenarios:")
            
            # First, demonstrate the 0-100 special rule
            print("\n--- Scenario A: 0-100 Special Rule ---")
            player1, player2 = alive_players[0], alive_players[1]
            
            # Force one to choose 0 and other to choose 100
            player1.choose_number(0)
            player2.choose_number(100)
            choices[0] = [player1]
            choices[100] = [player2]
            
            print(f"{player1.name} chooses: 0 (strategic)")
            print(f"{player2.name} chooses: 100 (counter-strategy)")
            
        else:
            # Normal AI strategy for other rounds
            for player in alive_players:
                # Simple AI strategy: random with some bias toward middle values
                if game.eliminated_count >= 3 and len(alive_players) > 2 and random.random() < 0.1:
                    # Small chance to try the 0-100 special rule
                    choice = random.choice([0, 100])
                else:
                    # Normal strategy - bias toward 30-60 range (since target is average * 0.8)
                    choice = random.randint(20, 80)
                
                player.choose_number(choice)
                if choice not in choices:
                    choices[choice] = []
                choices[choice].append(player)
                print(f"{player.name} chooses: {choice}")
        
        # Calculate target
        target = game.calculate_target(choices)
        print(f"\n>> Target number: {target:.2f}")
        
        # Show all choices
        print("\n>> All choices:")
        for number in sorted(choices.keys()):
            players_str = ", ".join([p.name for p in choices[number]])
            print(f"  {number}: {players_str}")
        
        # Apply rules and find winner
        winner, exact_match = game.apply_special_rules(choices, target)
        
        if winner:
            print(f"\n*** {winner.name} wins this round! ***")
            
            # Apply penalties to losers
            penalty = 2 if (exact_match and game.eliminated_count >= 2) else 1
            penalty_msg = f"{penalty} point{'s' if penalty > 1 else ''}"
            
            for player in alive_players:
                if player != winner:
                    player.lose_points(penalty)
                    print(f"   {player.name} loses {penalty_msg}")
        
        # Update elimination count
        current_alive = len(game.get_alive_players())
        initial_alive = len(alive_players)
        if current_alive < initial_alive:
            game.eliminated_count = len(game.players) - current_alive
        
        game.round_number += 1
        round_count += 1
        
        # Check win condition
        final_alive = game.get_alive_players()
        if len(final_alive) <= 1:
            game.game_over = True
            if final_alive:
                game.winner = final_alive[0]
        
        print("\n" + "-" * 50)
        
        # Add extra demonstration for Rule 3 when exactly 2 players remain
        if game.eliminated_count >= 3 and len(game.get_alive_players()) == 2 and not game.game_over:
            print("\n*** BONUS DEMONSTRATION ***")
            print("Let's also see what happens in a normal round with Rule 3 active:")
            input("Press Enter to see normal round with Rule 3...")
            
            # Simulate one more normal round
            alive_players = game.get_alive_players()
            if len(alive_players) == 2:
                print(f"\n{'='*20} BONUS ROUND {game.round_number} {'='*20}")
                print("\n>> Current Status:")
                for player in alive_players:
                    print(f"  {player}")
                
                game.display_rules()
                
                # Normal choices this time
                choices = {}
                print(f"\n>> ROUND {game.round_number} - Number Selection (Normal Strategy)")
                print("-" * 40)
                
                for player in alive_players:
                    # Normal strategic choices
                    choice = random.randint(30, 70)
                    player.choose_number(choice)
                    if choice not in choices:
                        choices[choice] = []
                    choices[choice].append(player)
                    print(f"{player.name} chooses: {choice} (normal strategy)")
                
                # Calculate and show results
                target = game.calculate_target(choices)
                print(f"\n>> Target number: {target:.2f}")
                
                print("\n>> All choices:")
                for number in sorted(choices.keys()):
                    players_str = ", ".join([p.name for p in choices[number]])
                    print(f"  {number}: {players_str}")
                
                winner, exact_match = game.apply_special_rules(choices, target)
                
                if winner:
                    print(f"\n*** {winner.name} wins this bonus round! ***")
                    penalty = 2 if (exact_match and game.eliminated_count >= 2) else 1
                    penalty_msg = f"{penalty} point{'s' if penalty > 1 else ''}"
                    
                    for player in alive_players:
                        if player != winner:
                            player.lose_points(penalty)
                            print(f"   {player.name} loses {penalty_msg}")
                
                # Update game state
                current_alive = len(game.get_alive_players())
                if current_alive < len(alive_players):
                    game.eliminated_count = len(game.players) - current_alive
                
                game.round_number += 1
                
                final_alive = game.get_alive_players()
                if len(final_alive) <= 1:
                    game.game_over = True
                    if final_alive:
                        game.winner = final_alive[0]
        
        if not game.game_over:
            input("Press Enter to continue to next round...")
    
    # Game end
    print("\n" + "="*50)
    if game.winner:
        print(f"*** GAME CLEAR! {game.winner.name} is the winner! ***")
    else:
        print("XX All players eliminated! No winner!")
    print("="*50)

if __name__ == "__main__":
    simulate_game()
