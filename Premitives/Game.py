import random, pygame, Tools.functions as functions
from Tools.Timer import Timer
import game_parameters as gp
from Tetrominos import Tetrominos
from GameStates import GameStates
from copy import deepcopy

preview_pos = pygame.Vector2(1, 6)


elements_coor = {
    "board": (0.364, 0.01666),
    "next_text": (0.68, 0.01666),
    "hold_text": (0.24, 0.40),
    "line_text": (0.15, 0.26),
    "level_text": (0.15, 0.173),
    "time": (0.15, 0.08),
    "score":(0.15,0.7),
    "preview_surface": (0.68, 0.05),
    
}

preview_tetrominos_pos = [[preview_pos.x, preview_pos.y + i] for i in range(0, 21, 3)]

HOLD_POS = (10, 16)


class GameMode:
    resumed = "resumed"
    paused = "paused"
    initialized = "initialized"
    start_time = 0

    def init_surfaces(self):
        self.board_surface = functions.generate_surf(
            (gp.board_width, gp.board_height), 0
        )
        self.main_surface = functions.generate_surf((gp.WIDTH, gp.HEIGHT), 0)
        self.shadow_surf = functions.generate_surf((12 * gp.cell_size, gp.HEIGHT), 80)
        self.preview_surface = functions.generate_surf((5 * gp.cell_size, gp.HEIGHT), 0)
        self.preview_surface.set_colorkey(gp.BLACK)

    def __init__(self, game, shape: str = None) -> None:
        if shape:
            self.shape = shape
            self.currnet_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, gp.cell_size)
            self.preview_tetrominos = [
                Tetrominos(pos, self.shape, gp.cell_size / 2)
                for pos in preview_tetrominos_pos
            ]
        self.init_surfaces()
        self.game = game
        self.score=0
        self.curr_drop_score=None
        self.held_piece = None
        self.destroy = []
        self.tetrominos = []
        self.score = 0
        self.level = 0
        self.state = GameMode.initialized
        self.cleared_lines = 0
        self.switch_available = False
        self.timer = Timer()
        self.placed_blocks = [
            [None for i in range(gp.playable_num)] for j in range(gp.boardy_cell_number)
        ]

    def reset_game(self):
        functions.reset_board(self.placed_blocks, self.tetrominos)
        self.timer.reset()
        self.level = self.cleared_lines = self.score = 0
        self.held_piece = None

    def set_state(self, new_state, last_mode: str = None):
        self.game.set_state(new_state, last_mode)

    def swap_pieces(self):
        if self.held_piece is None:
            self.current_piece.isHeld = True
            self.held_piece = deepcopy(self.current_piece)
            self.held_piece.set_pos(HOLD_POS)
            self.held_piece.isHeld = False
        elif self.switch_available:
            temp = self.current_piece
            self.current_piece = self.held_piece
            self.current_piece.set_pos(gp.SPAWN_LOCATION)
            self.held_piece = temp
            self.held_piece.set_pos(HOLD_POS)
            self.switch_available = False

    def render_timer(self) -> pygame.Surface:
        int_timer = int(self.timer.time)
        time = self.game.main_font.render(
            f"TIME : {(int_timer//1000)//60:02d}:{(int_timer//1000)%60:02d}:{(int_timer//10)%100:02d}",
            True,
            gp.WHITE,
        )
        return time

    def resize(self):
        self.init_surfaces()
        for line in self.placed_blocks:
            for block in line:
                if block is not None:
                    block.resize()
        self.current_piece.resize()
        for tetrmino in self.tetrominos:
            tetrmino.resize()
        for preview_piece in self.preview_tetrominos:
            preview_piece.resize(gp.cell_size * 0.80)

    def draw(self):
        # self.main_surface.fill(BLACK)
        self.shadow_surf.fill(gp.BLACK)
        self.board_surface.fill(gp.BLACK)
        for line in self.placed_blocks:
            for block in line:
                block.draw(self.board_surface)
        self.current_piece.draw(
            self.board_surface, self.shadow_surf, self.placed_blocks
        )
        functions.draw_grid(self.board_surface, gp.grid, (96, 96, 96))
        self.board_surface.blit(self.shadow_surf, (0, 0))
        self.main_surface.blit(
            self.board_surface,
            (
                ((gp.WIDTH - 12 * gp.cell_size) // 2),
                (gp.HEIGHT - 24 * gp.cell_size) // 2,
            ),
        )

    def update_HUD(self,cleared_lines : int,score_list : list)->None:
        if cleared_lines>0:
            self.score+=score_list[cleared_lines-1]*(self.level+1)
        if self.curr_drop_score is not None:
            if self.curr_drop_score[0]:
                self.score+=self.curr_drop_score[1]*2
            if self.curr_drop_score and not self.curr_drop_score[0]:
                self.score+=1 
        self.cleared_lines+=cleared_lines
    
    def draw_HUD(self, target_lines: str = "\u221E"):
        self.preview_surface.fill(gp.BLACK)
        LINES = self.game.main_font.render(
            f"LINES : {self.cleared_lines} / {target_lines}", True, gp.WHITE
        )
        
        LEVEL = self.game.main_font.render(f"LEVEL : {self.level}", True, gp.WHITE)
        HOLD = self.game.main_font.render("HOLD : ", True, gp.WHITE)
        NEXT = self.game.main_font.render("NEXT : ", True, gp.WHITE)
        SCORE=self.game.main_font.render(f"SCORE : {self.score}", True, gp.WHITE)
        
        for preview in self.preview_tetrominos:
            preview.draw(self.preview_surface, None, self.placed_blocks)
        self.current_piece.draw(
            self.board_surface, self.shadow_surf, self.placed_blocks
        )
        self.main_surface.blit(
            HOLD,
            (
                int(elements_coor["hold_text"][0] * gp.WIDTH),
                int(elements_coor["hold_text"][1] * gp.HEIGHT),
            ),
        )
        self.main_surface.blit(
            NEXT,
            (
                int(elements_coor["next_text"][0] * gp.WIDTH),
                int(elements_coor["next_text"][1] * gp.HEIGHT),
            ),
        )
        self.main_surface.blit(
            self.render_timer(),
            (
                int(elements_coor["time"][0] * gp.WIDTH),
                int(elements_coor["time"][1] * gp.HEIGHT),
            ),
        )
        self.main_surface.blit(
            LEVEL,
            (
                int(elements_coor["level_text"][0] * gp.WIDTH),
                int(elements_coor["level_text"][1] * gp.HEIGHT),
            ),
        )
        self.main_surface.blit(
            LINES,
            (
                int(elements_coor["line_text"][0] * gp.WIDTH),
                int(elements_coor["line_text"][1] * gp.HEIGHT),
            ),
        )
        self.main_surface.blit(
            self.preview_surface,
            (
                int(elements_coor["preview_surface"][0] * gp.WIDTH),
                int(elements_coor["preview_surface"][1] * gp.HEIGHT),
            ),
        )
        self.main_surface.blit(SCORE,(int(elements_coor["score"][0]*gp.WIDTH),int(elements_coor["score"][1]*gp.HEIGHT)))

    def draw_board(self):
        self.current_piece.draw(
            self.board_surface, self.shadow_surf, self.placed_blocks
        )

        functions.draw_grid(self.board_surface, gp.grid, (96, 96, 96))

        self.board_surface.blit(self.shadow_surf, (0, 0))
        self.main_surface.blit(
            self.board_surface,
            (
                int(elements_coor["board"][0] * gp.WIDTH),
                int(elements_coor["board"][1] * gp.HEIGHT),
            ),
        )
