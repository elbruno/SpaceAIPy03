# Space.AI.PY() 🚀

A Python console-based Space Invaders-style game built with AI assistance. Experience classic arcade gameplay with modern Python programming, featuring smooth animations, colorful graphics, and automatic screenshot capture.

![Game Preview](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![Status](https://img.shields.io/badge/Status-Playable-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## 🎮 What's This Game About?

Space.AI.PY() is a terminal-based space shooter where you defend Earth from an alien invasion! Control your spaceship, dodge enemy fire, and eliminate all invaders before they reach the surface. Built with Python and featuring:

- **Flicker-free rendering** using double-buffered display
- **Unicode box-drawing characters** for crisp visuals
- **Cross-platform colored output** via colorama
- **Non-blocking input handling** for smooth gameplay
- **Automatic screenshot capture** to save your best moments
- **Three difficulty levels** (Slow, Medium, Fast)

## 📁 Repository Structure

```
space_ai_py/
├── main.py                 # Entry point - handles startup and speed selection
├── start_screen.py         # Start screen display with game instructions
├── game_manager.py         # Main game loop, state management, and rendering
├── player.py              # Player character movement, shooting, and collision
├── enemy.py               # Enemy formation, movement patterns, and AI
├── bullet.py              # Bullet physics and collision detection
├── screenshot_service.py  # Screenshot capture using PIL
├── render_state.py        # Double-buffered rendering system
├── utils.py               # Console utilities and terminal management
├── requirements.txt       # Python dependencies
├── screenshots/           # Auto-generated folder for game screenshots
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or higher)
- **pip** (Python package installer)

### Quick Start

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd space_ai_py
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install colorama keyboard pillow
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

### Dependencies Explained

- **colorama** (0.4.6+): Cross-platform colored terminal text output
- **keyboard** (0.13.5+): Non-blocking keyboard input detection
- **pillow** (10.4.0+): Screenshot capture and image processing

## 🎯 How to Play

### Game Objective
Eliminate all 8 enemies before they reach the bottom of the screen or hit you with their bullets!

### Controls
| Key | Action |
|-----|--------|
| `←` or `A` | Move spaceship left |
| `→` or `D` | Move spaceship right |
| `SPACE` | Fire bullet (max 3 bullets on screen) |
| `S` | Take manual screenshot |
| `Q` | Quit game |

### Game Elements

#### Your Spaceship
- **Character**: `A`
- **Color**: Cyan
- **Lives**: 1 (game over if hit)
- **Bullets**: Maximum 3 active bullets at once

#### Enemy Formation
- **Top Row (5 enemies)**: `><` `oo` `><` `oo` `><` (Red)
- **Bottom Row (3 enemies)**: `/O\` `/O\` `/O\` (Yellow)
- **Movement**: Classic sweep pattern - move horizontally, then down
- **Shooting**: Only one enemy shoots at a time

#### Scoring System
- **10 points** per enemy destroyed
- **Bonus**: Faster completion = better bragging rights!

### Game Speed Options
At startup, choose your preferred difficulty:
1. **Slow** (30 FPS) - Perfect for beginners
2. **Medium** (40 FPS) - Balanced challenge  
3. **Fast** (50 FPS) - For arcade veterans

## 🖼️ Screenshot Feature

The game automatically captures screenshots:
- **Automatic**: Every 30 seconds during gameplay
- **Manual**: Press `S` key anytime
- **Storage**: Saved in `screenshots/` folder with timestamps
- **Format**: PNG files with game state preserved

Screenshot filenames: `screenshot_YYYYMMDD_HHMMSS.png`

## 🎨 Technical Features

### Rendering System
- **Double-buffered rendering**: Eliminates screen flicker
- **Unicode box-drawing**: Clean, crisp game borders (┌ ┐ └ ┘ ─ │)
- **Color-coded elements**: Easy visual distinction
- **Optimized updates**: Only changed screen areas are redrawn

### Input Handling
- **Non-blocking input**: Smooth real-time controls
- **Key state tracking**: Prevents accidental rapid-fire
- **Shot cooldown**: 300ms between bullets for balanced gameplay

### Cross-Platform Compatibility
- **Windows**: Full support with proper console handling
- **macOS/Linux**: Terminal compatibility with fallback options
- **UTF-8 encoding**: Proper Unicode character display

## 🚀 Advanced Usage

### Running with Custom Python Environment
If using a virtual environment:
```bash
# Activate your virtual environment first
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

python main.py
```

### Troubleshooting

**Keyboard Input Issues:**
- On some Linux systems, you may need to run with `sudo` for keyboard access
- Alternative: Use WASD keys instead of arrow keys

**Display Problems:**
- Ensure your terminal supports UTF-8 encoding
- Try increasing terminal size if game appears cramped
- Some terminals may not support all Unicode characters

**Permission Errors (Screenshots):**
- Ensure write permissions in the game directory
- Screenshots folder is auto-created but needs write access

## 🏗️ Development & Customization

### Code Structure
The game follows object-oriented design principles:

- **Entity System**: Separate classes for Player, Enemy, Bullet
- **State Management**: Centralized game state in GameManager
- **Rendering Pipeline**: Modular render state system
- **Service Layer**: Screenshot and utility services

### Customization Ideas
Want to modify the game? Here are some starting points:

- **Difficulty**: Adjust enemy speed, bullet speed, or spawn rates in `enemy.py`
- **Graphics**: Modify character representations in each entity class
- **Scoring**: Change point values in `game_manager.py`
- **Controls**: Add new key bindings in `game_manager.py`
- **Effects**: Enhance screenshot service or add sound effects

### Code Quality
- **Type hints**: Full typing support for better IDE experience
- **Documentation**: Comprehensive docstrings throughout
- **Error handling**: Graceful fallbacks for platform differences
- **Performance**: Optimized rendering and input loops

## 📜 Game History

This project was created as a Python adaptation of a C# Space Invaders specification. The original concept called for a flicker-free console game with proper Unicode rendering, which inspired this modern Python implementation.

## 🤝 Contributing

Feel free to fork this project and add your own features! Some ideas:
- Sound effects and music
- Power-ups and special weapons  
- Multiple levels with different enemy patterns
- High score persistence
- Network multiplayer support

## 📄 License

This project is created for educational and entertainment purposes. Feel free to use, modify, and share!

---

**Ready to defend Earth? Run `python main.py` and start your space adventure!** 🛸✨

*Built with Python + AI for galactic defense*
