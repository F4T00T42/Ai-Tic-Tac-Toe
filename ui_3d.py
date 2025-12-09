import pygame
import math

pygame.init()

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cubic Viewer - Layer Transparency + Hollow Circles")

# Colors
BG_COLOR = (20, 20, 20)
LAYER_COLOR = (50, 50, 50)
LAYER_COLOR_SELECTED = (200, 200, 200)
CELL_COLOR = (90, 90, 90)
CELL_BORDER = (255, 255, 255)
CIRCLE_COLOR = (255, 200, 0)

# Cube
CUBE_SIZE = 400
LAYER_COUNT = 4
CELLS_PER_LAYER = 4
CELL_SIZE = CUBE_SIZE / CELLS_PER_LAYER
LAYER_SPACING = CUBE_SIZE / LAYER_COUNT

# Rotation
rotation_x, rotation_y = 0.3, 0.5
is_dragging = False
last_mouse_pos = None

# Layer & cells
current_layer = 1
hovered_cell = None
clicked_cells = set()

clock = pygame.time.Clock()


def project_3d_to_2d(x, y, z, cx, cy):
    distance = 800
    scale = distance / (distance + z)
    return cx + x * scale, cy + y * scale, scale, z


def rotate_point_3d(x, y, z, rx, ry):
    cos_y = math.cos(ry)
    sin_y = math.sin(ry)
    x1 = x * cos_y - z * sin_y
    z1 = x * sin_y + z * cos_y
    cos_x = math.cos(rx)
    sin_x = math.sin(rx)
    y1 = y * cos_x - z1 * sin_x
    z2 = y * sin_x + z1 * cos_x
    return x1, y1, z2


def point_in_polygon(point, poly):
    x, y = point
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-6) + x1):
            inside = not inside
    return inside


def scale_polygon(poly, factor):
    cx = sum(x for x, _ in poly) / len(poly)
    cy = sum(y for _, y in poly) / len(poly)
    return [((x - cx) * factor + cx, (y - cy) * factor + cy) for x, y in poly]


def draw_circle_on_cell(layer_surf, cell_3d, layer_z, cx, cy, rx, ry, alpha=255, radius_ratio=0.25, thickness=3):
    """Draw hollow circle on a cell in 3D space with proper alpha."""
    # Average center of the cell
    center_x = sum(x for x, y in cell_3d) / 4
    center_y = sum(y for x, y in cell_3d) / 4

    num_points = 20
    radius = CELL_SIZE * radius_ratio
    points_2d = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        px = center_x + math.cos(angle) * radius
        py = center_y + math.sin(angle) * radius
        rx3d, ry3d, rz3d = rotate_point_3d(px, py, layer_z, rx, ry)
        sx, sy, _, _ = project_3d_to_2d(rx3d, ry3d, rz3d, cx, cy)
        points_2d.append((sx, sy))
    pygame.draw.polygon(layer_surf, (*CIRCLE_COLOR, alpha), points_2d, thickness)


