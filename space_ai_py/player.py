"""
Player class for managing player character, movement, and shooting.
"""
import time
from typing import List, Tuple
from colorama import Fore
from bullet import Bullet


class Player:
    """Manages player position, movement, and bullet firing."""
    
    def __init__(self, x: int, y: int, screen_width: int, bullet_speed: int = 1):
        """Initialize player with starting position, screen bounds, and bullet speed."""
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.bullet_speed = bullet_speed
        self.max_bullets = 3
        self.bullets: List[Bullet] = []
        self.alive = True
        self.last_shot_time = 0
        self.shot_cooldown = 0.3  # 300ms cooldown between shots
    
    def move_left(self) -> None:
        """Move player left within screen bounds."""
        if self.x > 2:  # Stay within game area (inside border)
            self.x -= 1
    
    def move_right(self) -> None:
        """Move player right within screen bounds."""
        if self.x < self.screen_width - 3:  # Stay within game area (inside border)
            self.x += 1
    
    def shoot(self) -> bool:
        """Fire a bullet if under the bullet limit and cooldown has elapsed."""
        current_time = time.time()
        
        # Check if enough time has passed since last shot
        if current_time - self.last_shot_time < self.shot_cooldown:
            return False
        
        # Remove inactive bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        
        if len(self.bullets) < self.max_bullets:
            # Create new bullet at player position with configurable speed
            bullet_velocity = -self.bullet_speed  # Negative for upward movement
            bullet = Bullet(self.x, self.y - 1, bullet_velocity, is_player_bullet=True)
            self.bullets.append(bullet)
            self.last_shot_time = current_time  # Update last shot time
            return True
        return False
    
    def update(self, screen_height: int) -> None:
        """Update player bullets."""
        # Update all bullets
        for bullet in self.bullets:
            bullet.update(screen_height)
        
        # Remove inactive bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.active]
    
    def get_character(self) -> str:
        """Get the character representation of the player."""
        return 'A'
    
    def get_color(self) -> str:
        """Get the color of the player."""
        return Fore.CYAN
    
    def get_position(self) -> Tuple[int, int]:
        """Get current position as tuple."""
        return self.x, self.y
    
    def get_bullet_count(self) -> int:
        """Get current number of active bullets."""
        return len([bullet for bullet in self.bullets if bullet.active])
    
    def check_collision(self, bullet_x: int, bullet_y: int) -> bool:
        """Check if a bullet hits the player."""
        return self.x == bullet_x and self.y == bullet_y
    
    def destroy(self) -> None:
        """Mark player as destroyed."""
        self.alive = False
