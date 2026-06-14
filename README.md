# 2048 GAME — Python Edition

A Python/Tkinter remake of the classic 2048 puzzle game, built as a follow-up to my original [C++ console version](https://github.com/ali4xk/Project2048). This version adds a full graphical interface, multiple difficulty levels, and a persistent leaderboard.

**Built by Muhammad Ali ([@ali4xk](https://github.com/ali4xk))**

---

## Features

- **Graphical interface** — built entirely with Python's built-in `tkinter` library (no external dependencies)
- **Three difficulty levels**
  - Easy — 4×4 grid
  - Medium — 6×6 grid
  - Hard — 10×10 grid
- **Classic 2048 mechanics** — slide and merge tiles with arrow keys or WASD
- **Live score tracking**
- **Persistent leaderboard** — scores are saved to `leaderboard.json` with player name, score, difficulty, grid size, and timestamp
  - Filter by difficulty
  - Search by player name
  - Top scores highlighted with medal icons
- **Quit anytime** — quitting mid-game saves your current score to the leaderboard

---

## Getting Started

### Requirements

- Python 3.8 or higher
- `tkinter` (included with most standard Python installations)

### Run the game

```bash
python3 game2048.py
```

No additional packages need to be installed.

---

## How to Play

1. Enter your player name and choose a difficulty on the main menu.
2. Use the **arrow keys** (or **W / A / S / D**) to slide tiles up, down, left, or right.
3. Tiles with the same number merge into one when they collide, adding to your score.
4. The game ends when no more moves are possible — your score is automatically saved to the leaderboard.
5. View the **🏆 Leaderboard** at any time from the menu or in-game header.

---

## Project Structure

```
.
├── game2048.py        # Main game file
├── leaderboard.json   # Auto-created on first game-over; stores all scores
└── README.md
```

---

## About

This project was built as a learning exercise to explore Python and `tkinter` after originally implementing 2048 in C++ with file-based leaderboard handling. The goal was to recreate the same core logic and features — grid-based movement, scoring, and persistent leaderboard storage — with a proper graphical interface.

## License

This project is open source and available for anyone to use, modify, and learn from.
