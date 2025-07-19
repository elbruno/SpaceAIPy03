"""
Utility functions for console operations and terminal management.
"""
import os
import sys
from typing import Tuple


def clear_screen() -> None:
    """Clear console without flickering."""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS and Linux
        os.system('clear')


def set_cursor_position(x: int, y: int) -> None:
    """Move cursor to specific position using ANSI escape codes."""
    print(f"\033[{y};{x}H", end='', flush=True)


def hide_cursor() -> None:
    """Hide the cursor."""
    print("\033[?25l", end='', flush=True)


def show_cursor() -> None:
    """Show the cursor."""
    print("\033[?25h", end='', flush=True)


def get_terminal_dimensions() -> Tuple[int, int]:
    """Return width, height of console."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        # Fallback for environments where terminal size detection fails
        return 80, 24


def setup_console() -> None:
    """Set up console for optimal game display."""
    # Ensure UTF-8 encoding for Unicode characters
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    # Hide cursor for clean display
    hide_cursor()


def cleanup_console() -> None:
    """Clean up console settings before exit."""
    show_cursor()
    print("\033[0m", end='')  # Reset all formatting
