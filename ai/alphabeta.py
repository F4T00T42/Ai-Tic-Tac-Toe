import numpy as np
from config import maxDepth, PLAYER, AI

def alphabeta(board, depth, isMaximizing, alpha, beta, empty_cells, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return depth - 10
  if board.checkWin(ai):
    return 10 - depth
  if not len(empty_cells) or depth == maxDepth:
    return 0


  if isMaximizing:
    max_eval = -np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = ai
      next_empty = np.delete(empty_cells, i, axis=0)
      eval = alphabeta(board, depth + 1, False, alpha, beta, next_empty)
      board.board[d, r, c] = 0

      max_eval = max(max_eval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break  # ✂ PRUNE
    return max_eval
  else:
    min_eval = np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = player
      next_empty = np.delete(empty_cells, i, axis=0)
      eval = alphabeta(board, depth + 1, True, alpha, beta, next_empty)
      board.board[d, r, c] = 0

      min_eval = min(min_eval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return min_eval

def move(board):
  empty_cells = np.argwhere(board.board == 0)
  bestScore = -np.inf
  move = None

  for i, (d, r, c) in enumerate(empty_cells):
    board.board[d, r, c] = AI
    next_empty = np.delete(empty_cells, i, axis=0)
    score = alphabeta(board, 0, False, float('-inf'), float('inf'), next_empty)
    board.board[d, r, c] = 0

    if score > bestScore or move is None:
      bestScore = score
      move = (d, r, c)

  if move:
    board.markSquare(*move, AI)
    return True
  return False