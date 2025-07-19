"""
ScreenshotService class for capturing game screenshots.
"""
import os
import shutil
from datetime import datetime
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from colorama import Fore
from render_state import RenderState


class ScreenshotService:
    """Handle screenshot capture and saving."""
    
    def __init__(self, screenshots_dir: str = "screenshots"):
        """Initialize screenshot service."""
        self.screenshots_dir = screenshots_dir
        self.font_size = 12
        self.char_width = 7
        self.char_height = 14
        self.font = self._load_font()
        
        # Create and clear screenshots directory
        self._setup_directory()
    
    def _setup_directory(self) -> None:
        """Create and clear the screenshots directory."""
        if os.path.exists(self.screenshots_dir):
            shutil.rmtree(self.screenshots_dir)
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def _load_font(self) -> Optional[ImageFont.ImageFont]:
        """Load a monospace font for rendering."""
        font_names = ["consolas.ttf", "cour.ttf", "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"]
        
        for font_name in font_names:
            try:
                # Try to load system font
                return ImageFont.truetype(font_name, self.font_size)
            except (OSError, IOError):
                continue
        
        try:
            # Fallback to default font
            return ImageFont.load_default()
        except (OSError, IOError):
            return None
    
    def _color_to_rgb(self, color_code: str) -> tuple:
        """Convert colorama color code to RGB tuple."""
        color_map = {
            Fore.BLACK: (0, 0, 0),
            Fore.RED: (255, 0, 0),
            Fore.GREEN: (0, 255, 0),
            Fore.YELLOW: (255, 255, 0),
            Fore.BLUE: (0, 0, 255),
            Fore.MAGENTA: (255, 0, 255),
            Fore.CYAN: (0, 255, 255),
            Fore.WHITE: (255, 255, 255),
        }
        return color_map.get(color_code, (255, 255, 255))
    
    def capture_screenshot(self, render_state: RenderState, score: int = 0, time_seconds: int = 0, bullets: int = 0) -> str:
        """Capture screenshot of current game state."""
        try:
            # Calculate image dimensions
            img_width = render_state.width * self.char_width
            img_height = render_state.height * self.char_height
            
            # Create image with black background
            image = Image.new('RGB', (img_width, img_height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Render each character
            for y in range(render_state.height):
                for x in range(render_state.width):
                    char, color = render_state.get_character(x, y)
                    
                    if char != ' ':  # Only draw non-space characters
                        # Calculate pixel position
                        pixel_x = x * self.char_width
                        pixel_y = y * self.char_height
                        
                        # Get RGB color
                        rgb_color = self._color_to_rgb(color)
                        
                        # Draw character
                        if self.font:
                            draw.text((pixel_x, pixel_y), char, fill=rgb_color, font=self.font)
                        else:
                            # Fallback: draw a small rectangle if no font is available
                            draw.rectangle([pixel_x, pixel_y, pixel_x + 4, pixel_y + 8], fill=rgb_color)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # Save image
            image.save(filepath, "PNG")
            return filepath
            
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return ""
    
    def auto_screenshot(self, render_state: RenderState, score: int, time_seconds: int, bullets: int) -> None:
        """Take automatic screenshot periodically."""
        # This can be called periodically during gameplay
        if time_seconds % 30 == 0 and time_seconds > 0:  # Every 30 seconds
            self.capture_screenshot(render_state, score, time_seconds, bullets)
