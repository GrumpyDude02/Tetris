from Premitives.Game import GameMode, preview_tetrominos_pos
from Tetrominos import Tetrominos
from GameStates import GameStates
import Globals as gp
import Tools.functions as functions
import pygame, random


class Tetris(GameMode):
    switch_available = True

    def __init__(self, game) -> None:
        super().__init__(game)
        self.index = 0
        self.shapes_list = list(gp.SHAPES.keys())
        # shuffling
        random.shuffle(self.shapes_list)
        self.next_shapes = [shape for shape in self.shapes_list]
        self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.next_shapes.pop(0), gp.cell_size)
        random.shuffle(self.shapes_list)
        self.next_shapes.append(self.shapes_list[self.index])
        self.preview_tetrominos = [
            Tetrominos(pos, shape, gp.cell_size * 0.80) for pos, shape in zip(preview_tetrominos_pos, self.shapes_list)
        ]
        self.index += 1

    def reset_game(self):
        super().reset_game()
        random.shuffle(self.shapes_list)
        self.next_shapes = [shape for shape in self.shapes_list]
        random.shuffle(self.shapes_list)
        self.current_piece = self.update_queue()
        self.state = GameMode.initialized
        self.destroy = []

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            if event.type == pygame.ACTIVEEVENT:
                if event.state == 2:
                    self.state = GameMode.paused
                    self.set_state(GameStates.paused)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(GameStates.paused, GameStates.Tetris)
                    GameMode.timer.pause_timer()
                if event.key == pygame.K_c:
                    self.swap_pieces()
        self.curr_drop_score = self.current_piece.handle_events(self.current_time, events, self.placed_blocks, self.dt)

    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.destroy.remove(tetromino)

    def set_shapes(self):
        for shape, tetromino in zip(self.next_shapes, self.preview_tetrominos):
            tetromino.set_shape(shape)

    def update_queue(self) -> Tetrominos:
        self.next_shapes.append(self.shapes_list[self.index])
        self.index = (self.index + 1) % 7
        if self.index == 0:
            random.shuffle(self.shapes_list)
        shape = self.next_shapes.pop(0)
        return Tetrominos(gp.SPAWN_LOCATION, shape, gp.cell_size)

    def update(self):
        cleared = 0
        wasSet = False
        if self.current_piece.isSet:
            wasSet = True
            cleared = functions.check_line(self.placed_blocks, gp.PLAYABLE_AREA_CELLS)
            self.tetrominos.append(self.current_piece)
            self.current_piece = self.update_queue()
            self.set_shapes()
            self.switch_available = True
        elif self.current_piece.isHeld:
            self.current_piece = self.update_queue()
            self.set_shapes()
            self.switch_available = False
        if self.cleared_lines > (self.level + 1) * 10:
            self.level += 1
        self.update_HUD(wasSet, cleared, gp.LINE_NUMBER_SCORE)
        self.current_piece.update(self.level, self.dt, self.current_time, self.placed_blocks)

    def draw(self):
        self.main_surface.fill(gp.BLACK)
        self.shadow_surf.fill(gp.BLACK)
        self.board_surface.fill(gp.BLACK)
        if self.held_piece:
            self.held_piece.draw(self.main_surface)
        for tetromino in self.tetrominos:
            tetromino.draw(self.board_surface, None, self.placed_blocks)
            if tetromino.destroy:
                self.destroy.append(tetromino)

        self.draw_board()
        self.draw_HUD()

        self.game.screen.blit(self.main_surface, (0, 0))

    def loop(self):
        GameMode.timer.start_timer()
        while self.game.state == GameStates.Tetris:
            if functions.game_over(self.placed_blocks, gp.SPAWN_LOCATION[1]):
                self.set_state(GameStates.game_over, GameStates.Tetris)
            GameMode.timer.update_timer()
            self.dt = min(GameMode.timer.delta_time(), 0.066)
            self.destroy = []
            self.current_time = GameMode.timer.current_time() * 1000
            pygame.display.set_caption("Tetris FPS:" + str(round(self.game.clock.get_fps())))
            self.handle_events()
            self.update()
            self.draw()
            self.game.clock.tick(gp.FPS) / 1000
            pygame.display.flip()
            self.destroy_tetrominos()
