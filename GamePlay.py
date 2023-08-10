from Premitives.Game import Game, preview_tetrominos_pos
from Tetrominos import Tetrominos
from GameStates import GameStates
import Globals as gp
from copy import deepcopy


class Classic(Game):
    switch_available = True

    def __init__(self, game) -> None:
        super().__init__(game, GameStates.Tetris)
        self.placed_blocks = [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)]
        self.update = self.update_classic
        self.init_queue()
        self.set_shapes()

    def reset_game(self):
        super().reset_game()
        self.init_queue()
        self.set_shapes()

    def set_attributes(self, data):
        self.level = data["Level"]
        self.completed_sets = self.level
        self.increment_level = not data["LockSpeed"]


class PracticeGame(Game):
    def __init__(self, game) -> None:
        super().__init__(game, GameStates.practice_game)
        self.update = self.update_practice


class CustomGame(Game):
    def __init__(self, game):
        super().__init__(game, GameStates.custom_game)

    def set_attributes(self, data):
        if data["Shape"] != "All":
            self.update = self.update_practice
            self.shape = data["Shape"]
            self.preview_tetrominos = [
                Tetrominos(pos, self.shape, self.settings.cell_size * 0.8) for pos in preview_tetrominos_pos
            ]
            self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)
        else:
            self.update = self.update_classic
            self.init_queue()

        self.blocks_to_draw = []
        self.level = data["Level"]
        self.completed_sets = self.level
        self.increment_level = not data["LockSpeed"]
        self.placed_blocks = deepcopy(data["Grid"])
        if self.placed_blocks is None:
            self.placed_blocks = [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)]
            return
        for row in self.placed_blocks:
            for block in row:
                if block is not None:
                    block.width = self.settings.cell_size
                    self.blocks_to_draw.append(block)
