import pygame
import math
from utils import *
from config import *

def draw_circle_on_cell(layer_surf, cell_3d, layer_z, board, alpha=255, radius_ratio=0.25, thickness=7):
  """Draw hollow circle on a cell in 3D space with proper alpha."""
  center_x = sum(x for x, y in cell_3d) / 4
  center_y = sum(y for x, y in cell_3d) / 4

  num_points = 20
  radius = CELL_SIZE * radius_ratio
  points_2d = []

  for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    px = center_x + math.cos(angle) * radius
    py = center_y + math.sin(angle) * radius
    rx3d, ry3d, rz3d = rotate_point_3d(px, py, layer_z, board.rotation_x, board.rotation_y)
    sx, sy, _, _ = project_3d_to_2d(rx3d, ry3d, rz3d, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    points_2d.append((sx, sy))

  pygame.draw.polygon(layer_surf, (*CIRCLE_COLOR, alpha), points_2d, thickness)

def draw_cross_on_cell(layer_surf, cell_3d, layer_z, board, alpha=255, ratio=0.35, thickness=6):
  """Draw a 3D-projected X inside a cell."""
  # Compute center
  cx = sum(x for x, y in cell_3d) / 4
  cy = sum(y for x, y in cell_3d) / 4

  # Size of cross lines
  size = CELL_SIZE * ratio

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
    sx1, sy1, _, _ = project_3d_to_2d(rx1, ry1, rz1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    sx2, sy2, _, _ = project_3d_to_2d(rx2, ry2, rz2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Draw the segment
    pygame.draw.line(layer_surf, (*CROSS_COLOR, alpha), (sx1, sy1), (sx2, sy2), thickness)

def draw_3d_cube(surface, board):
  """Draw the cube with layers, cells, and clicked circles. Returns hovered cell."""
  mouse_pos = pygame.mouse.get_pos()
  hovered_cell = None
  layers_data = []

  # Prepare all layers
  for layer_idx in range(LAYER_COUNT):
    layer_num = layer_idx + 1
    layer_z = -CUBE_SIZE / 2 + (layer_idx + 0.5) * LAYER_SPACING

    # Layer corners
    layer_corners = []
    for i in range(4):
      x, y = (-CUBE_SIZE/2, -CUBE_SIZE/2) if i == 0 else \
            ( CUBE_SIZE/2, -CUBE_SIZE/2) if i == 1 else \
            ( CUBE_SIZE/2,  CUBE_SIZE/2) if i == 2 else \
            (-CUBE_SIZE/2,  CUBE_SIZE/2)
      rx, ry, rz = rotate_point_3d(x, y, layer_z, board.rotation_x, board.rotation_y)
      sx, sy, scale, dz = project_3d_to_2d(rx, ry, rz, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
      layer_corners.append((sx, sy, dz))

    avg_depth = sum(p[2] for p in layer_corners) / 4
    layer_corners_2d = [(p[0], p[1]) for p in layer_corners]

    # Cells in this layer
    cells = []
    cs = CELL_SIZE * 0.7
    for row in range(CELLS_PER_LAYER):
      for col in range(CELLS_PER_LAYER):
        cx3d = -CUBE_SIZE/2 + (col + 0.5) * CELL_SIZE
        cy3d = -CUBE_SIZE/2 + (row + 0.5) * CELL_SIZE

        corners = []
        corners_3d = []
        for i in range(4):
          px, py = (cx3d - cs/2, cy3d - cs/2) if i == 0 else \
                  (cx3d + cs/2, cy3d - cs/2) if i == 1 else \
                  (cx3d + cs/2, cy3d + cs/2) if i == 2 else \
                  (cx3d - cs/2, cy3d + cs/2)
          rxp, ryp, rzp = rotate_point_3d(px, py, layer_z, board.rotation_x, board.rotation_y)
          sx, sy, _, _ = project_3d_to_2d(rxp, ryp, rzp, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
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

    layer_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(layer_surf, (*LAYER_COLOR, alpha), layer["layer_corners"])
    pygame.draw.polygon(layer_surf, (*CELL_BORDER, alpha), layer["layer_corners"], 2)

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
      pygame.draw.polygon(layer_surf, (*CELL_COLOR, 255 if layer_num == board.current_layer else alpha), poly)
      pygame.draw.polygon(layer_surf, (*CELL_BORDER, alpha), poly, 1)

      # Draw symbol if this cell is used
      dim, row, col = ident
      value = board.board[dim][row][col]
      if value == 1:  # player
        draw_cross_on_cell(layer_surf, cell["poly_3d"], layer_z, board, alpha=alpha)
      elif value == 2:  # AI
        draw_circle_on_cell(layer_surf, cell["poly_3d"], layer_z, board, alpha=alpha)


    surface.blit(layer_surf, (0, 0))

  return hovered_cell