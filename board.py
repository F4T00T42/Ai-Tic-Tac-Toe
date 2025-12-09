import pygame
import math
import numpy as np
from config import BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS, LAYER_COUNT

class Board:
  def __init__(self):
    self.board = np.zeros((BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS))
    self.game = None
    self.rotation_x = 0.3
    self.rotation_y = 0.5
    self.is_dragging = False
    self.last_mouse_pos = None
    self.current_layer = 1
    self.hovered_cell = None
    self.clicked_cells = set()
    self.current_player = 1  # 1 = human, 2 = AI

  def isSquareAvailable(self, dim, row, col):
    return self.board[dim][row][col] == 0

  def markSquare(self, dim, row, col, player):
    self.board[dim][row][col] = player

  def isFull(self):
    return not (0 in self.board)

  def reset(self):
    self.board.fill(0)

  def checkWin(self, player):
    board = self.board
    D, R, C = BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS

    for dim in range(D):
      for row in range(R):
        if np.all(board[dim][row] == player):
          return True

      for col in range(C):
        if np.all(board[dim][:, col] == player):
          return True

      if all(board[dim][i][i] == player for i in range(R)):
        return True
      if all(board[dim][i][R - 1 - i] == player for i in range(R)):
        return True

    for row in range(R):
      for col in range(C):
          if all(board[dim][row][col] == player for dim in range(D)):
            return True

    for row in range(R):
      if all(board[dim][row][dim] == player for dim in range(D)):
        return True
      if all(board[dim][row][R - 1 - dim] == player for dim in range(D)):
        return True

    for col in range(C):
      if all(board[dim][dim][col] == player for dim in range(D)):
        return True
      if all(board[dim][D - 1 - dim][col] == player for dim in range(D)):
        return True

    if all(board[dim][dim][dim] == player for dim in range(D)):
      return True
    if all(board[dim][dim][R - 1 - dim] == player for dim in range(D)):
      return True
    if all(board[dim][D - 1 - dim][dim] == player for dim in range(D)):
      return True
    if all(board[dim][dim][R - 1 - dim] == player for dim in range(D)):
      return True

    return False

  def ai_move(self):
    from ai.minimax import bestMove
    bestMove(self)

  # Handles player move on a cell
  def handle_cell_click(self, cell):
    if not cell:
      return
    dim, row, col = cell
    if self.isSquareAvailable(dim, row, col):
      self.markSquare(dim, row, col, 1)  # Human = 1
      if not self.checkWin(1) and not self.isFull():
        self.current_player = 2
        self.ai_move()
        self.current_player = 1

  # Event handlers
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if self.hovered_cell:
          self.handle_cell_click(self.hovered_cell)
        else:
          # Start drag rotation
          self.is_dragging = True
          self.last_mouse_pos = event.pos

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            self.is_dragging = False
            self.last_mouse_pos = None

    elif event.type == pygame.MOUSEMOTION:
      if self.is_dragging and self.last_mouse_pos:
        dx = event.pos[0] - self.last_mouse_pos[0]
        dy = event.pos[1] - self.last_mouse_pos[1]
        self.rotation_y += dx * 0.01
        self.rotation_x += dy * 0.01
        self.rotation_x = max(-math.pi / 2, min(math.pi / 2, self.rotation_x))
        self.last_mouse_pos = event.pos

    elif event.type == pygame.KEYDOWN:
      self.handle_key_down(event)

  def handle_key_down(self, event):
    if event.key == pygame.K_LEFT:
      self.current_layer = max(1, self.current_layer - 1)
    elif event.key == pygame.K_RIGHT:
      self.current_layer = min(LAYER_COUNT, self.current_layer + 1)
    elif event.key == pygame.K_r:
      self.reset()