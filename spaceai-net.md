// C# Console Project: Space Invaders-style Game — Title: Space.AI.NET()
// This prompt is for GitHub Copilot Agent Mode, starting from an empty C# console project.

// Objective:
// Build a modular, flicker-free, color-rendered console game titled "Space.AI.NET()".
// The game must support input handling, player/enemy movement and bullets, UI, screenshot capture, double-buffered rendering, and a polished start screen layout.

// FILE: Program.cs
// Responsibilities:
// - Set UTF-8 output encoding for box-drawing characters:
//     Console.OutputEncoding = System.Text.Encoding.UTF8;
// - Set Console.CursorVisible = false
// - Call StartScreen.Show()
// - After that, read the user input for speed selection:
//     [1] Slow (default), [2] Medium, [3] Fast
//     ENTER defaults to slow
// - Clear the console and call GameManager.RunGameLoop()

// FILE: StartScreen.cs
// Class: StartScreen
// Responsibilities:
// - Display the start screen with layout:
//   - Title: "Space.AI.NET()" — centered horizontally
//   - Subtitle (optional): "Built with .NET + AI for galactic defense"
//   - Instructions and speed options: **left-aligned**
//     Example layout:
//
//     How to Play:
//     ←   Move Left
//     →   Move Right
//     SPACE   Shoot
//     S   Take Screenshot
//     Q   Quit
//
//     Select Game Speed:
//     [1] Slow (default)
//     [2] Medium
//     [3] Fast
//     Press ENTER for default
//
// - Use Console.WindowWidth and Console.WindowHeight to align content
// - This class is for display only — input is handled in Program.cs

// FILE: GameManager.cs
// Class: GameManager
// Responsibilities:
// - Manage game state and the main loop
// - Initialize player, enemies, bullets, UI
// - Handle input using Console.KeyAvailable and Console.ReadKey(true)
//     - Do not use background threads for input
// - Update all entities
// - Implement double-buffered rendering:
//     - Maintain current and previous char/color buffers
//     - Update only changed characters using Console.SetCursorPosition()
//     - Do not use Console.Clear()
// - Hide cursor with Console.CursorVisible = false
// - Draw bounding box using Unicode box-drawing characters:
//     - ┌ ┐ └ ┘ for corners
//     - ─ for horizontal edges
//     - │ for vertical edges
//     - Do not use fallback ASCII characters like '+', '-', '|', or '?'
//     - REQUIREMENT: Set Console.OutputEncoding = System.Text.Encoding.UTF8 before any rendering to ensure proper character support
// - Draw UI inside the top of the box:
//     Format: "Score: 0000   Time: 00s   Bullets: 2/3"
// - Expose GetRenderState() for ScreenshotService
// - Trigger ScreenshotService periodically and on 'S' key

// FILE: Player.cs
// Class: Player
// Responsibilities:
// - Rendered as 'A'
// - Controlled with Left/Right arrow keys
// - Fires up to 3 bullets using Spacebar
// - Constrained to lower area of screen

// FILE: Enemy.cs
// Class: Enemy
// Responsibilities:
// - 8 total enemies:
//     - Top row (5): ><, oo, ><, oo, >< — ConsoleColor.Red
//     - Bottom row (3): /O\ — ConsoleColor.DarkYellow
// - Move left to right, sweep-style
// - After each full sweep, move down one row
// - Only one enemy may shoot at a time

// FILE: Bullet.cs
// Class: Bullet
// Responsibilities:
// - Bullets move vertically
// - Player bullets: '^'
// - Enemy bullets: 'v'
// - Detect collisions with enemies or player

// FILE: ScreenshotService.cs
// Class: ScreenshotService
// Responsibilities:
// - Create and clear a folder named "screenshoots" on game start
// - Capture screenshots automatically and manually (S key)
// - Use GameManager.GetRenderState() to retrieve buffers
// - Render to PNG or JPG using System.Drawing.Bitmap and Graphics
// - Use Unicode-compatible monospace font ("Consolas" or "Lucida Console") for correct visuals
// - Include:
//     - Bounding box using Unicode characters (┌ ┐ └ ┘ ─ │)
//     - UI line
//     - Player, enemies, bullets

// FILE: RenderState.cs (optional)
// Class: RenderState
// Responsibilities:
// - Maintain current frame buffers for characters and colors

// Visual Settings:
// - Player ('A'): ConsoleColor.Cyan
// - 2-char enemies (><, oo): ConsoleColor.Red
// - 3-char enemies (/O\): ConsoleColor.DarkYellow
// - Player bullets: '^', ConsoleColor.White
// - Enemy bullets: 'v', ConsoleColor.White
// - UI text: ConsoleColor.White

// Rendering Rules:
// - Do not use Console.Clear()
// - Use double-buffered rendering (only update differences)
// - Hide cursor using Console.CursorVisible = false
// - Use correct Unicode box-drawing characters:
//     ┌ ┐ └ ┘ ─ │
// - REQUIREMENT: Set Console.OutputEncoding = System.Text.Encoding.UTF8 before any output
// - Never use fallback characters like '+', '-', '|', or '?'