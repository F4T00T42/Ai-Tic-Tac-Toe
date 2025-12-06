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
HEIGHT = 400
WIDTH = 400
LINE_WIDTH = 5
BOARD_ROWS = 4
BOARD_COLS = 4
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 4
CIRCLE_WIDTH = 10
CROSS_WIDTH = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Tic Tac Toe')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))


def drawLines(color = WHITE):
  for i in range(1, BOARD_ROWS):
    pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
    pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


def drawFigures(color = WHITE):
  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if board[row][col] == 1:
        pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
        pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)
      elif board[row][col] == 2:
        pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)


def isSquareAvailable(row, col):
  return board[row][col] == 0


def markSquare(row, col, player):
  board[row][col] = player


def isBoardFull(checkBoard = board):
  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if checkBoard[row][col] == 0:
        return False
  return True


def checkWin(player, checkBoard = board):
  for row in range(BOARD_ROWS):
    if checkBoard[row][0] == player and checkBoard[row][1] == player and checkBoard[row][2] == player and checkBoard[row][3] == player:
      return True

  for col in range(BOARD_COLS):
    if checkBoard[0][col] == player and checkBoard[1][col] == player and checkBoard[2][col] == player and checkBoard[3][col] == player:
      return True

  if checkBoard[0][0] == player and checkBoard[1][1] == player and checkBoard[2][2] == player and checkBoard[3][3] == player:
    return True

  if checkBoard[0][3] == player and checkBoard[1][2] == player and checkBoard[2][1] == player and checkBoard[3][0] == player:
    return True

  return False


def minimax(minimaxBoard, depth, isMaximizing):
  if depth == 3:
    return 0
  if checkWin(2, minimaxBoard):
    return float('inf')
  elif checkWin(1, minimaxBoard):
    return float('-inf')
  elif isBoardFull(minimaxBoard):
    return 0


  if isMaximizing:
    bestScore = float('-inf')
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if minimaxBoard[row][col] == 0:
          minimaxBoard[row][col] = 2
          score = minimax(minimaxBoard, depth + 1, False)
          minimaxBoard[row][col] = 0
          bestScore = max(score, bestScore)
    return bestScore
  else:
    bestScore = float('inf')
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if minimaxBoard[row][col] == 0:
          minimaxBoard[row][col] = 1
          score = minimax(minimaxBoard, depth + 1, True)
          minimaxBoard[row][col] = 0
          bestScore = min(score, bestScore)
    return bestScore
  

def bestMove():
  bestScore = float('-inf')
  move = (-1, -1)
  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if board[row][col] == 0:
        board[row][col] = 2
        score = minimax(board, 0, False)
        board[row][col] = 0
        if score > bestScore:
          bestScore = score
          move = (row, col)

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


drawLines()

player = 1
gameOver = False


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
      mouseX = event.pos[0] // SQUARE_SIZE
      mouseY = event.pos[1] // SQUARE_SIZE

      if isSquareAvailable(mouseY, mouseX):
        markSquare(mouseY, mouseX, player)
        if checkWin(player):
          gameOver = True
        player = player % 2 + 1

      if not gameOver:
        if bestMove():
          if checkWin(2):
            gameOver = True
          player = player % 2 +1

      if not gameOver:
        if isBoardFull():
          gameOver = True

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r:
        restartGame()
        gameOver = False
        player = 1

  if not gameOver:
    drawFigures()
  else:
    if checkWin(1):
      drawFigures(GREEN)
      drawLines(GREEN)
    elif checkWin(2):
      drawFigures(RED)
      drawLines(RED)
    else:
      drawFigures(GRAY)
      drawLines(GRAY)

  pygame.display.update()