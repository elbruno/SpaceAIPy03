"""
StartScreen class for displaying the game's start screen.
"""
import os
from colorama import Fore, Style


class StartScreen:
    """Display the start screen with game instructions and speed selection."""
    
    @staticmethod
    def show() -> None:
        """Display the start screen layout."""
        try:
            width, height = os.get_terminal_size().columns, os.get_terminal_size().lines
        except OSError:
            width, height = 80, 24
        
        # Clear screen
        print("\033[2J\033[H", end='')
        
        # Calculate center position for title
        title = "Space.AI.PY()"
        subtitle = "Built with Python + AI for galactic defense"
        title_x = (width - len(title)) // 2
        subtitle_x = (width - len(subtitle)) // 2
        
        # Display title and subtitle
        print(f"\033[3;{title_x}H{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        print(f"\033[4;{subtitle_x}H{Fore.WHITE}{subtitle}{Style.RESET_ALL}")
        
        # Instructions (left-aligned)
        instructions_start_y = 7
        instructions = [
            "",
            "How to Play:",
            "←   Move Left",
            "→   Move Right",
            "SPACE   Shoot",
            "S   Take Screenshot",
            "Q   Quit",
            "",
            "Select Game Speed:",
            "[1] Slow (default)",
            "[2] Medium",
            "[3] Fast",
            "Press ENTER for default"
        ]
        
        # Display instructions
        for i, line in enumerate(instructions):
            y_pos = instructions_start_y + i
            if y_pos < height - 2:  # Leave some space at bottom
                if line.startswith("How to Play:") or line.startswith("Select Game Speed:"):
                    print(f"\033[{y_pos};5H{Fore.YELLOW}{Style.BRIGHT}{line}{Style.RESET_ALL}")
                elif line.startswith("["):
                    print(f"\033[{y_pos};5H{Fore.GREEN}{line}{Style.RESET_ALL}")
                else:
                    print(f"\033[{y_pos};5H{Fore.WHITE}{line}{Style.RESET_ALL}")
        
        # Position cursor for input
        input_y = instructions_start_y + len(instructions) + 2
        print(f"\033[{input_y};5H{Fore.CYAN}Your choice: {Style.RESET_ALL}", end='', flush=True)
