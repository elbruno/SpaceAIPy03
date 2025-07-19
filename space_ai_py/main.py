"""
Space.AI.PY() - A Python console Space Invaders game.
Main entry point for the game.
"""
import sys
import os
from colorama import init as colorama_init
from start_screen import StartScreen
from game_manager import GameManager
from utils import setup_console, cleanup_console


def get_speed_selection() -> tuple[int, int, int]:
    """Get speed selection from user input for game, player bullets, and enemy bullets."""
    try:
        choice = input().strip()
        if not choice:  # Empty input - use defaults
            return (1, 1, 1)
        
        # Parse comma-separated values
        parts = choice.split(',')
        if len(parts) == 1:
            # Single value - use for all three settings
            speed = int(parts[0]) if parts[0].isdigit() and parts[0] in ['1', '2', '3'] else 1
            return (speed, speed, speed)
        elif len(parts) == 3:
            # Three values - game, player bullets, enemy bullets
            game_speed = int(parts[0]) if parts[0].strip().isdigit() and parts[0].strip() in ['1', '2', '3'] else 1
            player_bullet_speed = int(parts[1]) if parts[1].strip().isdigit() and parts[1].strip() in ['1', '2', '3'] else 1
            enemy_bullet_speed = int(parts[2]) if parts[2].strip().isdigit() and parts[2].strip() in ['1', '2', '3'] else 1
            return (game_speed, player_bullet_speed, enemy_bullet_speed)
        else:
            # Invalid format - use defaults
            return (1, 1, 1)
    except (KeyboardInterrupt, EOFError, ValueError):
        return (1, 1, 1)


def main():
    """Main entry point for Space.AI.PY()."""
    try:
        # Initialize colorama for cross-platform colored output
        colorama_init(autoreset=True)
        
        # Set up console for UTF-8 encoding and optimal display
        setup_console()
        
        # Show start screen
        StartScreen.show()
        
        # Get speed selection from user
        game_speed, player_bullet_speed, enemy_bullet_speed = get_speed_selection()
        
        # Clear console and start game
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create and run game
        game = GameManager(game_speed, player_bullet_speed, enemy_bullet_speed)
        game.run_game_loop()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cleanup_console()


if __name__ == "__main__":
    main()
