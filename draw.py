import pygame
from config import *

#BOARD
def drawLines(screen, color = WHITE):
  for i in range(1, BOARD_DIMENSIONS):
    pygame.draw.line(screen, color, (DIMENSION_SIZE * i, 0), (DIMENSION_SIZE * i, HEIGHT), LINE_WIDTH * 3)
  for y in range(BOARD_DIMENSIONS):
    for i in range(1, BOARD_COLS):
      pygame.draw.line(screen, color, (0, SQUARE_HEIGHT * i), (WIDTH, SQUARE_HEIGHT * i), LINE_WIDTH) #HORIZONTAL LINES
      pygame.draw.line(screen, color, (DIMENSION_SIZE * y + SQUARE_WIDTH * i, 0), (DIMENSION_SIZE * y + SQUARE_WIDTH * i, WIDTH), LINE_WIDTH) #VERTICAL LINES

def drawFigures(screen, board, color = WHITE):
  for dim in range(BOARD_DIMENSIONS):
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if board[dim][row][col] == 1:
          pygame.draw.line(screen, color, (col * SQUARE_SIZE + DIMENSION_SIZE * dim + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + DIMENSION_SIZE * dim + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
          pygame.draw.line(screen, color, (col * SQUARE_SIZE + DIMENSION_SIZE * dim + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + DIMENSION_SIZE * dim + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)
        elif board[dim][row][col] == 2:
          pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + DIMENSION_SIZE * dim + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
