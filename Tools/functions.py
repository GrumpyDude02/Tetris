import random, pygame
import Globals as gp
from Block import block


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


def generate_surf(surf_size: tuple, transparency_amount: int = None, color_key: tuple = None) -> pygame.Surface:
    try:
        surface = pygame.Surface(surf_size, pygame.HWACCEL)
    except pygame.error:
        surface = pygame.Surface(surf_size)
    if color_key is not None:
        surface.set_colorkey(color_key)
    if transparency_amount is not None:
        surface.set_alpha(transparency_amount)
    return surface


def draw_rects(window: pygame.Surface, grid: list[pygame.Rect], color) -> None:
    for rect in grid:
        pygame.draw.rect(window, color, rect)


def map_values(value: float, input_range: tuple[float], output_range: tuple[float]):
    return ((value - input_range[0]) / (input_range[1] - input_range[0])) * (
        output_range[1] - output_range[0]
    ) + output_range[0]