def draw_3d_cube(surface, center_x, center_y):
    global hovered_cell
    mouse_pos = pygame.mouse.get_pos()
    hovered_cell = None

    layers_data = []

    for layer_idx in range(LAYER_COUNT):
        layer_num = layer_idx + 1
        layer_z = -CUBE_SIZE / 2 + (layer_idx + 0.5) * LAYER_SPACING

        # Layer corners
        layer_corners = []
        for i in range(4):
            if i == 0: x, y = -CUBE_SIZE/2, -CUBE_SIZE/2
            if i == 1: x, y =  CUBE_SIZE/2, -CUBE_SIZE/2
            if i == 2: x, y =  CUBE_SIZE/2,  CUBE_SIZE/2
            if i == 3: x, y = -CUBE_SIZE/2,  CUBE_SIZE/2
            rx, ry, rz = rotate_point_3d(x, y, layer_z, rotation_x, rotation_y)
            sx, sy, scale, dz = project_3d_to_2d(rx, ry, rz, center_x, center_y)
            layer_corners.append((sx, sy, dz))

        avg_depth = sum(p[2] for p in layer_corners) / 4
        layer_corners_2d = [(p[0], p[1]) for p in layer_corners]

        # Cells
        cells = []
        cs = CELL_SIZE * 0.7
        for row in range(CELLS_PER_LAYER):
            for col in range(CELLS_PER_LAYER):
                cx3d = -CUBE_SIZE/2 + (col + 0.5) * CELL_SIZE
                cy3d = -CUBE_SIZE/2 + (row + 0.5) * CELL_SIZE

                corners = []
                corners_3d = []
                for i in range(4):
                    if i == 0: px, py = cx3d - cs/2, cy3d - cs/2
                    if i == 1: px, py = cx3d + cs/2, cy3d - cs/2
                    if i == 2: px, py = cx3d + cs/2, cy3d + cs/2
                    if i == 3: px, py = cx3d - cs/2, cy3d + cs/2
                    rxp, ryp, rzp = rotate_point_3d(px, py, layer_z, rotation_x, rotation_y)
                    sx, sy, _, _ = project_3d_to_2d(rxp, ryp, rzp, center_x, center_y)
                    corners.append((sx, sy))
                    corners_3d.append((px, py))
                cells.append({"poly": corners, "coords": (layer_num, row, col), "poly_3d": corners_3d})

        layers_data.append({
            "depth": avg_depth,
            "layer_corners": layer_corners_2d,
            "cells": cells,
            "layer_number": layer_num,
            "layer_z": layer_z
        })

    # Sort back to front
    layers_data.sort(key=lambda d: d["depth"], reverse=True)

    # Draw layers with alpha
    for layer in layers_data:
        layer_num = layer["layer_number"]
        layer_z = layer["layer_z"]
        alpha = 255 if layer_num == current_layer else int(255*0.2)

        layer_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        pygame.draw.polygon(layer_surf, (*LAYER_COLOR, alpha), layer["layer_corners"])
        pygame.draw.polygon(layer_surf, (*CELL_BORDER, alpha), layer["layer_corners"], 2)

        for cell in layer["cells"]:
            poly = cell["poly"]
            ident = cell["coords"]

            if layer_num == current_layer:
                if point_in_polygon(mouse_pos, poly):
                    hovered_cell = ident
                    grown = scale_polygon(poly, 1.1)
                    pygame.draw.polygon(layer_surf, (220, 220, 220, 255), grown)
                    pygame.draw.polygon(layer_surf, (0, 0, 0, 255), grown, 2)

            # Draw cell background
            pygame.draw.polygon(layer_surf, (*CELL_COLOR, alpha if layer_num != current_layer else 255), poly)
            pygame.draw.polygon(layer_surf, (*CELL_BORDER, alpha), poly, 1)

            # Draw circle if clicked
            if ident in clicked_cells:
                draw_circle_on_cell(layer_surf, cell["poly_3d"], layer_z, center_x, center_y,
                                    rotation_x, rotation_y, alpha=alpha, radius_ratio=0.25, thickness=7)

        surface.blit(layer_surf, (0,0))


def main():
    global rotation_x, rotation_y, is_dragging, last_mouse_pos, current_layer

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hovered_cell is not None:
                        if hovered_cell in clicked_cells:
                            clicked_cells.remove(hovered_cell)
                        else:
                            clicked_cells.add(hovered_cell)
                    else:
                        is_dragging = True
                        last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
                    last_mouse_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if is_dragging and last_mouse_pos:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    rotation_y += dx * 0.01
                    rotation_x += dy * 0.01
                    rotation_x = max(-math.pi/2, min(math.pi/2, rotation_x))
                    last_mouse_pos = event.pos

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_layer = max(1, current_layer - 1)
                elif event.key == pygame.K_RIGHT:
                    current_layer = min(LAYER_COUNT, current_layer + 1)

        screen.fill(BG_COLOR)
        draw_3d_cube(screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()


if __name__ == "__main__":
    main()
