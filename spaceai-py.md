# Python Console Project: Space Invaders-style Game — Title: Space.AI.PY()
# This prompt is for creating a modular, flicker-free, color-rendered console game using Python.

# Objective:
# Build a modular, flicker-free, color-rendered console game titled "Space.AI.PY()".
# The game must support input handling, player/enemy movement and bullets, UI, screenshot capture, double-buffered rendering, and a polished start screen layout.

# Required Dependencies:
# - colorama: For cross-platform colored terminal text
# - keyboard: For non-blocking input handling
# - Pillow (PIL): For screenshot capture to PNG/JPG
# - Install with: pip install colorama keyboard pillow

# FILE: main.py
# Responsibilities:
# - Import all necessary modules
# - Initialize colorama with colorama.init()
# - Set up console for UTF-8 encoding (if needed)
# - Hide cursor
# - Call start_screen.show()
# - After that, read the user input for speed selection:
#     [1] Slow (default), [2] Medium, [3] Fast
#     ENTER defaults to slow
# - Clear the console and call game_manager.run_game_loop()

# FILE: start_screen.py
# Class: StartScreen
# Responsibilities:
# - Display the start screen with layout:
#   - Title: "Space.AI.PY()" — centered horizontally
#   - Subtitle (optional): "Built with Python + AI for galactic defense"
#   - Instructions and speed options: **left-aligned**
#     Example layout:
#
#     How to Play:
#     ←   Move Left
#     →   Move Right
#     SPACE   Shoot
#     S   Take Screenshot
#     Q   Quit
#
#     Select Game Speed:
#     [1] Slow (default)
#     [2] Medium
#     [3] Fast
#     Press ENTER for default
#
# - Use os.get_terminal_size() to get console dimensions for alignment
# - This class is for display only — input is handled in main.py

# FILE: game_manager.py
# Class: GameManager
# Responsibilities:
# - Manage game state and the main loop
# - Initialize player, enemies, bullets, UI
# - Handle input using keyboard.is_pressed() for non-blocking input detection
#     - Check for arrow keys, spacebar, 'S', and 'Q'
#     - Use threading or async approach if needed for smooth gameplay
# - Update all entities each frame
# - Implement double-buffered rendering:
#     - Maintain current and previous character/color buffers as 2D arrays
#     - Update only changed characters using cursor positioning
#     - Use ANSI escape codes or colorama for positioning: \033[row;colH
#     - Do not clear entire screen each frame
# - Hide cursor
# - Draw bounding box using Unicode box-drawing characters:
#     - ┌ ┐ └ ┘ for corners
#     - ─ for horizontal edges
#     - │ for vertical edges
#     - Ensure proper UTF-8 encoding for Unicode support
# - Draw UI inside the top of the box:
#     Format: "Score: 0000   Time: 00s   Bullets: 2/3"
# - Expose get_render_state() method for ScreenshotService
# - Trigger ScreenshotService periodically and on 'S' key press
# - Handle game timing with time.sleep() or time.perf_counter()

# FILE: player.py
# Class: Player
# Responsibilities:
# - Rendered as 'A'
# - Controlled with Left/Right arrow keys
# - Fires up to 3 bullets using Spacebar
# - Constrained to lower area of screen
# - Track position (x, y coordinates)
# - Handle movement bounds checking

# FILE: enemy.py
# Class: Enemy
# Responsibilities:
# - 8 total enemies:
#     - Top row (5): ><, oo, ><, oo, >< — Red color
#     - Bottom row (3): /O\ — Yellow/Orange color
# - Move left to right, sweep-style
# - After each full sweep, move down one row
# - Only one enemy may shoot at a time
# - Track individual enemy positions and states
# - Handle collision detection

# FILE: bullet.py
# Class: Bullet
# Responsibilities:
# - Bullets move vertically each frame
# - Player bullets: '^' (move up)
# - Enemy bullets: 'v' (move down)
# - Detect collisions with enemies or player
# - Remove bullets when they hit targets or go off-screen
# - Track position and velocity

