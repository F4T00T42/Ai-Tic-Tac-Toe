#SIZES
def recalc_sizes():
  global CUBE_SIZE, CELL_SIZE, LAYER_SPACING

  CUBE_SIZE = (SCREEN_WIDTH + SCREEN_HEIGHT) * 0.18
  CELL_SIZE = CUBE_SIZE / BOARD_ROWS
  LAYER_SPACING = CUBE_SIZE / BOARD_DIMENSIONS


SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1400
BOARD_DIMENSIONS = 4
BOARD_ROWS = 4
BOARD_COLS = 4

#Board Colors
BG_COLOR = (170, 100, 200)
LAYER_COLOR = (50, 50, 50)
CELL_COLOR = (90, 90, 90)
CELL_BORDER = (255, 255, 255)
CELL_PLAYER_COLOR = (0, 0, 255)
CELL_AI_COLOR = (150, 0, 0)
CIRCLE_COLOR = (255, 255, 255)
CROSS_COLOR = (255, 255, 255)

layer_select_arrow_color = (50, 150, 255)
layer_select_bg_color = (30, 30, 30)
new_game_color = (255, 80, 80)
panel_color = (50, 50, 50)
panel_border_color = (255, 255, 255)
ai_items_base_color = (60, 60, 60)
ai_items_hover_color = (100, 100, 220)
ai_items_selected_color = (30, 200, 30)

# Rotation
rotation_x, rotation_y = 0.3, 0.5
is_dragging = False
last_mouse_pos = None

# Layer & cells
current_layer = 1
hovered_cell = None
clicked_cells = set()

#SETTINGS
PLAYER = 1
AI = 2
maxDepth = 1