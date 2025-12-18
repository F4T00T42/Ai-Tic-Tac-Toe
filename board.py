import pygame
import math
import time
import numpy as np
import config
from config import BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS
from ai.minimax import move as minimax_move, minimax, minimaxTBE, minimaxPOS
from ai.alphabeta import move as alphabeta_move, alphabeta, alphabetaTBE, alphabetaPOS
from win_lines import generate_winning_lines
from win_lines import compute_positional_weights


class Board:
  def __init__(self):
    self.board = np.zeros((BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS))
    self.rotation_x = 0.3
    self.rotation_y = 0.5
    self.is_dragging = False
    self.last_mouse_pos = None
    self.current_layer = 1
    self.hovered_cell = None
    self.current_player = config.PLAYER
    self.celebrating = False
    self.ai_engine = "Minimax"
    self.game_started = False
    self.ai_timer = 0.00
    self.ui_rect = []
    self.win_lines = generate_winning_lines(BOARD_DIMENSIONS)
    self.POSITIONAL_WEIGHTS = compute_positional_weights(self.win_lines)
    self.engines = {
    "Minimax": minimax_move(minimax),
    "Threat-based\nHeuristic Eval(MM)": minimax_move(minimaxTBE),
    "   Positional\nHeuristic Eval(MM)": minimax_move(minimaxPOS),
    "Alpha-Beta": alphabeta_move(alphabeta),
    "Threat-based\nHeuristic Eval(AB)": alphabeta_move(alphabetaTBE),
    "   Positional\nHeuristic Eval(AB)": alphabeta_move(alphabetaPOS)
    }




  def isSquareAvailable(self, dim, row, col):
    return self.board[dim][row][col] == 0

  def markSquare(self, dim, row, col, player):
    self.board[dim][row][col] = player

  def isFull(self):
    return not (0 in self.board)

  def reset(self):
    self.board.fill(0)
    self.current_player = config.PLAYER
    self.celebrating = False
    self.game_started = False
    config.BG_COLOR = (170, 100, 200)

  def change_layer(self, direction):
    self.current_layer = max(
      1,
      min(config.BOARD_DIMENSIONS, self.current_layer + direction)
    )
    # print(self.win_lines)

  def choose_ai(self, engine_name):
    self.ai_engine = engine_name

  def checkWin(self, player):
    b = self.board
    for line in self.win_lines:
      if all(b[d, r, c] == player for d, r, c in line):
        return True
    return False

  def ai_move(self):
    start = time.perf_counter()
    self.engines[self.ai_engine](self)
    return time.perf_counter() - start

  # Handles player move on a cell
  def handle_cell_click(self, cell):
    if not cell:
      return

    #To hide the ai list
    # self.game_started = True

    dim, row, col = cell
    if self.isSquareAvailable(dim, row, col):
      self.markSquare(dim, row, col, self.current_player)
      if not self.checkWin(self.current_player) and not self.isFull():
        self.current_player = config.AI
        self.ai_timer = self.ai_move()
        self.current_player = config.PLAYER

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