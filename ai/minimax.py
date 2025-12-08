import numpy as np
from config import maxDepth, PLAYER, AI

def minimax(board, depth, isMaximizing, player = PLAYER, ai = AI):
  if board.checkWin(player):
    return float('-inf')
  if board.checkWin(ai):
    return float('inf')
  if board.isFull() or depth == maxDepth:
        return 0


  b = board.board
  if isMaximizing:
    bestScore = float('-inf')
    for dim in range(b.shape[0]):
      for row in range(b.shape[1]):
        for col in range(b.shape[2]):
          if b[dim][row][col] == 0:
            b[dim][row][col] = ai
            score = minimax(board, depth + 1, False)
            b[dim][row][col] = 0
            bestScore = max(score, bestScore)
    return bestScore
  else:
    bestScore = float('inf')
    for dim in range(b.shape[0]):
      for row in range(b.shape[1]):
        for col in range(b.shape[2]):
          if b[dim][row][col] == 0:
            b[dim][row][col] = player
            score = minimax(board, depth + 1, True)
            b[dim][row][col] = 0
            bestScore = min(score, bestScore)
    return bestScore
  

def bestMove(board):
  b = board.board

  bestScore = float('-inf')
  move = None

  for dim in range(b.shape[0]):
    for row in range(b.shape[1]):
      for col in range(b.shape[2]):
        if b[dim][row][col] == 0:
          b[dim][row][col] = AI
          score = minimax(board, 0, False)
          b[dim][row][col] = 0
          if score > bestScore or move is None:
            bestScore = score
            move = (dim, row, col)

  if move:
    board.markSquare(*move, AI)
    return True
  return False