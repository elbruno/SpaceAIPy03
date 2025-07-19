"""
GameManager class for managing game state and the main game loop.
"""
import time
import keyboard
from typing import Optional
from colorama import Fore, init as colorama_init
from utils import clear_screen, set_cursor_position, hide_cursor, get_terminal_dimensions, cleanup_console
from render_state import RenderState
from player import Player
from enemy import EnemyManager
from screenshot_service import ScreenshotService


class GameManager:
    """Manages game state, entities, and the main game loop."""
    
    def __init__(self, speed: int = 1, player_bullet_speed: int = 1, enemy_bullet_speed: int = 1):
        """Initialize game manager with specified speeds."""
        # Initialize colorama
        colorama_init(autoreset=True)
        
        # Game settings
        self.speed = speed
        self.player_bullet_speed = player_bullet_speed
        self.enemy_bullet_speed = enemy_bullet_speed
        self.target_fps = 20 + (speed * 10)  # 30, 40, 50 FPS for speeds 1, 2, 3
        self.frame_time = 1.0 / self.target_fps
        
        # Screen setup
        self.width, self.height = get_terminal_dimensions()
        self.game_area_width = min(self.width - 2, 78)  # Leave space for borders
        self.game_area_height = min(self.height - 2, 22)
        
        # Game state
        self.running = True
        self.score = 0
        self.start_time = time.time()
        self.last_screenshot_time = 0
        
        # Input state tracking to prevent continuous firing
        self.space_pressed = False
        
        # Initialize render state
        self.render_state = RenderState(self.game_area_width, self.game_area_height)
        
        # Initialize game entities
        player_start_x = self.game_area_width // 2
        player_start_y = self.game_area_height - 3
        self.player = Player(player_start_x, player_start_y, self.game_area_width, self.player_bullet_speed)
        self.enemy_manager = EnemyManager(self.game_area_width, bullet_speed=self.enemy_bullet_speed)
        
        # Initialize screenshot service
        self.screenshot_service = ScreenshotService()
        
        # Setup console
        hide_cursor()
        clear_screen()
    
    def handle_input(self) -> None:
        """Handle keyboard input non-blocking."""
        try:
            if keyboard.is_pressed('q'):
                self.running = False
            elif keyboard.is_pressed('left') or keyboard.is_pressed('a'):
                self.player.move_left()
            elif keyboard.is_pressed('right') or keyboard.is_pressed('d'):
                self.player.move_right()
            elif keyboard.is_pressed('space'):
                # Only shoot on initial press, not while held
                if not self.space_pressed:
                    self.player.shoot()
                    self.space_pressed = True
            else:
                # Reset space key state when not pressed
                if self.space_pressed:
                    self.space_pressed = False
                    
            if keyboard.is_pressed('s'):
                self.take_screenshot()
        except:
            # Fallback for systems where keyboard library doesn't work
            pass
    
    def update_entities(self) -> None:
        """Update all game entities."""
        # Update player
        self.player.update(self.game_area_height)
        
        # Update enemies
        self.enemy_manager.update(self.game_area_height)
        
        # Check collisions
        self._check_collisions()
        
        # Check win/lose conditions
        self._check_game_conditions()
    
    def _check_collisions(self) -> None:
        """Check all collision scenarios."""
        # Player bullets vs enemies
        score_gained = self.enemy_manager.check_bullet_collisions(self.player.bullets)
        self.score += score_gained
        
        # Enemy bullets vs player
        for bullet in self.enemy_manager.bullets:
            if bullet.active and self.player.check_collision(bullet.x, bullet.y):
                self.player.destroy()
                bullet.destroy()
                self.running = False  # Game over
    
    def _check_game_conditions(self) -> None:
        """Check for win/lose conditions."""
        # Check if all enemies are defeated
        if self.enemy_manager.all_enemies_defeated():
            self.running = False  # Player wins
        
        # Check if enemies reached the bottom
        alive_enemies = self.enemy_manager.get_alive_enemies()
        for enemy in alive_enemies:
            if enemy.y >= self.game_area_height - 5:  # Too close to player area
                self.running = False  # Game over
    
    def render_frame(self) -> None:
        """Render the current frame using double buffering."""
        # Clear buffer
        self.render_state.clear_buffer()
        
        # Draw bounding box
        self.render_state.draw_box(0, 0, self.game_area_width - 1, self.game_area_height - 1, Fore.WHITE)
        
        # Draw UI
        current_time = int(time.time() - self.start_time)
        ui_text = f"Score: {self.score:04d}   Time: {current_time:02d}s   Bullets: {self.player.get_bullet_count()}/3"
        self.render_state.draw_text(2, 1, ui_text, Fore.WHITE)
        
        # Draw player
        if self.player.alive:
            px, py = self.player.get_position()
            self.render_state.set_character(px, py, self.player.get_character(), self.player.get_color())
        
        # Draw player bullets
        for bullet in self.player.bullets:
            if bullet.active:
                bx, by = bullet.get_position()
                self.render_state.set_character(bx, by, bullet.get_character(), bullet.get_color())
        
        # Draw enemies
        for enemy in self.enemy_manager.get_alive_enemies():
            ex, ey = enemy.get_position()
            enemy_text = enemy.get_character()
            enemy_color = enemy.get_color()
            
            # Draw multi-character enemies
            for i, char in enumerate(enemy_text):
                self.render_state.set_character(ex + i, ey, char, enemy_color)
        
        # Draw enemy bullets
        for bullet in self.enemy_manager.bullets:
            if bullet.active:
                bx, by = bullet.get_position()
                self.render_state.set_character(bx, by, bullet.get_character(), bullet.get_color())
        
        # Update only changed positions
        changed_positions = self.render_state.get_changed_positions()
        
        for x, y in changed_positions:
            char, color = self.render_state.get_character(x, y)
            # Offset by 1 to account for terminal coordinates starting at 1
            set_cursor_position(x + 1, y + 1)
            print(f"{color}{char}", end='', flush=True)
        
        # Update previous buffers
        self.render_state.update_previous_buffers()
    
    def take_screenshot(self) -> None:
        """Take a manual screenshot."""
        current_time = int(time.time() - self.start_time)
        filepath = self.screenshot_service.capture_screenshot(
            self.render_state, self.score, current_time, self.player.get_bullet_count()
        )
        if filepath:
            # Show brief message
            set_cursor_position(2, self.game_area_height + 2)
            print(f"{Fore.GREEN}Screenshot saved: {filepath}", end='', flush=True)
    
    def get_render_state(self) -> RenderState:
        """Get current render state for screenshot service."""
        return self.render_state
    
    def run_game_loop(self) -> None:
        """Run the main game loop."""
        try:
            while self.running:
                frame_start = time.perf_counter()
                
                # Handle input (non-blocking)
                self.handle_input()
                
                # Update game state
                self.update_entities()
                
                # Render frame (only differences)
                self.render_frame()
                
                # Auto screenshot every 30 seconds
                current_time = time.time()
                if current_time - self.last_screenshot_time >= 30:
                    self.last_screenshot_time = current_time
                    elapsed_seconds = int(current_time - self.start_time)
                    self.screenshot_service.auto_screenshot(
                        self.render_state, self.score, elapsed_seconds, self.player.get_bullet_count()
                    )
                
                # Frame timing
                elapsed = time.perf_counter() - frame_start
                if elapsed < self.frame_time:
                    time.sleep(self.frame_time - elapsed)
            
            # Game over screen
            self._show_game_over()
            
        except KeyboardInterrupt:
            pass
        finally:
            cleanup_console()
    
    def _show_game_over(self) -> None:
        """Display game over screen."""
        set_cursor_position(1, self.game_area_height + 3)
        final_time = int(time.time() - self.start_time)
        
        if not self.player.alive:
            print(f"{Fore.RED}GAME OVER! You were hit!")
        elif self.enemy_manager.all_enemies_defeated():
            print(f"{Fore.GREEN}VICTORY! All enemies defeated!")
        else:
            print(f"{Fore.YELLOW}Game ended.")
        
        print(f"{Fore.WHITE}Final Score: {self.score}")
        print(f"{Fore.WHITE}Time Survived: {final_time} seconds")
        print(f"{Fore.WHITE}Press any key to exit...")
        
        try:
            input()
        except:
            pass
