import sys
import pygame
from config import *
from board import Board
from draw import drawLines, drawFigures
from ai.minimax import bestMove

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Tic Tac Toe')

board = Board()
drawLines(screen)


player = PLAYER
gameOver = False

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
      dim = event.pos[0] // DIMENSION_SIZE
      col = (event.pos[0] % DIMENSION_SIZE) // SQUARE_WIDTH
      row = event.pos[1] // SQUARE_HEIGHT

      if board.isSquareAvailable(dim, row, col):
        board.markSquare(dim, row, col, player)
        if board.checkWin(player):
          gameOver = True
        player = player % 2 + 1

        if not gameOver:
          if bestMove(board):
            if board.checkWin(2):
              gameOver = True
            player = player % 2 +1

        if not gameOver:
          if board.isFull():
            gameOver = True

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r:
        screen.fill(BLACK)
        board.reset()
        drawLines(screen)
        player = 1
        gameOver = False
        continue

  if not gameOver:
    drawFigures(screen, board.board)
  else:
    if board.checkWin(1):
      drawFigures(screen, board.board, GREEN)
      drawLines(screen, GREEN)
    elif board.checkWin(2):
      drawFigures(screen, board.board, RED)
      drawLines(screen, RED)
    else:
      drawFigures(screen, board.board, GRAY)
      drawLines(screen, GRAY)

  pygame.display.update()