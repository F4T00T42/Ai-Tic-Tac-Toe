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
HEIGHT = 350
WIDTH = 1400
LINE_WIDTH = 5
BOARD_DIMENSIONS = 4
BOARD_ROWS = 4
BOARD_COLS = 4
SQUARE_WIDTH = WIDTH // 16
SQUARE_HEIGHT = HEIGHT // 4
SQUARE_SIZE = 87
DIMENSION_SIZE = SQUARE_WIDTH * 4
CIRCLE_RADIUS = SQUARE_WIDTH // 4
CIRCLE_WIDTH = 5
CROSS_WIDTH = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Tic Tac Toe')
screen.fill(BLACK)

board = np.zeros((BOARD_DIMENSIONS, BOARD_ROWS, BOARD_COLS))

maxDepth = 1


#BOARD
def drawLines(color = WHITE):
  for i in range(1, BOARD_DIMENSIONS):
    pygame.draw.line(screen, color, (DIMENSION_SIZE * i, 0), (DIMENSION_SIZE * i, HEIGHT), LINE_WIDTH * 3)
  for y in range(BOARD_DIMENSIONS):
    for i in range(1, BOARD_COLS):
      pygame.draw.line(screen, color, (0, SQUARE_HEIGHT * i), (WIDTH, SQUARE_HEIGHT * i), LINE_WIDTH) #HORIZONTAL LINES
      pygame.draw.line(screen, color, (DIMENSION_SIZE * y + SQUARE_WIDTH * i, 0), (DIMENSION_SIZE * y + SQUARE_WIDTH * i, WIDTH), LINE_WIDTH) #VERTICAL LINES

def drawFigures(color = WHITE):
  for dim in range(BOARD_DIMENSIONS):
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if board[dim][row][col] == 1:
          pygame.draw.line(screen, color, (col * SQUARE_SIZE + DIMENSION_SIZE * dim + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + DIMENSION_SIZE * dim + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
          pygame.draw.line(screen, color, (col * SQUARE_SIZE + DIMENSION_SIZE * dim + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + DIMENSION_SIZE * dim + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)
        elif board[dim][row][col] == 2:
          pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + DIMENSION_SIZE * dim + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)


#FUNCTIONS
def isSquareAvailable(dim, row, col):
  return board[dim][row][col] == 0


def markSquare(dim, row, col, player):
  board[dim][row][col] = player


def isBoardFull(checkBoard = board):
  for dim in range(BOARD_DIMENSIONS):
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if checkBoard[dim][row][col] == 0:
          return False
  return True


def checkWin(player, checkBoard = board):
  for dim in range(BOARD_DIMENSIONS):
    for row in range(BOARD_ROWS):
      if np.all(checkBoard[dim][row] == player):
        return True #HORIZONTAL LINE ON SAME DIMENSION

    for col in range(BOARD_COLS):
      if np.all(checkBoard[dim][:, col] == player):
        return True #VERTICAL LINE ON SAME DIMENSION
      
    if all(checkBoard[dim][row][row] == player for row in range(BOARD_ROWS)):
        return True #DIAGONAL LINE ON SAME DIMENSION \
    
    if all(checkBoard[dim][row][3 - row] == player for row in range(BOARD_ROWS)):
        return True #OPPOSITE DIAGONAL LINE ON SAME DIMENSION /

  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if all(checkBoard[dim][row][col] == player for dim in range(BOARD_DIMENSIONS)):
        return True #STRAIGHT LINE THROUGH EVERY DIMENSION

  for row in range(BOARD_ROWS):
    if all(checkBoard[dim][row][dim] == player for dim in range(BOARD_DIMENSIONS)):
      return True #HORIZONTAL LINE THROUGH DIMENSIONS
    if all(checkBoard[dim][row][3 - dim] == player for dim in range(BOARD_DIMENSIONS)):
      return True #OPPOSITE HORIZONTAL LINE THROUGH DIMENSIONS

  for col in range(BOARD_COLS):
    if all(checkBoard[dim][dim][col] == player for dim in range(BOARD_DIMENSIONS)):
      return True #VERTICAL LINE THROUGH DIMENSIONS
    if all(checkBoard[dim][3 - dim][col] == player for dim in range(BOARD_DIMENSIONS)):
      return True #OPPOSITE VERTICAL LINE THROUGH DIMENSIONS

  if all(checkBoard[dim][dim][dim] == player for dim in range(BOARD_DIMENSIONS)):
    return True #DIAGONAL LINE THROUGH DIMENSIONS \
  if all(checkBoard[dim][dim][3 - dim] == player for dim in range(BOARD_DIMENSIONS)):
    return True #DIAGONAL LINE THROUGH DIMENSIONS /

  if all(checkBoard[dim][3 - dim][dim] == player for dim in range(BOARD_DIMENSIONS)):
    return True #DIAGONAL LINE THROUGH DIMENSIONS /
  if all(checkBoard[dim][dim][3 - dim] == player for dim in range(BOARD_DIMENSIONS)):
    return True #DIAGONAL LINE THROUGH DIMENSIONS \

  return False


def minimax(minimaxBoard, depth, isMaximizing):
  if depth == maxDepth:
    return 0
  if checkWin(2, minimaxBoard):
    return float('inf')
  elif checkWin(1, minimaxBoard):
    return float('-inf')
  elif isBoardFull(minimaxBoard):
    return 0


  if isMaximizing:
    bestScore = float('-inf')
    for dim in range(BOARD_DIMENSIONS):
      for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
          if minimaxBoard[dim][row][col] == 0:
            minimaxBoard[dim][row][col] = 2
            score = minimax(minimaxBoard, depth + 1, False)
            minimaxBoard[dim][row][col] = 0
            bestScore = max(score, bestScore)
    return bestScore
  else:
    bestScore = float('inf')
    for dim in range(BOARD_DIMENSIONS):
      for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
          if minimaxBoard[dim][row][col] == 0:
            minimaxBoard[dim][row][col] = 1
            score = minimax(minimaxBoard, depth + 1, True)
            minimaxBoard[dim][row][col] = 0
            bestScore = min(score, bestScore)
    return bestScore
  

def bestMove():
  bestScore = float('-inf')
  move = None

  for dim in range(BOARD_DIMENSIONS):
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        if board[dim][row][col] == 0:
          board[dim][row][col] = 2
          score = minimax(board, 0, False)
          board[dim][row][col] = 0
          if score > bestScore:
            bestScore = score
            move = (dim, row, col)

  if move:
    markSquare(move[0], move[1], move[2], 2)
    return True
  return False


def restartGame():
  screen.fill(BLACK)
  drawLines(WHITE)
  for dim in range(BOARD_DIMENSIONS):
    for row in range(BOARD_ROWS):
      for col in range(BOARD_COLS):
        board[dim][row][col] = 0


drawLines()

player = 1
gameOver = False


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
      x, y = event.pos

      dim = x // DIMENSION_SIZE
      col = (x % DIMENSION_SIZE) // SQUARE_SIZE
      row = y // SQUARE_SIZE


      if isSquareAvailable(dim, row, col):
        markSquare(dim, row, col, player)
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