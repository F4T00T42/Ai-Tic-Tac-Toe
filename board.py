import pygame
import math
import numpy as np
import config
from config import BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS
from draw import draw_ai_list, draw_newGame_button, draw_layer_selector
from ai.minimax import move as minimax_move
from ai.alphabeta import move as alphabeta_move
# from ai.heuristic import move as heuristic_move


class Board:
  def __init__(self):
    self.board = np.zeros((BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS))
    self.rotation_x = 0.3
    self.rotation_y = 0.5
    self.is_dragging = False
    self.last_mouse_pos = None
    self.current_layer = 1
    self.hovered_cell = None
    self.current_player = 1  # 1 = human, 2 = AI
    self.celebrating = False
    self.ai_engine = "Alpha-Beta"
    self.game_started = False
    self.ui_rect = []
    self.engines = {
    "Minimax": minimax_move,
    "Alpha-Beta": alphabeta_move,
    # "Heuristic Eval": heuristic_move
    }




  def isSquareAvailable(self, dim, row, col):
    return self.board[dim][row][col] == 0

  def markSquare(self, dim, row, col, player):
    self.board[dim][row][col] = player

  def isFull(self):
    return not (0 in self.board)

  def reset(self):
    self.board.fill(0)
    self.current_player = 1
    self.celebrating = False
    self.game_started = False
    config.BG_COLOR = (170, 100, 200)

  def change_layer(self, direction):
    self.current_layer = max(
      1,
      min(config.BOARD_DIMENSIONS, self.current_layer + direction)
    )

  def choose_ai(self, engine_name):
    self.ai_engine = engine_name

  def checkWin(self, player):
    b = self.board  # shape = (D, R, C)
    D, R, C = b.shape
    d_idx = np.arange(D)

    # 1. Check all rows in each layer
    if np.any(np.all(b == player, axis=2)):
        return True

    # 2. Check all columns in each layer
    if np.any(np.all(b == player, axis=1)):
        return True
    
    # 3. Check diagonals in each layer
    diag1 = np.array([np.diag(b[dim]) for dim in range(D)])
    diag2 = np.array([np.diag(np.fliplr(b[dim])) for dim in range(D)])
    if np.any(np.all(diag1 == player, axis=1)) or np.any(np.all(diag2 == player, axis=1)):
        return True

    # 4. Check verticals (through layers)
    if np.any(np.all(b == player, axis=0)):
        return True

    # 5. 3D diagonals
    if (
        np.all(b[d_idx, d_idx, d_idx] == player) or  # main 3D diagonal
        np.all(b[d_idx, d_idx, R-1-d_idx] == player) or
        np.all(b[d_idx, C-1-d_idx, d_idx] == player) or
        np.all(b[R-1-d_idx, d_idx, d_idx] == player)
    ):
        return True

    # Column diagonals across layers
    col_diag1 = np.all(b[d_idx, d_idx, :] == player, axis=0)        # ascending row
    col_diag2 = np.all(b[d_idx, R-1-d_idx, :] == player, axis=0)    # descending row
    if np.any(col_diag1) or np.any(col_diag2):
        return True

    # Row diagonals across layers
    row_diag1 = np.all(b[d_idx, :, d_idx] == player, axis=0)        # ascending column
    row_diag2 = np.all(b[d_idx, :, C-1-d_idx] == player, axis=0)    # descending column
    if np.any(row_diag1) or np.any(row_diag2):
      return True

    return False

  def ai_move(self):
    self.engines[self.ai_engine](self)

  # Handles player move on a cell
  def handle_cell_click(self, cell):
    if not cell:
      return

    #To hide the ai list
    self.game_started = True

    dim, row, col = cell
    if self.isSquareAvailable(dim, row, col):
      self.markSquare(dim, row, col, 1)  # Human = 1
      if not self.checkWin(1) and not self.isFull():
        self.current_player = 2
        self.ai_move()
        self.current_player = 1

  def handle_ui_click(self, pos):
    for rect, action in self.ui_rect:
      if rect.collidepoint(pos):
        if callable(action):
          action(pos)
        return True
    return False

  # Event handlers
  def handle_event(self, event, ui_rects):
    if event.type == pygame.MOUSEBUTTONDOWN:
      self.handle_mouse_down(event, ui_rects)
    elif event.type == pygame.MOUSEBUTTONUP:
      self.handle_mouse_up(event)
    elif event.type == pygame.MOUSEMOTION:
      self.handle_mouse_motion(event)
    elif event.type == pygame.KEYDOWN:
      self.handle_key_down(event)

  def handle_mouse_down(self, event, ui_rects):
    if event.button != 1:
      return
    else:
      if self.handle_ui_click(event.pos):
        return
      elif self.hovered_cell:
        self.handle_cell_click(self.hovered_cell)
      else:
        self.is_dragging = True
        self.last_mouse_pos = event.pos


  def handle_mouse_up(self, event):
    if event.button == 1:
      self.is_dragging = False
      self.last_mouse_pos = None


  def handle_mouse_motion(self, event):
    if self.is_dragging and self.last_mouse_pos:
      dx = event.pos[0] - self.last_mouse_pos[0]
      dy = event.pos[1] - self.last_mouse_pos[1]
      self.rotation_y += dx * 0.01
      self.rotation_x += dy * 0.01
      self.rotation_x = max(-math.pi / 2, min(math.pi / 2, self.rotation_x))
      self.last_mouse_pos = event.pos

  def handle_key_down(self, event):
    if event.key == pygame.K_LEFT:
      self.current_layer = max(1, self.current_layer - 1)
    elif event.key == pygame.K_RIGHT:
      self.current_layer = min(BOARD_DIMENSIONS, self.current_layer + 1)
    elif event.key == pygame.K_r:
      self.reset()
      self.celebrating = False