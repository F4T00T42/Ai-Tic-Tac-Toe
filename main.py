import math
import pygame
import config
from board import Board
from game import Game
from draw import draw_3d_cube, draw_ai_list, draw_newGame_button, draw_layer_selector
from ai.minimax import bestMove

pygame.init()

# Screen
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
config.recalc_sizes()
pygame.display.set_caption("AI Cubic Solver")

board = Board()
game = Game(board)
board.game = game

clock = pygame.time.Clock()


def main():
  global screen
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
      
      if event.type == pygame.VIDEORESIZE:
        # Update screen size
        config.SCREEN_WIDTH, config.SCREEN_HEIGHT = event.w, event.h
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
        config.recalc_sizes()

      if not board.celebrating:
        board.handle_event(event)
        screen.fill(config.BG_COLOR)
        board.hovered_cell = draw_3d_cube(screen, board)
        draw_ai_list(screen, board)
        draw_newGame_button(screen, board)
        draw_layer_selector(screen, board, event)

      if board.celebrating:
        if event.type == pygame.MOUSEBUTTONDOWN:
          board.is_dragging = True
          board.last_mouse_pos = event.pos
        elif event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN):
          board.handle_event(event)

    if not board.celebrating:
      if board.checkWin(config.PLAYER):
        board.celebrating = True
        board.celebration_winner = config.PLAYER

      elif board.checkWin(config.AI):
        board.celebrating = True
        board.celebration_winner = config.AI

    if board.celebrating:
      if board.celebration_winner == config.PLAYER:
        bg_color = (30, 180, 30)
        message = "YOU WIN!"
      else:
        bg_color = (180, 30, 30)
        message = "AI WINS!"

      screen.fill(bg_color)
      board.hovered_cell = draw_3d_cube(screen, board)

      # Celebration message
      font = pygame.font.SysFont("arial", 48, bold=True)
      text_surf = font.render(message, True, (255, 255, 255))
      rect = text_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 50))
      screen.blit(text_surf, rect)

      # Instructions
      small_font = pygame.font.SysFont("arial", 24)
      info = small_font.render("Press R to restart", True, (255, 255, 255))
      info_rect = info.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 40))
      screen.blit(info, info_rect)

    pygame.display.flip()
    clock.tick(60)


if __name__ == "__main__":
    main()