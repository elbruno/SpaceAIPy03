"""
Bullet class for managing player and enemy projectiles.
"""
from typing import Tuple
from colorama import Fore


class Bullet:
    """Manages bullet movement, rendering, and collision detection."""
    
    def __init__(self, x: int, y: int, velocity: int, is_player_bullet: bool = True):
        """Initialize bullet with position and movement properties."""
        self.x = x
        self.y = y
        self.velocity = velocity  # Positive for up (player), negative for down (enemy)
        self.is_player_bullet = is_player_bullet
        self.active = True
    
    def update(self, screen_height: int) -> None:
        """Update bullet position and check if it's still on screen."""
        self.y += self.velocity
        
        # Remove bullets that go off screen
        if self.y < 1 or self.y >= screen_height - 1:
            self.active = False
    
    def get_character(self) -> str:
        """Get the character representation of the bullet."""
        return '^' if self.is_player_bullet else 'v'
    
    def get_color(self) -> str:
        """Get the color of the bullet."""
        return Fore.WHITE
    
    def get_position(self) -> Tuple[int, int]:
        """Get current position as tuple."""
        return self.x, self.y
    
    def check_collision(self, target_x: int, target_y: int, target_width: int = 1) -> bool:
        """Check if bullet collides with a target at given position."""
        if not self.active:
            return False
        
        # Check if bullet position overlaps with target
        return (target_x <= self.x < target_x + target_width and 
                self.y == target_y)
    
    def destroy(self) -> None:
        """Mark bullet as inactive."""
        self.active = False
