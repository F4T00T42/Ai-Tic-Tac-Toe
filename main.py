import sys
import pygame
import numpy as np

pygame.init()

#COLORS
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)

#SIZES
HEIGHT = 300
WIDTH = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Tic Tac Toe')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))


def Lines(color = WHITE):
  for i in range(1, BOARD_ROWS):
    pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
    pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (HEIGHT, SQUARE_SIZE * i), LINE_WIDTH)


def DrawFigures(color = WHITE):
  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if board[row][col] == 1:
        pygame.draw.line(screen, color, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)), (int(col * SQUARE_SIZE + SQUARE_SIZE), int(row * SQUARE_SIZE + SQUARE_SIZE)))
        pygame.draw.line(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE), int(row * SQUARE_SIZE)), (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE + SQUARE_SIZE)))
      elif board[row][col] == 2:
        pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)