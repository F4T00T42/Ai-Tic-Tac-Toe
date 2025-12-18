import numpy as np
from itertools import permutations, product

def all_symmetries(board):
  boards = []

  for perm in permutations([0, 1, 2]):
    b = np.transpose(board, perm)

    for flips in product([False, True], repeat=3):
      c = b
      for axis, f in enumerate(flips):
        if f:
          c = np.flip(c, axis)
      boards.append(c)

  return boards


def canonical(board):
  return min(
    tuple(b.flatten())
    for b in all_symmetries(board)
  )