# FILE: screenshot_service.py
# Class: ScreenshotService
# Responsibilities:
# - Create and clear a folder named "screenshots" on game start
# - Capture screenshots automatically and manually (S key)
# - Use game_manager.get_render_state() to retrieve current frame buffers
# - Render to PNG using PIL (Pillow):
#     - Create image with appropriate size
#     - Use monospace font if available ("Consolas" or "Courier New")
#     - Draw each character with proper colors
# - Include in screenshot:
#     - Bounding box using Unicode characters (┌ ┐ └ ┘ ─ │)
#     - UI line with game stats
#     - Player, enemies, bullets with correct colors
# - Save with timestamp: screenshot_YYYYMMDD_HHMMSS.png

# FILE: render_state.py
# Class: RenderState
# Responsibilities:
# - Store current frame state as 2D arrays
# - character_buffer: 2D array of characters
# - color_buffer: 2D array of color information
# - Provide methods to update and compare buffers
# - Support for colorama color codes or RGB values

# FILE: utils.py
# Utility functions:
# - clear_screen(): Clear console without flickering
# - set_cursor_position(x, y): Move cursor to specific position
# - hide_cursor() / show_cursor(): Control cursor visibility
# - get_terminal_dimensions(): Return width, height of console

# Color Scheme (using colorama.Fore):
# - Player ('A'): Fore.CYAN
# - 2-char enemies (><, oo): Fore.RED
# - 3-char enemies (/O\): Fore.YELLOW
# - Player bullets ('^'): Fore.WHITE
# - Enemy bullets ('v'): Fore.WHITE
# - UI text: Fore.WHITE
# - Bounding box: Fore.WHITE

# Input Handling:
# - Use keyboard library for non-blocking input detection
# - Check for multiple keys simultaneously
# - Handle key press events without blocking game loop
# - Alternative: Use threading with input() for basic implementation

# Rendering Rules:
# - Do not clear entire screen each frame (causes flickering)
# - Use double-buffered rendering (only update changed characters)
# - Hide cursor during gameplay
# - Use correct Unicode box-drawing characters: ┌ ┐ └ ┘ ─ │
# - Ensure UTF-8 encoding support for Unicode characters
# - Use ANSI escape codes or colorama for cursor positioning
# - Update characters individually using cursor movement

# Game Loop Structure:
# ```python
# import time
# 
# def run_game_loop():
#     clock = time.perf_counter()
#     target_fps = 30  # or based on speed selection
#     frame_time = 1.0 / target_fps
#     
#     while running:
#         frame_start = time.perf_counter()
#         
#         # Handle input (non-blocking)
#         handle_input()
#         
#         # Update game state
#         update_entities()
#         
#         # Render (only differences)
#         render_frame()
#         
#         # Frame timing
#         elapsed = time.perf_counter() - frame_start
#         if elapsed < frame_time:
#             time.sleep(frame_time - elapsed)
# ```

# Project Structure:
# ```
# space_ai_py/
# ├── main.py
# ├── start_screen.py
# ├── game_manager.py
# ├── player.py
# ├── enemy.py
# ├── bullet.py
# ├── screenshot_service.py
# ├── render_state.py
# ├── utils.py
# ├── requirements.txt
# └── screenshots/
# ```

# Additional Python-Specific Features:
# - Use type hints for better code documentation
# - Implement proper exception handling
# - Use dataclasses for game entities if appropriate
# - Consider using enum for game states and colors
# - Add docstrings to all classes and methods

# Performance Considerations:
# - Minimize string operations in the render loop
# - Use list comprehensions where appropriate
# - Cache frequently used calculations
# - Optimize buffer comparison operations
# - Consider using numpy arrays for large buffers (optional)

# Cross-Platform Compatibility:
# - Use os.name to detect platform
# - Handle different terminal capabilities
# - Provide fallback for systems without advanced terminal features
# - Test on Windows, macOS, and Linux terminals
