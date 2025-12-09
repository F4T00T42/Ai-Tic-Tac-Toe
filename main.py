import sys
import math
import pygame
from config import *
from board import Board
from game import Game
from draw import draw_3d_cube
from ai.minimax import bestMove

pygame.init()

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Cubic Solver")

board = Board()
game = Game(board)
board.game = game

clock = pygame.time.Clock()


def main():
  running = True

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
        board.handle_event(event)

    screen.fill(BG_COLOR)

    board.hovered_cell = draw_3d_cube(screen, board)

    pygame.display.flip()
    clock.tick(120)

  pygame.quit()

if __name__ == "__main__":
  main()