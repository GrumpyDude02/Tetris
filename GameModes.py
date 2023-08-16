from Premitives.Game import Game, preview_tetrominos_pos
from Tetrominos import Tetrominos
from block import block
from GameStates import GameStates
import Globals as gp
from copy import deepcopy
import pygame, random


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
        self.update = self.update_generic


class CustomGame(Game):
    def __init__(self, game):
        super().__init__(game, GameStates.custom_game)

    def set_attributes(self, data):
        print("hh")
        if data["Shape"] != "All":
            self.update = self.update_generic
            self.shape = data["Shape"]
            self.preview_tetrominos = [
                Tetrominos(pos, self.shape, self.settings.cell_size * 0.8) for pos in preview_tetrominos_pos
            ]
            self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)
        else:
            self.update = self.update_classic
            self.init_queue()
            self.set_shapes()

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


class Dig(Game):
    def __init__(self, game):
        Game.__init__(self, game, GameStates.dig_mode)

    def set_attributes(self, data):
        if data["Shape"] == "All":
            self.update = self.update_classic
            self.init_queue()
            self.set_shapes()
        else:
            self.update = self.update_generic
            self.shape = data["Shape"]
            self.preview_tetrominos = [
                Tetrominos(pos, self.shape, self.settings.cell_size * 0.8) for pos in preview_tetrominos_pos
            ]
            self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)

        self.level = data["Level"]
        self.completed_sets = self.level
        self.increment_level = not data["LockSpeed"]

        self.placed_blocks = [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)]
        self.blocks_to_draw = []

        random_block_index = previous_random_index = None
        for i in range(gp.BOARD_Y_CELL_NUMBER - 1, 10, -1):
            for j in range(gp.PLAYABLE_AREA_CELLS):
                self.placed_blocks[i][j] = block(pygame.Vector2(j, i), self.game.settings.cell_size, (180, 180, 180), None)
                self.blocks_to_draw.append(self.placed_blocks[i][j])
            while random_block_index == previous_random_index:
                random_block_index = random.randint(0, gp.PLAYABLE_AREA_CELLS - 1)

            previous_random_index = random_block_index
            self.blocks_to_draw.remove(self.placed_blocks[i][random_block_index])
            self.placed_blocks[i][random_block_index] = None