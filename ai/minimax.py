import numpy as np
from config import maxDepth, PLAYER, AI
import ai.heuristicEval as hv

def move(minimax_fn):
  def engine(board):
    empty_cells = np.argwhere(board.board == 0)
    bestScore = -np.inf
    move = None

    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = AI
      next_empty = np.delete(empty_cells, i, axis=0)
      score = minimax_fn(board, 0, False, next_empty)
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


def minimax(board, depth, isMaximizing, empty_cells, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return -np.inf + depth
  if board.checkWin(ai):
    return np.inf - depth
  if board.isFull() or depth == maxDepth:
        return 0


  if isMaximizing:
    score = -np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = ai
      next_empty = np.delete(empty_cells, i, axis=0)
      score = max(score, minimax(board, depth + 1, False, next_empty))
      board.board[d, r, c] = 0
    return score
  else:
    score = np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = player
      next_empty = np.delete(empty_cells, i, axis=0)
      score = min(score, minimax(board, depth + 1, True, next_empty))
      board.board[d, r, c] = 0
    return score

def minimaxPOS(board, depth, isMaximizing, empty_cells, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return -np.inf + depth
  if board.checkWin(ai):
    return np.inf - depth
  if board.isFull() or depth == maxDepth:
        return hv.positional_based_eval(board)


  if isMaximizing:
    score = -np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = ai
      next_empty = np.delete(empty_cells, i, axis=0)
      score = max(score, minimaxPOS(board, depth + 1, False, next_empty))
      board.board[d, r, c] = 0
    return score
  else:
    score = np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = player
      next_empty = np.delete(empty_cells, i, axis=0)
      score = min(score, minimaxPOS(board, depth + 1, True, next_empty))
      board.board[d, r, c] = 0
    return score

def minimaxTBE(board, depth, isMaximizing, empty_cells, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return -np.inf + depth
  if board.checkWin(ai):
    return np.inf - depth
  if board.isFull() or depth == maxDepth:
        return hv.threat_based_eval(board)


  if isMaximizing:
    score = -np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = ai
      next_empty = np.delete(empty_cells, i, axis=0)
      score = max(score, minimaxTBE(board, depth + 1, False, next_empty))
      board.board[d, r, c] = 0
    return score
  else:
    score = np.inf
    for i, (d, r, c) in enumerate(empty_cells):
      board.board[d, r, c] = player
      next_empty = np.delete(empty_cells, i, axis=0)
      score = min(score, minimaxTBE(board, depth + 1, True, next_empty))
      board.board[d, r, c] = 0
    return score