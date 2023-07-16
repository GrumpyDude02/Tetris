import pygame, Tools.functions as functions
from GameStates import GameStates
from Tools.Timer import Timer
import Globals as gp
from Tetrominos import Tetrominos
from copy import deepcopy

preview_pos = pygame.Vector2(1, 6)


elements_coor = {
    "board": (0.364, 0.01666),
    "next_text": (0.68, 0.01666),
    "hold_text": (0.24, 0.40),
    "line_text": (0.15, 0.26),
    "level_text": (0.15, 0.173),
    "time": (0.15, 0.08),
    "score": (0.15, 0.7),
    "clearance_type": (0.15, 0.76),
    "preview_surface": (0.68, 0.05),
}

preview_tetrominos_pos = [[preview_pos.x, preview_pos.y + i] for i in range(0, 21, 3)]

HOLD_POS = (10, 16)


class GameMode:
    resumed = "resumed"
    paused = "paused"
    initialized = "initialized"
    start_time = 0
    last_time = 0
    timer = Timer()

    def init_surfaces(self) -> None:
        self.board_surface = functions.generate_surf((self.settings.board_width, self.settings.board_height))
        self.main_surface = functions.generate_surf((self.settings.width, self.settings.height))
        self.shadow_surf = functions.generate_surf((12 * self.settings.cell_size, self.settings.height), 80, (0, 0, 0))
        self.preview_surface = functions.generate_surf((5 * self.settings.cell_size, self.settings.height), 0, (0, 0, 0))
        self.clearance_type_surf = functions.generate_surf((int(0.20 * self.settings.width), int(0.3 * self.settings.height)), color_key=(0, 0, 0))
        self.clearance_type_surf.set_alpha(255)

    def __init__(self, game, shape: str = None) -> None:
        if shape:
            self.shape = shape
            self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)
            self.preview_tetrominos = [Tetrominos(pos, self.shape, self.settings.cell_size / 2) for pos in preview_tetrominos_pos]
        self.game = game
        self.settings = self.game.settings
        self.init_surfaces()
        self.score = self.level = self.cleared_lines = self.combo = self.current_time = self.dt = 0
        self.clearance_type = ""
        self.destroy = []
        self.tetrominos = []
        self.switch_available = False
        self.curr_drop_score = None
        self.held_piece = None
        self.last_spin_kick = ""
        self.state = GameMode.initialized
        self.placed_blocks = [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)]

    def reset_game(self) -> None:
        functions.reset_board(self.placed_blocks, self.tetrominos)
        GameMode.timer.reset()
        self.level = self.cleared_lines = self.score = 0
        self.held_piece = None
        self.last_spin_kick = ""

    def set_state(self, new_state: GameStates, last_mode: str = None):
        self.game.set_state(new_state, last_mode)

    def swap_pieces(self) -> None:
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
        int_timer = int(GameMode.timer.time)
        time = self.game.main_font.render(
            f"TIME : {(int_timer//1000)//60:02d}:{(int_timer//1000)%60:02d}:{(int_timer//10)%100:02d}",
            True,
            gp.WHITE,
        )
        return time

    def resize(self) -> None:
        self.init_surfaces()
        for line in self.placed_blocks:
            for block in line:
                if block is not None:
                    block.resize()
        self.current_piece.resize()
        for tetrmino in self.tetrominos:
            tetrmino.resize()
        for preview_piece in self.preview_tetrominos:
            preview_piece.resize(self.settings.cell_size * 0.80)

    def draw(self) -> None:
        self.shadow_surf.fill(gp.BLACK)
        self.board_surface.fill(gp.BLACK)
        for line in self.placed_blocks:
            for block in line:
                block.draw(self.board_surface)
        self.current_piece.draw(self.board_surface, self.shadow_surf, self.placed_blocks)
        functions.draw_grid(self.board_surface, self.game.settings.grid, (96, 96, 96))
        self.board_surface.blit(self.shadow_surf, (0, 0))
        self.main_surface.blit(
            self.board_surface,
            (
                ((self.settings.width - 12 * self.settings.cell_size) // 2),
                (self.settings.height - 24 * self.settings.cell_size) // 2,
            ),
        )

    def update_HUD(self, isSet: bool, cleared_lines: int, score_list: list) -> None:
        if self.curr_drop_score is not None:
            if self.curr_drop_score[0] is True:
                self.score += self.curr_drop_score[1] * 2
            elif self.curr_drop_score[0] is False:
                self.score += 1
            elif self.curr_drop_score[0] is None and self.curr_drop_score[2] != 0:
                if all([self.current_piece.collide(direction, self.placed_blocks) for direction in gp.MOVES.values()]):
                    self.last_spin_kick = f"{self.current_piece.shape}-SPIN\n"
                else:
                    self.last_spin_kick = ""

        if cleared_lines > 0:
            self.combo += 1
            self.clearance_type_surf.set_alpha(255)
            self.score += score_list[cleared_lines - 1] * (self.level + 1)
            match cleared_lines:
                case 1:
                    self.clearance_type = "Single\n"
                case 2:
                    self.clearance_type = "Double\n"
                case 3:
                    self.clearance_type = "Triple\n"
                case 4:
                    self.clearance_type = "Tetris\n"
            self.clearance_type += f"{self.last_spin_kick}"
            self.last_spin_kick = ""

            if self.combo > 1:
                self.clearance_type += f"combo x{self.combo}"
                self.score = (self.level + 1) * 50 * self.combo
        elif isSet:
            self.combo = 0
        self.cleared_lines += cleared_lines

    def draw_HUD(self, target_lines: str = "\u221E") -> None:
        a = self.clearance_type_surf.get_alpha()
        curr_time = GameMode.timer.current_time() * 1000
        if a > 0 and curr_time - GameMode.last_time > 25:
            self.clearance_type_surf.set_alpha(a - 5)
            GameMode.last_time = curr_time

        self.preview_surface.fill(gp.BLACK)
        self.clearance_type_surf.fill(gp.BLACK)
        LINES = self.game.main_font.render(f"LINES : {self.cleared_lines} / {target_lines}", True, gp.WHITE)
        LEVEL = self.game.main_font.render(f"LEVEL : {self.level}", True, gp.WHITE)
        HOLD = self.game.main_font.render("HOLD : ", True, gp.WHITE)
        NEXT = self.game.main_font.render("NEXT : ", True, gp.WHITE)
        SCORE = self.game.main_font.render(f"SCORE : {self.score}", True, gp.WHITE)
        line_clear_type = self.game.main_font.render(self.clearance_type, True, gp.WHITE)
        self.clearance_type_surf.blit(line_clear_type, (0, 0))

        for preview in self.preview_tetrominos:
            preview.draw(self.preview_surface, None, self.placed_blocks)
        self.current_piece.draw(self.board_surface, self.shadow_surf, self.placed_blocks)
        self.main_surface.blit(
            HOLD,
            (
                int(elements_coor["hold_text"][0] * self.settings.width),
                int(elements_coor["hold_text"][1] * self.settings.height),
            ),
        )
        self.main_surface.blit(
            NEXT,
            (
                int(elements_coor["next_text"][0] * self.settings.width),
                int(elements_coor["next_text"][1] * self.settings.height),
            ),
        )
        self.main_surface.blit(
            self.render_timer(),
            (
                int(elements_coor["time"][0] * self.settings.width),
                int(elements_coor["time"][1] * self.settings.height),
            ),
        )
        self.main_surface.blit(
            LEVEL,
            (
                int(elements_coor["level_text"][0] * self.settings.width),
                int(elements_coor["level_text"][1] * self.settings.height),
            ),
        )
        self.main_surface.blit(
            LINES,
            (
                int(elements_coor["line_text"][0] * self.settings.width),
                int(elements_coor["line_text"][1] * self.settings.height),
            ),
        )
        self.main_surface.blit(
            self.preview_surface,
            (
                int(elements_coor["preview_surface"][0] * self.settings.width),
                int(elements_coor["preview_surface"][1] * self.settings.height),
            ),
        )
        self.main_surface.blit(
            SCORE, (int(elements_coor["score"][0] * self.settings.width), int(elements_coor["score"][1] * self.settings.height))
        )
        self.main_surface.blit(
            self.clearance_type_surf,
            (int(elements_coor["clearance_type"][0] * self.settings.width), int(elements_coor["clearance_type"][1] * self.settings.height)),
        )

    def draw_board(self) -> None:
        self.current_piece.draw(self.board_surface, self.shadow_surf, self.placed_blocks)

        functions.draw_grid(self.board_surface, self.game.settings.grid, (96, 96, 96))

        self.board_surface.blit(self.shadow_surf, (0, 0))
        self.main_surface.blit(
            self.board_surface,
            (
                int(elements_coor["board"][0] * self.settings.width),
                int(elements_coor["board"][1] * self.settings.height),
            ),
        )
