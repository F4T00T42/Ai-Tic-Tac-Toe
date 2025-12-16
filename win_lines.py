import itertools
from config import BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS

def generate_winning_lines(N):
  lines = []

  rng = range(N)

  # Rows & columns in each layer
  for d in rng:
    for r in rng:
      lines.append([(d, r, c) for c in rng])  # rows
    for c in rng:
      lines.append([(d, r, c) for r in rng])  # columns

    # layer diagonals
    lines.append([(d, i, i) for i in rng])
    lines.append([(d, i, N-1-i) for i in rng])

  # verticals through layers
  for r in rng:
    for c in rng:
      lines.append([(d, r, c) for d in rng])

  # diagonals through layers (row fixed)
  for r in rng:
    lines.append([(i, r, i) for i in rng])
    lines.append([(i, r, N-1-i) for i in rng])

  # diagonals through layers (column fixed)
  for c in rng:
    lines.append([(i, i, c) for i in rng])
    lines.append([(i, N-1-i, c) for i in rng])

  # 4 main 3D diagonals
  lines.append([(i, i, i) for i in rng])
  lines.append([(i, i, N-1-i) for i in rng])
  lines.append([(i, N-1-i, i) for i in rng])
  lines.append([(N-1-i, i, i) for i in rng])

  return lines


def compute_positional_weights(winning_lines):

  weights = [[[0 for _ in range(BOARD_DIMENSIONS)] for _ in range(BOARD_ROWS)] for _ in range(BOARD_COLS)]

  for line in winning_lines:
    for (x, y, z) in line:
      weights[z][y][x] += 1

  return weights