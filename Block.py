import pygame
from pygame.math import Vector2 as v
import Globals as gp

# useless comment


class block:
    def __init__(self, pos: pygame.Vector2, cell_size: int, color: pygame.color, tetromino, block_spacing: int = 1) -> None:
        self.spacing = block_spacing
        self.map_pos = v(pos[0], pos[1])
        self.width = cell_size
        self.sc_pos = self.map_pos * cell_size
        self.color = color
        self.tetromino = tetromino

    def update(self) -> None:
        self.map_pos[1] += 1

    def move(self, direction: pygame.Vector2) -> None:
        self.map_pos += direction

    def draw(self, window: pygame.Surface) -> None:
        width = int(self.width * 0.12)
        self.sc_pos = v((self.map_pos[0] + 1) * self.width, (self.map_pos[1] - gp.Y_BORDER_OFFSET - 1) * self.width)
        pygame.draw.rect(
            window,
            (max(self.color[0] - 40, 0), max(self.color[1] - 40, 0), max(self.color[2] - 40, 0)),
            pygame.Rect(self.sc_pos[0], self.sc_pos[1], self.width - self.spacing, self.width - self.spacing),
            width=width,
        )
        pygame.draw.rect(
            window,
            self.color,
            pygame.Rect(
                self.sc_pos[0] + width,
                self.sc_pos[1] + width,
                self.width - self.spacing - width * 2,
                self.width - self.spacing - width * 2,
            ),
        )

    def draw_highlight(self, window):
        width = int(self.width * 0.12)
        self.sc_pos = v((self.map_pos[0] + 1) * self.width, (self.map_pos[1] - gp.Y_BORDER_OFFSET - 1) * self.width)
        if self.map_pos[1] > gp.Y_BORDER_OFFSET + 1:
            pygame.draw.rect(
                window,
                (255, 255, 255),
                pygame.Rect(self.sc_pos[0] - 1, self.sc_pos[1] - 1, self.width + 1, self.width + 1),
                width=width,
            )
        pygame.draw.rect(
            window,
            (max(self.color[0] - 40, 0), max(self.color[1] - 40, 0), max(self.color[2] - 40, 0)),
            pygame.Rect(self.sc_pos[0], self.sc_pos[1], self.width - self.spacing, self.width - self.spacing),
            width=width,
        )
        pygame.draw.rect(
            window,
            self.color,
            pygame.Rect(
                self.sc_pos[0] + width,
                self.sc_pos[1] + width,
                self.width - self.spacing - width * 2,
                self.width - self.spacing - width * 2,
            ),
        )

    def overlap(self, pos, placed_blocks: list[list]):
        return bool(placed_blocks[int(pos.y)][int(pos.x)])

    def in_bounds(self, pos):
        return (0 <= pos.x < gp.PLAYABLE_AREA_CELLS) and pos.y < gp.BOARD_Y_CELL_NUMBER

    def collide(self, pos: pygame.Vector2, placed_blocks: list[list]) -> bool:
        if self.in_bounds(pos) and not self.overlap(pos, placed_blocks):
            return False
        return True

    def resize(self, block_size: int = None):
        if block_size is None:
            self.width = gp.cell_size
        else:
            self.width = block_size
