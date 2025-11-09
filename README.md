# The Not-So-Russian-Roulette

A light-hearted, turn-based terminal game inspired by (but not encouraging) Russian Roulette. Players take turns pulling the trigger, shooting opponents, or triggering random events. The game includes animated console effects, environmental hazards, AI opponents, and a cameo ("Snoop Dogg") that can join the match.

> Note: This project is provided for entertainment and learning purposes only. It is not intended to glamorize or promote real-life dangerous behavior.

## Features
- Turn-based play between You and an AI opponent
- Randomized "bullets" (safe or bang) per round
- Special events (environmental hazards, potion, shields, surprise NPCs)
- Status effects: shields, drunken/confused state, temporary effects
- Console animations and typewriter effects
- Simple AI decision-making that reacts to health and status

## Requirements
- Python 3.8+
- Windows is recommended. The game uses `msvcrt.getch()` for player input which is only available on Windows. On other platforms you'll need to modify the input code (see "Porting to other OS" below).

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/DoodleSaurus/The-Not-So-Russian-Roulette.git
   cd The-Not-So-Russian-Roulette
   ```
2. Ensure you have Python 3 installed and available on your PATH.

No external dependencies are required beyond the Python standard library.

## Running the game
On Windows:
```
python roulette.py
```

Gameplay flow:
- You are player "You" and will be prompted to make choices each turn by pressing a key (1, 2, or 3).
  - 1 — Pull the trigger on yourself
  - 2 — Shoot your opponent
  - 3 — Feeling lucky (trigger a special random event)
- The AI opponent will take its turn automatically.
- Special events can add shields, cause damage from hazards, add NPCs, and more.
- The game ends when 0 or 1 players remain alive or when all bullets have been cycled.

## Porting to non-Windows platforms
The code currently imports `msvcrt` and calls `msvcrt.getch()` to read a single keypress for the human player. To run on macOS or Linux, replace the input handling with a cross-platform approach such as:
- Use `getch` from the `getch` package (`pip install getch`) and replace `msvcrt.getch()` with `getch.getch()`, or
- Use `input()` (requires pressing Enter) — replace the single-key logic with `choice = input().strip()`.

Example simple change:
```py
# at top of file, conditionally import
try:
    import msvcrt
    getch = lambda: msvcrt.getch().decode('utf-8')
except ImportError:
    import sys, tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
# then use getch() where msvcrt.getch() is used
```

## Customization
- Change the number range or rules inside the `Roulette` and `spin` logic to tweak difficulty.
- Add or adjust events in `spin_event()` and the event handler functions to expand gameplay variety.
- Adjust `delay` and animation timings for faster or slower feedback.

## Contributing
- Fork the repository, make changes on a feature branch, and open a pull request.
- Please ensure changes preserve the intended tone and do not promote real-life harm.

## License
This repository is licensed under Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0). See LICENSE for details.

## Disclaimer
This is a fictional game project for programming practice and fun. It should not be used to encourage or simulate dangerous real-world activities. Play responsibly.
