# AI 3D Tic Tac Toe

A Python-based 3D Tic Tac Toe game powered by **Pygame** with an AI opponent using the **Minimax algorithm**. The game features a 4×4×4 3D board, real-time graphics, and smart AI moves.

---

## Features

* **3D 4×4×4 Board:** Play on four stacked layers with 4×4 grids each.
* **AI Opponent:** Challenge the computer using the Minimax, Alpha-Beta pruning or 2 Heuristic function algorithms.
* **Interactive GUI:** Click to place your mark; the AI responds immediately.
* **Win Detection:** Detects horizontal, vertical, diagonal, and cross-dimensional wins.
* **Restart Option:** Reset the game anytime by pressing `R`.
* **Color-coded End Game:**

  * Green for player win
  * Red for AI win
  * Gray for a tie

---

## Requirements

* Python **3.8 – 3.13** (Pygame does not officially support Python 3.14 yet)
* [Pygame](https://www.pygame.org/news)
* [NumPy](https://numpy.org/)

**Tip:** To check which Python versions your Pygame supports, run:

```bash
python -m pip show pygame
```

Or visit the [Pygame release page](https://github.com/pygame/pygame/releases) to see version compatibility.

---

Install dependencies via pip:

```bash
pip install pygame numpy
```

---

## How to Play

1. Run the game:

```bash
python tic_tac_toe_3d.py
```

2. Click on a square to place your mark (Player 1).
3. The AI (Player 2) will automatically make its move.
4. Watch for a win or tie.
5. Press `R` to restart the game at any time.

---

## Game Rules

* Players alternate turns placing X (player) or O (AI) on any available square.
* The goal is to get **four in a row**: horizontally, vertically, diagonally, or across dimensions.
* The game ends when either player wins or the board is full (tie).

---

## File Structure

```
Ai-Tic-Tac-Toe/
│
├── main.py                  # Game loop, input handling, and overall control
│
├── board.py                 # Board class: state, move placement, resets, win logic
├── draw.py                  # Rendering: grid, shapes, colors, endgame effects
├── config.py                # All configuration values: sizes, colors, dimensions
├── utils.py                 # Board utilities: 3d or 2d projection function, rotate function 
├── win_lines.py             # All win conditions: win conditions and cells.
│
├── ai/                      # AI engines (Minimax, Alpha-Beta, evaluation heuristics)
│   └── alphabeta.py
│   └── heuristicEval.py
│   └── minimax.py
│   └── symmetry.py
│
└── README.md                # Project documentation
```

---

## Customization

* **Board Size:** Change `BOARD_DIMENSIONS`, `BOARD_ROWS`, and `BOARD_COLS` in the code.
* **AI Difficulty:** Adjust `maxDepth` to make AI smarter (higher values = stronger AI, slower performance).
* **Colors & UI:** Modify RGB values and line widths for a personalized look.
