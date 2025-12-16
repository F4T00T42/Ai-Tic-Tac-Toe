import pygame
import config
from board import Board
from draw import draw_3d_cube, draw_ai_list, draw_newGame_button, draw_layer_selector, draw_ai_timer

pygame.init()

# Screen
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
config.recalc_sizes()
pygame.display.set_caption("AI Cubic Solver")

board = Board()

clock = pygame.time.Clock()


def main():
  global screen

  while True:
    board.ui_rects = []

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
      if event.type == pygame.VIDEORESIZE:
        # Update screen size
        config.SCREEN_WIDTH, config.SCREEN_HEIGHT = event.w, event.h
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
        config.recalc_sizes()

      if board.celebrating:
        if event.type == pygame.MOUSEBUTTONDOWN:
          if not board.handle_ui_click(event.pos):
            board.is_dragging = True
            board.last_mouse_pos = event.pos
        elif event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN):
          board.handle_event(event, board.ui_rects)

      else:
        board.handle_event(event, board.ui_rects)


    screen.fill(config.BG_COLOR)

    if board.celebrating:
      if celebration_winner == config.PLAYER:
        config.BG_COLOR = (30, 180, 30)
        message = "YOU WIN!"
      elif celebration_winner == config.AI:
        config.BG_COLOR = (180, 30, 30)
        message = "AI WINS!"
      else:
        config.BG_COLOR = (130, 130, 130)
        message = "TIE!"

      # Celebration message
      font = pygame.font.SysFont("arial", 48, bold=True)
      text_surf = font.render(message, True, (255, 255, 255))
      rect = text_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 50))
      screen.blit(text_surf, rect)

    else:
      if board.checkWin(config.PLAYER):
        board.celebrating = True
        celebration_winner = config.PLAYER
      elif board.checkWin(config.AI):
        board.celebrating = True
        celebration_winner = config.AI

    board.hovered_cell = draw_3d_cube(screen, board)

    board.ui_rect = []
    board.ui_rect += draw_newGame_button(screen, board)
    board.ui_rect += draw_layer_selector(screen, board)
    board.ui_rect += draw_ai_list(screen, board)
    board.ui_rect += draw_ai_timer(screen, board, board.ai_timer)

    pygame.display.flip()
    clock.tick(60)


if __name__ == "__main__":
    main()