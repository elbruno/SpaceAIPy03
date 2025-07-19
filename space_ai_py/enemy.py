"""
Enemy class for managing enemy entities, movement, and behavior.
"""
import random
from typing import List, Tuple, Optional
from colorama import Fore
from bullet import Bullet


class Enemy:
    """Individual enemy entity with position and display properties."""
    
    def __init__(self, x: int, y: int, enemy_type: str, color: str):
        """Initialize enemy with position and visual properties."""
        self.x = x
        self.y = y
        self.enemy_type = enemy_type  # "><", "oo", "/O\"
        self.color = color
        self.alive = True
        self.width = len(enemy_type)
    
    def get_character(self) -> str:
        """Get the character representation of the enemy."""
        return self.enemy_type
    
    def get_color(self) -> str:
        """Get the color of the enemy."""
        return self.color
    
    def get_position(self) -> Tuple[int, int]:
        """Get current position as tuple."""
        return self.x, self.y
    
    def move(self, dx: int, dy: int) -> None:
        """Move enemy by given offset."""
        self.x += dx
        self.y += dy
    
    def check_collision(self, bullet_x: int, bullet_y: int) -> bool:
        """Check if a bullet hits this enemy."""
        if not self.alive:
            return False
        return (self.x <= bullet_x < self.x + self.width and 
                self.y == bullet_y)
    
    def destroy(self) -> None:
        """Mark enemy as destroyed."""
        self.alive = False


class EnemyManager:
    """Manages all enemies, their movement patterns, and shooting."""
    
    def __init__(self, screen_width: int, start_y: int = 3):
        """Initialize enemy formation."""
        self.screen_width = screen_width
        self.enemies: List[Enemy] = []
        self.bullets: List[Bullet] = []
        self.direction = 1  # 1 for right, -1 for left
        self.move_counter = 0
        self.shoot_counter = 0
        self.shoot_interval = 60  # frames between enemy shots
        
        # Create enemy formation
        self._create_enemies(start_y)
    
    def _create_enemies(self, start_y: int) -> None:
        """Create the initial enemy formation."""
        self.enemies.clear()
        
        # Top row (5 enemies): ><, oo, ><, oo, ><
        top_row_types = ["><", "oo", "><", "oo", "><"]
        start_x = (self.screen_width - (5 * 4)) // 2  # Center the formation
        
        for i, enemy_type in enumerate(top_row_types):
            x = start_x + (i * 4)
            enemy = Enemy(x, start_y, enemy_type, Fore.RED)
            self.enemies.append(enemy)
        
        # Bottom row (3 enemies): /O\
        bottom_row_start_x = (self.screen_width - (3 * 5)) // 2  # Center 3 enemies
        for i in range(3):
            x = bottom_row_start_x + (i * 5)
            enemy = Enemy(x, start_y + 2, "/O\\", Fore.YELLOW)
            self.enemies.append(enemy)
    
    def update(self, screen_height: int) -> None:
        """Update enemy positions and bullets."""
        # Update enemy bullets
        for bullet in self.bullets:
            bullet.update(screen_height)
        
        # Remove inactive bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        
        # Move enemies
        self._update_enemy_movement()
        
        # Handle enemy shooting
        self._handle_enemy_shooting()
    
    def _update_enemy_movement(self) -> None:
        """Update enemy movement in sweep pattern."""
        self.move_counter += 1
        
        if self.move_counter >= 20:  # Move every 20 frames
            self.move_counter = 0
            
            # Check if any enemy hits the screen edge
            hit_edge = False
            alive_enemies = [e for e in self.enemies if e.alive]
            
            if alive_enemies:
                if self.direction == 1:  # Moving right
                    rightmost = max(e.x + e.width for e in alive_enemies)
                    if rightmost >= self.screen_width - 3:
                        hit_edge = True
                else:  # Moving left
                    leftmost = min(e.x for e in alive_enemies)
                    if leftmost <= 2:
                        hit_edge = True
                
                if hit_edge:
                    # Change direction and move down
                    self.direction *= -1
                    for enemy in alive_enemies:
                        enemy.move(0, 1)  # Move down
                else:
                    # Move horizontally
                    for enemy in alive_enemies:
                        enemy.move(self.direction, 0)
    
    def _handle_enemy_shooting(self) -> None:
        """Handle enemy shooting behavior."""
        self.shoot_counter += 1
        
        if self.shoot_counter >= self.shoot_interval:
            self.shoot_counter = 0
            
            # Only one enemy shoots at a time
            alive_enemies = [e for e in self.enemies if e.alive]
            if alive_enemies and len(self.bullets) < 2:  # Limit enemy bullets
                shooter = random.choice(alive_enemies)
                bullet = Bullet(shooter.x + shooter.width // 2, shooter.y + 1, 1, is_player_bullet=False)
                self.bullets.append(bullet)
    
    def get_alive_enemies(self) -> List[Enemy]:
        """Get list of all living enemies."""
        return [enemy for enemy in self.enemies if enemy.alive]
    
    def check_bullet_collisions(self, player_bullets: List[Bullet]) -> int:
        """Check collisions between player bullets and enemies. Returns score gained."""
        score = 0
        
        for bullet in player_bullets:
            if not bullet.active:
                continue
                
            for enemy in self.enemies:
                if enemy.alive and enemy.check_collision(bullet.x, bullet.y):
                    enemy.destroy()
                    bullet.destroy()
                    score += 10  # Points per enemy
                    break
        
        return score
    
    def all_enemies_defeated(self) -> bool:
        """Check if all enemies are defeated."""
        return len(self.get_alive_enemies()) == 0
