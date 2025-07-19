"""
RenderState class for managing frame buffers and rendering state.
"""
from typing import List, Optional, Tuple
from colorama import Fore, Back


class RenderState:
    """Store and manage current frame state as 2D arrays."""
    
    def __init__(self, width: int, height: int):
        """Initialize render state with given dimensions."""
        self.width = width
        self.height = height
        
        # Initialize buffers
        self.character_buffer: List[List[str]] = [[' ' for _ in range(width)] for _ in range(height)]
        self.color_buffer: List[List[str]] = [[Fore.WHITE for _ in range(width)] for _ in range(height)]
        
        # Previous frame buffers for comparison
        self.prev_character_buffer: List[List[str]] = [[' ' for _ in range(width)] for _ in range(height)]
        self.prev_color_buffer: List[List[str]] = [[Fore.WHITE for _ in range(width)] for _ in range(height)]
    
    def set_character(self, x: int, y: int, char: str, color: str = Fore.WHITE) -> None:
        """Set character and color at specific position."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.character_buffer[y][x] = char
            self.color_buffer[y][x] = color
    
    def get_character(self, x: int, y: int) -> Tuple[str, str]:
        """Get character and color at specific position."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.character_buffer[y][x], self.color_buffer[y][x]
        return ' ', Fore.WHITE
    
    def clear_buffer(self) -> None:
        """Clear the current buffers."""
        for y in range(self.height):
            for x in range(self.width):
                self.character_buffer[y][x] = ' '
                self.color_buffer[y][x] = Fore.WHITE
    
    def get_changed_positions(self) -> List[Tuple[int, int]]:
        """Get list of positions that changed since last frame."""
        changed = []
        for y in range(self.height):
            for x in range(self.width):
                if (self.character_buffer[y][x] != self.prev_character_buffer[y][x] or
                    self.color_buffer[y][x] != self.prev_color_buffer[y][x]):
                    changed.append((x, y))
        return changed
    
    def update_previous_buffers(self) -> None:
        """Update previous frame buffers with current state."""
        for y in range(self.height):
            for x in range(self.width):
                self.prev_character_buffer[y][x] = self.character_buffer[y][x]
                self.prev_color_buffer[y][x] = self.color_buffer[y][x]
    
    def draw_box(self, left: int, top: int, right: int, bottom: int, color: str = Fore.WHITE) -> None:
        """Draw a box using Unicode box-drawing characters."""
        # Corners
        self.set_character(left, top, '┌', color)
        self.set_character(right, top, '┐', color)
        self.set_character(left, bottom, '└', color)
        self.set_character(right, bottom, '┘', color)
        
        # Horizontal edges
        for x in range(left + 1, right):
            self.set_character(x, top, '─', color)
            self.set_character(x, bottom, '─', color)
        
        # Vertical edges
        for y in range(top + 1, bottom):
            self.set_character(left, y, '│', color)
            self.set_character(right, y, '│', color)
    
    def draw_text(self, x: int, y: int, text: str, color: str = Fore.WHITE) -> None:
        """Draw text at specified position."""
        for i, char in enumerate(text):
            if x + i < self.width:
                self.set_character(x + i, y, char, color)
