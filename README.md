# AI Cubic Solver — 3D Tic-Tac-Toe (4×4×4)
​
A three-dimensional Tic-Tac-Toe game (a 4×4×4 cube) built with **Pygame**, featuring
multiple search-based AI opponents (Minimax and Alpha-Beta pruning, with optional
heuristic evaluation for deeper, faster play).
​
You win by getting **four in a row** along *any* straight line through the cube —
rows, columns, vertical pillars, and the planar and space diagonals.
​
## Features
​
- Full 4×4×4 board rendered as four stacked 4×4 layers.
- Six selectable AI engines:
  - **Minimax** — exhaustive search to a fixed depth.
  - **Alpha-Beta** — Minimax with alpha-beta pruning (same result, faster).
  - **Heuristic variants** of both, which use a position evaluator (`ai/heuristicEval.py`)
    to score non-terminal nodes so the AI can "look ahead" without searching the
    full game tree.
- Board symmetry reduction (`ai/symmetry.py`) to prune equivalent positions.
- Restart at any time, plus a **New Game** button.
​
## Requirements
​
- Python 3.8–3.13
- `pygame`
​
## Installation & Run
​
```bash
git clone https://github.com/F4T00T42/Ai-Tic-Tac-Toe.git
cd Ai-Tic-Tac-Toe
pip install -r requirements.txt   # or: pip install pygame
python main.py
```
​
## Controls
​
- **Click** a cell to place your mark.
- **R** — restart the current game.
- **New Game** button — start over.
- Pick the AI engine from the in-game selection.
​
## Configuration (`config.py`)
​
| Setting              | Default | Meaning                                              |
| -------------------- | ------- | ---------------------------------------------------- |
| `BOARD_DIMENSIONS`   | `4`     | Cube size (4×4×4).                                    |
| `ROWS` / `COLS`      | `4`     | Derived board dimensions.                            |
| `PLAYER`             | `1`     | Human player marker.                                 |
| `AI`                 | `2`     | AI player marker.                                    |
| `maxDepth`           | `1`     | AI search depth. **Default is intentionally shallow** for instant moves — increase it (e.g. 2–3) for a much stronger but slower opponent. |
​
> **Tip:** Because the branching factor of a 64-cell board is large, raising
> `maxDepth` significantly increases think time. The Alpha-Beta and heuristic
> engines scale to higher depths far better than plain Minimax.
​
## Project Structure
​
```
main.py              # Entry point; window setup ("AI Cubic Solver") and game loop
board.py             # Board state + the six AI engine implementations
config.py            # Board dimensions, player markers, search depth
win_lines.py         # Precomputed set of all winning lines through the cube
draw.py              # Pygame rendering (layers, marks, UI)
utils.py             # Shared helpers
ai/
  minimax.py         # Minimax search
  alphabeta.py       # Alpha-Beta pruning search
  heuristicEval.py   # Position evaluation (threat counting) for heuristic engines
  symmetry.py        # Symmetry-based pruning of equivalent positions
```
​
## Known Issues / Notes
​
- `ai/minimax.py` and `ai/alphabeta.py` contain leftover debug `print()` calls
  that log to the console during AI turns. Remove them for clean output.
- **Coordinate-ordering inconsistency in `ai/heuristicEval.py`:** `count_threats`
  iterates coordinates as `(x, y, z)` but indexes `board.board[z][y][x]`, while
  `threat_based_eval` unpacks the same coordinates as `(z, y, x)`. If you tune the
  heuristic, verify the axis ordering is consistent.
​
## License
​
MIT
​
