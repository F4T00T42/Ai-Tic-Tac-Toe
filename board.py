import numpy as np
from config import BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS

class Board:
  def __init__(self):
    self.board = np.zeros((BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS))

  def isSquareAvailable(self, dim, row, col):
    return self.board[dim][row][col] == 0

  def markSquare(self, dim, row, col, player):
    self.board[dim][row][col] = player

  def isFull(self):
    return not (0 in self.board)

  def reset(self):
    return self.board.fill(0)

  def checkWin(self, player):
    board = self.board
    D, R, C = BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS

    for dim in range(D):
      for row in range(R):
        if np.all(board[dim][row] == player):
          return True #HORIZONTAL LINE ON SAME DIMENSION

      for col in range(C):
        if np.all(board[dim][:, col] == player):
          return True #VERTICAL LINE ON SAME DIMENSION
        
      if all(board[dim][row][row] == player for row in range(R)):
          return True #DIAGONAL LINE ON SAME DIMENSION \
      
      if all(board[dim][row][3 - row] == player for row in range(R)):
          return True #OPPOSITE DIAGONAL LINE ON SAME DIMENSION /

    for row in range(R):
      for col in range(C):
        if all(board[dim][row][col] == player for dim in range(D)):
          return True #STRAIGHT LINE THROUGH EVERY DIMENSION

    for row in range(R):
      if all(board[dim][row][dim] == player for dim in range(D)):
        return True #HORIZONTAL LINE THROUGH DIMENSIONS
      if all(board[dim][row][3 - dim] == player for dim in range(D)):
        return True #OPPOSITE HORIZONTAL LINE THROUGH DIMENSIONS

    for col in range(C):
      if all(board[dim][dim][col] == player for dim in range(D)):
        return True #VERTICAL LINE THROUGH DIMENSIONS
      if all(board[dim][3 - dim][col] == player for dim in range(D)):
        return True #OPPOSITE VERTICAL LINE THROUGH DIMENSIONS

    if all(board[dim][dim][dim] == player for dim in range(D)):
      return True #DIAGONAL LINE THROUGH DIMENSIONS \
    if all(board[dim][dim][3 - dim] == player for dim in range(D)):
      return True #DIAGONAL LINE THROUGH DIMENSIONS /

    if all(board[dim][3 - dim][dim] == player for dim in range(D)):
      return True #DIAGONAL LINE THROUGH DIMENSIONS /
    if all(board[dim][dim][3 - dim] == player for dim in range(D)):
      return True #DIAGONAL LINE THROUGH DIMENSIONS \

    return False