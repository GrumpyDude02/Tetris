import Globals as gp
import json, pygame
from block import block
import Tools.functions as functions

elements_coor = {
    "board": (0.364, 0.01666),
}


class Editor:
    def __init__(self, game, settings) -> None:
        self.settings = settings
        self.game = game
        self.place_blocks = [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)]
        self.board_surface = functions.generate_surf((self.settings.board_width, self.settings.board_height))

    def update(self):
        raw_pos = pygame.mouse.get_pos()
        pointed_block = (
            (raw_pos[0] - self.settings.cell_size - elements_coor["board"][0] * self.settings.width)
            // self.settings.cell_size,
            (raw_pos[1] + 5 * self.settings.cell_size - elements_coor["board"][1] * self.settings.height)
            // self.settings.cell_size
            - 2,
        )

        if 0 <= pointed_block[0] < gp.PLAYABLE_AREA_CELLS and 3 < pointed_block[1] < gp.BOARD_Y_CELL_NUMBER:
            if self.place_blocks[int(pointed_block[1])][int(pointed_block[0])] == None and pygame.mouse.get_pressed()[0]:
                self.place_blocks[int(pointed_block[1])][int(pointed_block[0])] = block(
                    pygame.math.Vector2(((pointed_block[0]), (pointed_block[1]))),
                    self.settings.cell_size,
                    (0, 0, 255),
                    None,
                )
            elif pygame.mouse.get_pressed()[2]:
                print("hh")
                self.place_blocks[int(pointed_block[1])][int(pointed_block[0])] = None
                print(self.place_blocks[int(pointed_block[1])][int(pointed_block[0])])

    def draw(self, surface):
        self.board_surface.fill((0, 0, 0))
        functions.draw_borders(self.board_surface, self.settings.grid, (255, 255, 0))
        for i in range(3, gp.BOARD_Y_CELL_NUMBER):
            for j in range(gp.PLAYABLE_AREA_CELLS):
                if self.place_blocks[i][j] is not None:
                    self.place_blocks[i][j].draw(self.board_surface)
        surface.blit(
            self.board_surface,
            (elements_coor["board"][0] * self.settings.width, elements_coor["board"][1] * self.settings.height),
        )
