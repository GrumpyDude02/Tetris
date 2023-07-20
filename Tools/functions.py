import random, pygame
import Globals as gp
from block import block


def shift_blocks_down(placed_blocks_ar: list[list[block]], playable_field, cleared_row: int) -> None:
    for row in range(cleared_row - 1, -1, -1):
        for col in range(playable_field):
            block = placed_blocks_ar[row][col]
            if block:
                block.map_pos[1] += 1
                placed_blocks_ar[row + 1][col] = block
                placed_blocks_ar[row][col] = None


def check_line(placed_blocks_ar: list[list[block]], playable_field: int) -> int:
    cleared_lines = 0
    for row, lines in enumerate(placed_blocks_ar):
        if all(item for item in lines):
            cleared_lines += 1
            for item in lines:
                item.tetromino.blocks.remove(item)
                placed_blocks_ar[row][int(item.map_pos[0])] = None
            shift_blocks_down(placed_blocks_ar, playable_field, row)
    return cleared_lines


def game_over(placed_blocks_ar, spawn_column) -> bool:
    if any(block for block in placed_blocks_ar[spawn_column - 1]):
        return True
    if any(block for block in placed_blocks_ar[spawn_column]):
        return True
    return False


def reset_board(placed_blocks: int, tetrominos: int):
    for row in range(len(placed_blocks)):
        for col in range(len(placed_blocks[row])):
            placed_blocks[row][col] = None
    tetrominos.clear()


def mod(m, n) -> int:
    return (m % n + n) % n


def clamp(minimum, maximum, value):
    return max(minimum, min(value, maximum))


def exclude(dictionary, exception: str) -> str:
    temp = [key for key in dictionary.keys() if key != exception]
    return random.choice(temp)


# found on https://www.akeric.com/blog/?p=720
def blurSurf(surface, amt):
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s" % amt)
    scale = 1.0 / float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


def generate_surf(surf_size: tuple, transparency_amount: int = 0, color_key: tuple = None) -> pygame.Surface:
    try:
        surface = pygame.Surface(surf_size, pygame.HWACCEL)
    except pygame.error:
        surface = pygame.Surface(surf_size)
    if color_key is not None:
        surface.set_colorkey(color_key)
    if transparency_amount:
        surface.set_alpha(transparency_amount)
    return surface


def draw_grid(window: pygame.Surface, grid, color) -> None:
    for rect in grid:
        pygame.draw.rect(window, color, rect)


def map_values(value: float, input_range: tuple[float], output_range: tuple[float]):
    return ((value - input_range[0]) / (input_range[1] - input_range[0])) * (
        output_range[1] - output_range[0]
    ) + output_range[0]
