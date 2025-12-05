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


def drawLines(color = WHITE):
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


def isSquareAvailable(row, col):
  return board[row][col] == 0


def markSquare(row, col, player):
  if isSquareAvailable(row, col):
    board[row][col] = player


def isBoardFull(checkBoard = board):
  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if checkBoard[row][col] == 0:
        return True
  return False


def checkWin(player, checkBoard = board):
  for row in range(BOARD_ROWS):
    if checkBoard[row][0] == player and checkBoard[row][1] == player and checkBoard[row][2] == player:
      return True

  for col in range(BOARD_COLS):
    if checkBoard[0][col] == player and checkBoard[1][col] == player and checkBoard[2][col] == player:
      return True

  if checkBoard[0][0] == player and checkBoard[1][1] == player and checkBoard[2][2] == player:
    return True

  if checkBoard[0][2] == player and checkBoard[1][1] == player and checkBoard[2][0] == player:
    return True
  
  return False


def minimax(minimaxBoard, depth, isMaximizing):
  if checkWin(2, minimaxBoard):
    return float('inf')
  elif checkWin(1, minimaxBoard):
    return float('-inf')
  elif isBoardFull(minimaxBoard):
    return 0


  if isMaximizing:
    bestScore = -1000

    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if minimaxBoard[row][col] == 0:
          minimaxBoard[row][col] = 2
          score = minimax(minimaxBoard, depth + 1, False)
          minimaxBoard[row][col] = 0
          bestScore = max(score, bestScore)
    return bestScore
  else:
    bestScore = 1000
    
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if minimaxBoard[row][col] == 0:
          minimaxBoard[row][col] = 1
          score = minimax(minimaxBoard, depth + 1, True)
          minimaxBoard[row][col] = 0
          bestScore = min(score, bestScore)
    return bestScore
  

def bestMove():
  bestScore = -1000
  move = (-1, -1)

  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if board[row][col] == 0:
        board[row][col] == 2
        score = minimax(board, 0, False)
        board[row][col] == 0

        if score > bestScore:
          bestScore = score
          move (row, col)

  if move != (-1, -1):
    markSquare(move[0], move[1], 2)
    return True
  return False


def restartGame():
  screen.fill(BLACK)
  drawLines(WHITE)
  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      board[row][col] = 0