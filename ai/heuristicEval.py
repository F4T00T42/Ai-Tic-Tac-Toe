import numpy as np
from config import BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS, PLAYER, AI

def count_threats(board, player):
  threats = 0

  for line in board.win_lines:
    player_count = 0
    empty_count = 0

    for (x, y, z) in line:
      cell = board.board[z][y][x]
      if cell == player:
        player_count += 1
      elif cell == 0:
        empty_count += 1

    if player_count == BOARD_DIMENSIONS - 1 and empty_count == 1:
      threats += 1

  return threats


def threat_based_eval(board):
  score = 0

  for line in board.win_lines:
    ai = 0
    player = 0

    for (z, y, x) in line:
      cell = board.board[z, y, x]
      if cell == AI:
        ai += 1
      elif cell == PLAYER:
        player += 1

    # blocked
    if ai > 0 and player > 0:
      continue

    # terminal
    if ai == BOARD_DIMENSIONS:
      return np.inf
    if player == BOARD_DIMENSIONS:
      return -np.inf

    # threat-focused scoring
    if ai == BOARD_DIMENSIONS - 1:
      score += 500
    elif ai == BOARD_DIMENSIONS // 2:
      score += 20

    if player == BOARD_DIMENSIONS - 1:
      score -= 800
    elif player == BOARD_DIMENSIONS // 2:
      score -= 30

  # fork detection
  ai_threats = count_threats(board, AI)
  player_threats = count_threats(board, PLAYER)

  if ai_threats >= 2:
    score += 1000
  if player_threats >= 2:
    score -= 1200

  return score


def positional_based_eval(board):
  score = 0

  for z in range(BOARD_DIMENSIONS):
    for y in range(BOARD_ROWS):
      for x in range(BOARD_COLS):
        if board.board[z][y][x] == AI:
          score += board.POSITIONAL_WEIGHTS[z][y][x]
        elif board.board[z][y][x] == PLAYER:
          score -= board.POSITIONAL_WEIGHTS[z][y][x]

  return score