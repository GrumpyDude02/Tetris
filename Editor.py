import Globals as gp
import json, pygame
from block import block
import Tools.functions as functions


def seriliaze_block(block: block):
    block_dict = {"position": (block.map_pos.x, block.map_pos.y), "color": block.color}
    return block_dict


def deserilize_block(block_dict: dict, block_width):
    map_pos = pygame.math.Vector2(block_dict["position"][0], block_dict["position"][1])
    color = block_dict["color"]
    return block(map_pos, block_width, color, None)


class Editor:
    def __init__(self, settings, board_posistion, size: float = 0.8) -> None:
        self.settings = settings
        self.size = size
        self.position = board_posistion
        self.resize()
        self.loaded_presets = {
            "Custom": [[[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)], []]
        }
        self.placed_blocks_reference = None
        self.drawn_blocks_reference = None

    def resize(self):
        self.board_width = self.settings.board_width * self.size
        self.board_height = self.settings.board_height * self.size
        self.cell_size = self.settings.cell_size * self.size
        self.grid = []
        for i in range(0, gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT):
            for j in range(gp.PLAYABLE_AREA_CELLS + gp.X_BORDER_OFFSET):
                if j == 0 or j == gp.PLAYABLE_AREA_CELLS + gp.X_BORDER_OFFSET - 1:
                    self.grid.append(
                        pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                    )
                elif i == 0 or i == gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT - 1:
                    self.grid.append(
                        pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                    )
        self.board_surface = functions.generate_surf((self.board_width, self.board_height))

    def load_presets(self, name) -> int:
        try:
            with open(f"Assets/Presets/{name}.txt", "r") as f:
                data = json.load(f)
                self.loaded_presets[name] = [[], []]
                for line in data[0]:
                    row = []
                    for value in line:
                        if value is not None:
                            block = deserilize_block(value, self.cell_size)
                            row.append(block)
                            self.loaded_presets[name][1].append(block)
                        else:
                            row.append(None)
                    self.loaded_presets[name][0].append(row)
            return 0
        except FileNotFoundError:
            return -1

    def select_preset(self, name) -> int:
        if self.loaded_presets.get(name) is None:
            if self.load_presets(name) == -1:
                self.placed_blocks_reference = None
                self.drawn_blocks_reference = None
                return -1
        self.placed_blocks_reference = self.loaded_presets[name][0]
        self.drawn_blocks_reference = self.loaded_presets[name][1]
        return 0

    def update(self):
        raw_pos = pygame.mouse.get_pos()
        block_pos = (
            (raw_pos[0] - self.cell_size - self.position[0] * self.settings.width) // self.cell_size,
            (raw_pos[1] + 3 * self.cell_size - self.position[1] * self.settings.height) // self.cell_size,
        )
        place_blocks = self.loaded_presets["Custom"][0]
        drawn_blocks = self.loaded_presets["Custom"][1]
        if 0 <= block_pos[0] < gp.PLAYABLE_AREA_CELLS and 3 < block_pos[1] < gp.BOARD_Y_CELL_NUMBER:
            if place_blocks[int(block_pos[1])][int(block_pos[0])] == None and pygame.mouse.get_pressed()[0]:
                place_blocks[int(block_pos[1])][int(block_pos[0])] = block(
                    pygame.math.Vector2(((block_pos[0]), (block_pos[1]))),
                    self.cell_size,
                    (180, 180, 180),
                    None,
                )
                drawn_blocks.append(place_blocks[int(block_pos[1])][int(block_pos[0])])
            elif pygame.mouse.get_pressed()[2] and place_blocks[int(block_pos[1])][int(block_pos[0])] is not None:
                drawn_blocks.remove(place_blocks[int(block_pos[1])][int(block_pos[0])])
                place_blocks[int(block_pos[1])][int(block_pos[0])] = None

    def save_preset(self, preset_name):
        with open(f"Assets/Presets/{preset_name}.txt", "w") as file:
            json.dump(self.loaded_presets["Custom"], file, default=seriliaze_block)

    def erase(self):
        self.loaded_presets["Custom"] = [
            [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)],
            [],
        ]
        self.placed_blocks_reference = self.loaded_presets["Custom"][0]
        self.drawn_blocks_reference = self.loaded_presets["Custom"][1]

    def draw(self, surface):
        self.board_surface.fill((0, 0, 0))
        functions.draw_borders(self.board_surface, self.grid, (96, 96, 96))
        if self.drawn_blocks_reference is not None:
            for block in self.drawn_blocks_reference:
                block.draw(self.board_surface)
        surface.blit(self.board_surface, (self.position[0] * self.settings.width, self.position[1] * self.settings.height))
