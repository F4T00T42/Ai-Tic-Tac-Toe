import pygame
import math
from utils import *
import config

def draw_layer_selector(surface, board, event=None):
  font_size = int(config.SCREEN_WIDTH * 0.015)
  font = pygame.font.SysFont("arial", font_size, bold=True)

  # Position and size
  w = config.SCREEN_WIDTH * 0.2
  h = config.SCREEN_HEIGHT * 0.06
  x = config.SCREEN_WIDTH * 0.5 - w * 0.5
  y = config.SCREEN_HEIGHT * 0.9
  arrow_w = w * 0.25
  arrow_color = (50, 150, 255)
  bg_color = (30, 30, 30)

  # Background rectangle
  pygame.draw.rect(surface, bg_color, (x, y, w, h), border_radius=8)

  # Draw left arrow
  left_rect = pygame.Rect(x + 5, y + 5, arrow_w, h - 10)
  pygame.draw.rect(surface, arrow_color, left_rect, border_radius=6)
  left_text = font.render("<", True, (255, 255, 255))
  left_text_rect = left_text.get_rect(center=left_rect.center)
  surface.blit(left_text, left_text_rect)

  # Draw right arrow
  right_rect = pygame.Rect(x + w - arrow_w - 5, y + 5, arrow_w, h - 10)
  pygame.draw.rect(surface, arrow_color, right_rect, border_radius=6)
  right_text = font.render(">", True, (255, 255, 255))
  right_text_rect = right_text.get_rect(center=right_rect.center)
  surface.blit(right_text, right_text_rect)

  # Draw current layer
  layer_text = font.render(f"Layer: {board.current_layer}", True, (255, 255, 255))
  layer_text_rect = layer_text.get_rect(center=(x + w // 2, y + h // 2))
  surface.blit(layer_text, layer_text_rect)

  if event and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    mouse_pos = event.pos
    if left_rect.collidepoint(mouse_pos):
      board.current_layer = max(1, board.current_layer - 1)
    elif right_rect.collidepoint(mouse_pos):
      board.current_layer = min(config.BOARD_DIMENSIONS, board.current_layer + 1)


def draw_newGame_button(surface, board):
  font_size = int(config.SCREEN_WIDTH * 0.015)
  font = pygame.font.SysFont("arial", font_size, bold=True)
  w = config.SCREEN_WIDTH * 0.1
  h = config.SCREEN_HEIGHT * 0.06
  x = config.SCREEN_WIDTH * 0.5 - w * 0.5
  y = config.SCREEN_HEIGHT * 0.95
  mouse_pos = pygame.mouse.get_pos()

  # Button color changes on hover
  color = (200, 50, 50) if pygame.Rect(x, y, w, h).collidepoint(mouse_pos) else (255, 80, 80)
  pygame.draw.rect(surface, color, (x, y, w, h), border_radius=8)

  # Button text
  text_surf = font.render("New Game", True, (255, 255, 255))
  text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
  surface.blit(text_surf, text_rect)

  # Handle click
  if pygame.mouse.get_pressed()[0] and pygame.Rect(x, y, w, h).collidepoint(mouse_pos):
    board.reset()


def draw_ai_list(surface, board):
  # Hide the selector if the game has started
  if getattr(board, 'game_started', False):
    return

  font_size = int(config.SCREEN_WIDTH * 0.018)
  title_font = pygame.font.SysFont("arial", font_size, bold=True)
  item_font = pygame.font.SysFont("arial", font_size, bold=True)

  w = config.SCREEN_WIDTH * 0.18
  spacing = config.SCREEN_HEIGHT * 0.015
  x = config.SCREEN_WIDTH - w - config.SCREEN_WIDTH * 0.02
  y = config.SCREEN_HEIGHT * 0.1
  h = config.SCREEN_HEIGHT * 0.06

  engines = ["minimax", "random", "advanced"]

  mouse_pos = pygame.mouse.get_pos()

  # Panel background
  panel_height = len(engines) * (h + spacing) + 50
  panel_rect = pygame.Rect(x - 10, y - 40, w + 20, panel_height)
  pygame.draw.rect(surface, (50, 50, 50), panel_rect, border_radius=14)
  pygame.draw.rect(surface, (255, 255, 255), panel_rect, 2, border_radius=14)

  # Panel title
  title_surf = title_font.render("AI Engines", True, (255, 255, 255))
  title_rect = title_surf.get_rect(center=(panel_rect.centerx, y - 20))
  surface.blit(title_surf, title_rect)

  for i, eng in enumerate(engines):
    rect = pygame.Rect(x, y + i * (h + spacing), w, h)

    base_color = (60, 60, 60)
    hover_color = (100, 100, 220)
    selected_color = (30, 200, 30)

    if eng == board.ai_engine:
      color = selected_color
    elif rect.collidepoint(mouse_pos):
      color = hover_color
    else:
      color = base_color

    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=10)

    text_surf = item_font.render(eng.capitalize(), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

    if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
      board.ai_engine = eng




def draw_circle_on_cell(layer_surf, cell_3d, layer_z, board, alpha=255, radius_ratio=0.18, thickness=6):
  center_x = sum(x for x, y in cell_3d) / 4
  center_y = sum(y for x, y in cell_3d) / 4

  num_points = 20
  radius = config.CELL_SIZE * radius_ratio
  points_2d = []

  for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    px = center_x + math.cos(angle) * radius
    py = center_y + math.sin(angle) * radius
    rx3d, ry3d, rz3d = rotate_point_3d(px, py, layer_z, board.rotation_x, board.rotation_y)
    sx, sy, _, _ = project_3d_to_2d(rx3d, ry3d, rz3d, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
    points_2d.append((sx, sy))

  pygame.draw.polygon(layer_surf, (*config.CIRCLE_COLOR, alpha), points_2d, thickness)

def draw_cross_on_cell(layer_surf, cell_3d, layer_z, board, alpha=255, ratio=0.18, thickness=6):
  # Compute center
  cx = sum(x for x, y in cell_3d) / 4
  cy = sum(y for x, y in cell_3d) / 4

  # Size of cross lines
  size = config.CELL_SIZE * ratio

  # Two diagonal segments in 3D (before rotation)
  segments = [
    ((cx - size, cy - size), (cx + size, cy + size)),
    ((cx + size, cy - size), (cx - size, cy + size)),
  ]

  for (x1, y1), (x2, y2) in segments:
    # Rotate into 3D
    rx1, ry1, rz1 = rotate_point_3d(x1, y1, layer_z, board.rotation_x, board.rotation_y)
    rx2, ry2, rz2 = rotate_point_3d(x2, y2, layer_z, board.rotation_x, board.rotation_y)

    # Project into 2D
    sx1, sy1, _, _ = project_3d_to_2d(rx1, ry1, rz1, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
    sx2, sy2, _, _ = project_3d_to_2d(rx2, ry2, rz2, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

    # Draw the segment
    pygame.draw.line(layer_surf, (*config.CROSS_COLOR, alpha), (sx1, sy1), (sx2, sy2), thickness)

def draw_3d_cube(surface, board):
  mouse_pos = pygame.mouse.get_pos()
  hovered_cell = None
  layers_data = []

  # Prepare all layers
  for layer_idx in range(config.BOARD_DIMENSIONS):
    layer_num = layer_idx + 1
    layer_z = -config.CUBE_SIZE / 2 + (layer_idx + 0.5) * config.LAYER_SPACING

    # Layer corners
    layer_corners = []
    for i in range(4):
      x, y = (-config.CUBE_SIZE/2, -config.CUBE_SIZE/2) if i == 0 else \
            ( config.CUBE_SIZE/2, -config.CUBE_SIZE/2) if i == 1 else \
            ( config.CUBE_SIZE/2,  config.CUBE_SIZE/2) if i == 2 else \
            (-config.CUBE_SIZE/2,  config.CUBE_SIZE/2)
      rx, ry, rz = rotate_point_3d(x, y, layer_z, board.rotation_x, board.rotation_y)
      sx, sy, scale, dz = project_3d_to_2d(rx, ry, rz, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
      layer_corners.append((sx, sy, dz))

    avg_depth = sum(p[2] for p in layer_corners) / 4
    layer_corners_2d = [(p[0], p[1]) for p in layer_corners]

    # Cells in this layer
    cells = []
    cs = config.CELL_SIZE * 0.85
    for row in range(config.BOARD_ROWS):
      for col in range(config.BOARD_COLS):
        cx3d = -config.CUBE_SIZE/2 + (col + 0.5) * config.CELL_SIZE
        cy3d = -config.CUBE_SIZE/2 + (row + 0.5) * config.CELL_SIZE

        corners = []
        corners_3d = []
        for i in range(4):
          px, py = (cx3d - cs/2, cy3d - cs/2) if i == 0 else \
                  (cx3d + cs/2, cy3d - cs/2) if i == 1 else \
                  (cx3d + cs/2, cy3d + cs/2) if i == 2 else \
                  (cx3d - cs/2, cy3d + cs/2)
          rxp, ryp, rzp = rotate_point_3d(px, py, layer_z, board.rotation_x, board.rotation_y)
          sx, sy, _, _ = project_3d_to_2d(rxp, ryp, rzp, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
          corners.append((sx, sy))
          corners_3d.append((px, py))
        cells.append({"poly": corners, "coords": (layer_num - 1, row, col), "poly_3d": corners_3d})

    layers_data.append({
        "depth": avg_depth,
        "layer_corners": layer_corners_2d,
        "cells": cells,
        "layer_number": layer_num,
        "layer_z": layer_z
    })

  # Sort layers back-to-front
  layers_data.sort(key=lambda d: d["depth"], reverse=True)

  # Draw all layers
  for layer in layers_data:
    layer_num = layer["layer_number"]
    layer_z = layer["layer_z"]
    alpha = 255 if layer_num == board.current_layer else int(255 * 0.3)

    layer_surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(layer_surf, (*config.LAYER_COLOR, alpha), layer["layer_corners"])
    pygame.draw.polygon(layer_surf, (*config.CELL_BORDER, alpha), layer["layer_corners"], 2)

    for cell in layer["cells"]:
      poly = cell["poly"]
      ident = cell["coords"]

      # Hover highlight
      if layer_num == board.current_layer and point_in_polygon(mouse_pos, poly):
        hovered_cell = ident
        grown = scale_polygon(poly, 1.1)
        pygame.draw.polygon(layer_surf, (220, 220, 220, 255), grown)
        pygame.draw.polygon(layer_surf, (0, 0, 0, 255), grown, 2)

      # Draw cell background
      pygame.draw.polygon(layer_surf, (*config.CELL_COLOR, 255 if layer_num == board.current_layer else alpha), poly)
      pygame.draw.polygon(layer_surf, (*config.CELL_BORDER, alpha), poly, 1)

      # Draw symbol if this cell is used
      dim, row, col = ident
      value = board.board[dim][row][col]
      if value == 1:  # player
        pygame.draw.polygon(layer_surf, (0, 0, 255, 255 if layer_num == board.current_layer else alpha), poly)
        draw_cross_on_cell(layer_surf, cell["poly_3d"], layer_z, board, alpha=alpha)
        pygame.draw.polygon(layer_surf, (*config.CELL_BORDER, alpha), poly, 1)
      elif value == 2:  # AI
        pygame.draw.polygon(layer_surf, (150, 0, 0, 255 if layer_num == board.current_layer else alpha), poly)
        draw_circle_on_cell(layer_surf, cell["poly_3d"], layer_z, board, alpha=alpha)
        pygame.draw.polygon(layer_surf, (*config.CELL_BORDER, alpha), poly, 1)


    surface.blit(layer_surf, (0, 0))

  return hovered_cell