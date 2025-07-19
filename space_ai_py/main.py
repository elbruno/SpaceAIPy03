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


def get_speed_selection() -> int:
    """Get speed selection from user input."""
    try:
        choice = input().strip()
        if choice == '1':
            return 1
        elif choice == '2':
            return 2
        elif choice == '3':
            return 3
        else:
            return 1  # Default to slow
    except (KeyboardInterrupt, EOFError):
        return 1


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
        speed = get_speed_selection()
        
        # Clear console and start game
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create and run game
        game = GameManager(speed)
        game.run_game_loop()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cleanup_console()


if __name__ == "__main__":
    main()
