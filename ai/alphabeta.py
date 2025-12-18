import numpy as np
from config import maxDepth, PLAYER, AI
import ai.heuristicEval as hv
from ai.symmetry import canonical

TT = {}

def move(alphabeta_fn):
  def engine(board):
    empty_cells = np.argwhere(board.board == 0)
    bestScore = -np.inf
    move = None

    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = AI
      next_empty = np.delete(empty_cells, i, axis=0)
      score = alphabeta_fn(board, 0, False, -np.inf, np.inf, next_empty)
      board.board[d, r, c] = 0
      print((d, r, c), score)

      if score > bestScore or move is None:
        bestScore = score
        move = (d, r, c)

    if move:
      board.markSquare(*move, AI)
      return True
    return False
  return engine


def alphabeta(board, depth, isMaximizing, alpha, beta, empty_cells, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return depth - 10
  if board.checkWin(ai):
    return 10 - depth
  if not len(empty_cells) or depth == maxDepth:
    return 0

  key = None
  if depth <= 3:
    key = (canonical(board.board), maxDepth - depth, isMaximizing)
    if key in TT:
      return TT[key]

  if isMaximizing:
    score = -np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = ai
      next_empty = np.delete(empty_cells, i, axis=0)
      score = max(score, alphabeta(board, depth + 1, False, alpha, beta, next_empty))
      board.board[d, r, c] = 0

      alpha = max(alpha, score)
      if beta <= alpha:
        break  # PRUNE
    return score
  else:
    score = np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = player
      next_empty = np.delete(empty_cells, i, axis=0)
      score = min(score, alphabeta(board, depth + 1, True, alpha, beta, next_empty))
      board.board[d, r, c] = 0

      beta = min(beta, score)
      if beta <= alpha:
        break
    return score

def alphabetaPOS(board, depth, isMaximizing, alpha, beta, empty_cells, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return depth - 10
  if board.checkWin(ai):
    return 10 - depth
  if not len(empty_cells) or depth == maxDepth:
    return hv.positional_based_eval(board)

  key = None
  if depth <= 3:
    key = (canonical(board.board), maxDepth - depth, isMaximizing)
    if key in TT:
      return TT[key]

  if isMaximizing:
    score = -np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = ai
      next_empty = np.delete(empty_cells, i, axis=0)
      score = max(score, alphabetaPOS(board, depth + 1, False, alpha, beta, next_empty))
      board.board[d, r, c] = 0

      alpha = max(alpha, score)
      if beta <= alpha:
        break  # PRUNE

    if key is not None:
      TT[key] = score
    return score
  else:
    score = np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = player
      next_empty = np.delete(empty_cells, i, axis=0)
      score = min(score, alphabetaPOS(board, depth + 1, True, alpha, beta, next_empty))
      board.board[d, r, c] = 0

      beta = min(beta, score)
      if beta <= alpha:
        break
    
    if key is not None:
      TT[key] = score
    return score

def alphabetaTBE(board, depth, isMaximizing, alpha, beta, empty_cells, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return depth - 10
  if board.checkWin(ai):
    return 10 - depth
  if not len(empty_cells) or depth == maxDepth:
    return hv.threat_based_eval(board)

  key = None
  if depth <= 3:
    key = (canonical(board.board), maxDepth - depth, isMaximizing)
    if key in TT:
      return TT[key]

  if isMaximizing:
    score = -np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = ai
      next_empty = np.delete(empty_cells, i, axis=0)
      score = max(score, alphabetaTBE(board, depth + 1, False, alpha, beta, next_empty))
      board.board[d, r, c] = 0

      alpha = max(alpha, score)
      if beta <= alpha:
        break  # PRUNE

    if key is not None:
      TT[key] = score
    return score
  else:
    score = np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = player
      next_empty = np.delete(empty_cells, i, axis=0)
      score = min(score, alphabetaTBE(board, depth + 1, True, alpha, beta, next_empty))
      board.board[d, r, c] = 0

      beta = min(beta, score)
      if beta <= alpha:
        break

    if key is not None:
      TT[key] = score
    return score