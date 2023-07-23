import pygame
from pygame.math import Vector2 as v

RESOLUTIONS = [(960, 540), (1024, 576), (1280, 720), (1366, 768), (1600, 900), (1920, 1080), (2560, 1440)]
BASE_RESOLUTION = RESOLUTIONS[0]
WIDTH = BASE_RESOLUTION[0]
HEIGHT = BASE_RESOLUTION[1]
BASE_FONT_SIZE = 22
BASE_CELL_SIZE = 22
FPS = 30
GAME_SPEED = 60
BOARD_SHIFT = 2
Y_BORDER_OFFSET = 2
X_BORDER_OFFSET = 2
PLAYABLE_AREA_CELLS = 10
BOARD_Y_CELL_NUMBER = 22 + Y_BORDER_OFFSET + BOARD_SHIFT
BOARD_X_CELL_NUMBER = BASE_RESOLUTION[0] // BASE_CELL_SIZE
PLACED_BLOCKS = [[None for i in range(10)] for j in range(BOARD_Y_CELL_NUMBER)]

MOVE_DELAY = 100
SPAWN_LOCATION = [5, 3]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GAME_SPEED = 60
CHOSEN_LEVEL = 1

SHAPES = {
    "T": [[v(0, 0), v(-1, 0), v(0, -1), v(1, 0)], (255, 68, 255)],
    "Z": [[v(0, 0), v(-1, -1), v(0, -1), v(1, 0)], (255, 0, 0)],
    "S": [[v(0, 0), v(1, -1), v(0, -1), v(-1, 0)], (0, 255, 0)],
    "L": [[v(0, 0), v(-1, 0), v(1, 0), v(1, -1)], (255, 129, 0)],
    "I": [[v(0, 0), v(-1, 0), v(1, 0), v(2, 0)], (0, 255, 255)],
    "J": [[v(0, 0), v(-1, -1), v(-1, 0), v(1, 0)], (0, 0, 255)],
    "O": [[v(0, 0), v(0, -1), v(1, 0), v(1, -1)], (255, 255, 0)],
}

OFFSETS_JLZST = (
    (v(0, 0), v(0, 0), v(0, 0), v(0, 0), v(0, 0)),
    (v(0, 0), v(1, 0), v(1, 1), v(0, -2), v(1, -2)),
    (v(0, 0), v(0, 0), v(0, 0), v(0, 0), v(0, 0)),
    (v(0, 0), v(-1, 0), v(-1, 1), v(0, -2), v(-1, -2)),
)

OFFSETS_I = [
    (v(0, 0), v(-1, 0), v(2, 0), v(-1, 0), v(2, 0)),
    (v(-1, 0), v(0, 0), v(0, 0), v(0, 1), v(0, 2)),
    (v(-1, -1), v(1, -1), v(-2, -1), v(1, 0), v(-2, 0)),
    (v(0, -1), v(0, -1), v(0, -1), v(0, -1), v(0, -2)),
]

MOVES = {"left": v(-1, 0), "right": v(1, 0), "down": v(0, 1)}


LEVEL_SPEED = [
    0.01667,
    0.021017,
    0.026977,
    0.035256,
    0.04693,
    0.06361,
    0.0879,
    0.1236,
    0.1775,
    0.2598,
    0.388,
    0.59,
    0.92,
    1.42,
    2.36,
]
LINE_NUMBER_SCORE = [100, 300, 500, 800]

# ------------------------------------------------------------------------------------------------------------
selected_res = BASE_RESOLUTION

cell_size = BASE_CELL_SIZE

board_width = 12 * BASE_CELL_SIZE
board_height = (BOARD_Y_CELL_NUMBER - BOARD_SHIFT) * BASE_CELL_SIZE


# -------------------------------------------------------------------------------------------------------------


def change_display_val(selected_res) -> float:
    global WIDTH, HEIGHT, board_width, board_height, cell_size, grid
    WIDTH = selected_res[0]
    HEIGHT = selected_res[1]
    scale_factor_y = HEIGHT / BASE_RESOLUTION[1]
    cell_size = round(BASE_CELL_SIZE * scale_factor_y)
    board_width = 12 * cell_size
    board_height = (BOARD_Y_CELL_NUMBER - BOARD_SHIFT) * cell_size
    grid = []
    for i in range(0, BOARD_Y_CELL_NUMBER - BOARD_SHIFT):
        for j in range(PLAYABLE_AREA_CELLS + X_BORDER_OFFSET):
            if j == 0 or j == PLAYABLE_AREA_CELLS + X_BORDER_OFFSET - 1:
                grid.append(pygame.Rect(j * cell_size, i * cell_size, cell_size - 1, cell_size - 1))
            elif i == 0 or i == BOARD_Y_CELL_NUMBER - BOARD_SHIFT - 1:
                grid.append(pygame.Rect(j * cell_size, i * cell_size, cell_size - 1, cell_size - 1))

    return scale_factor_y
