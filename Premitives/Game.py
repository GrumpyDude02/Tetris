import pygame, random, Tools.functions as functions
from GameStates import GameStates
from Tools.Timer import Timer
import Globals as gp
from Tetrominos import Tetrominos
import Block
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


class Game:
    start_time = 0
    last_time = 0
    drop_effect_last_tick = 0
    drop_effect_time = 10
    resumed = "resumed"
    paused = "paused"
    initialized = "initialized"
    animation_start_time = 0
    col_index_left = 4
    col_index_right = 5
    clear_animation_time = 75

    # Modes
    Classic = "Classic"
    Custom = "Custom"
    Dig = "Dig"
    Practice = "Practice"

    def init_surfaces(self) -> None:
        self.animate_line_clear = False
        self.board_surface = functions.generate_surf((self.settings.board_width, self.settings.board_height))
        self.drop_effect_surface = functions.generate_surf(
            (self.settings.board_width, self.settings.board_height), 255, (0, 0, 0)
        )
        self.main_surface = functions.generate_surf((self.settings.width, self.settings.height))
        self.shadow_surf = functions.generate_surf((12 * self.settings.cell_size, self.settings.height), 80, (0, 0, 0))
        self.preview_surface = functions.generate_surf((5 * self.settings.cell_size, self.settings.height), 0, (0, 0, 0))
        self.clearance_type_surf = functions.generate_surf(
            (int(0.20 * self.settings.width), int(0.3 * self.settings.height)), color_key=(0, 0, 0)
        )
        self.clearance_type_surf.set_alpha(255)

    def init_queue(self):
        self.index = 1
        # shuffling
        random.shuffle(self.shapes_list)
        self.next_shapes = [shape for shape in self.shapes_list]
        self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.next_shapes.pop(0), self.settings.cell_size)
        random.shuffle(self.shapes_list)
        self.next_shapes.append(self.shapes_list[0])
        self.preview_tetrominos = [
            Tetrominos(pos, shape, self.settings.cell_size * 0.80)
            for pos, shape in zip(preview_tetrominos_pos, self.shapes_list)
        ]

    def __init__(self, game, state, shape: str = None) -> None:
        if shape:
            self.shape = shape
            self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)
            self.preview_tetrominos = [
                Tetrominos(pos, self.shape, self.settings.cell_size / 2) for pos in preview_tetrominos_pos
            ]
        self.game = game
        self.settings = self.game.settings
        self.sound = self.game.sound
        self.init_surfaces()
        self.score = self.level = self.cleared_lines = self.combo = self.current_time = self.dt = 0
        self.timer = Timer()
        self.mode_state = state
        self.shapes_list = list(gp.SHAPES.keys())
        self.last_spin_kick = ""
        self.clearance_type = ""
        self.blit_offset = [0, 0]
        self.destroy = []
        self.tetrominos = []
        self.blocks_to_draw = []
        self.switch_available = False
        self.do_fade = True
        self.increment_level = True
        self.drop_effect = None
        self.completed_sets = 1
        self.preview_tetrominos = self.current_piece = self.curr_drop_score = self.placed_blocks = self.held_piece = None

    def init_mode(self, data):
        self.mode = data["Mode"]
        self.level = data["Level"]
        self.shape = data["Shape"]
        self.completed_sets = self.level + 1
        self.increment_level = not data["LockSpeed"]

        if self.shape == "All":
            self.init_queue()
            self.set_shapes()
        else:
            self.shape = data["Shape"]
            self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)
            self.preview_tetrominos = [
                Tetrominos(pos, self.shape, self.settings.cell_size * 0.8) for pos in preview_tetrominos_pos
            ]

        self.placed_blocks = deepcopy(data["Grid"])
        if self.placed_blocks is None:
            self.placed_blocks = [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)]

        if self.mode is Game.Custom or self.mode is Game.Practice:
            self.blocks_to_draw = []
            for row in self.placed_blocks:
                for block in row:
                    if block is not None:
                        block.width = self.settings.cell_size
                        self.blocks_to_draw.append(block)

        elif self.mode is Game.Dig:
            self.placed_blocks = [[None for i in range(gp.PLAYABLE_AREA_CELLS)] for j in range(gp.BOARD_Y_CELL_NUMBER)]
            random_block_index = previous_random_index = None
            for i in range(gp.BOARD_Y_CELL_NUMBER - 1, 10, -1):
                for j in range(gp.PLAYABLE_AREA_CELLS):
                    self.placed_blocks[i][j] = Block.block(
                        pygame.Vector2(j, i), self.game.settings.cell_size, (180, 180, 180), None
                    )
                    self.blocks_to_draw.append(self.placed_blocks[i][j])
                while random_block_index == previous_random_index:
                    random_block_index = random.randint(0, gp.PLAYABLE_AREA_CELLS - 1)

                previous_random_index = random_block_index
                self.blocks_to_draw.remove(self.placed_blocks[i][random_block_index])
                self.placed_blocks[i][random_block_index] = None

    def reset_game(self) -> None:
        functions.reset_board(self.placed_blocks, self.tetrominos)
        self.timer.reset()
        self.level = self.cleared_lines = self.score = 0
        self.completed_sets = 1
        Game.col_index_left = 4
        Game.col_index_right = 5
        self.animate_line_clear = False
        self.held_piece = None
        self.last_spin_kick = ""
        self.destroy = []

    def set_shapes(self):
        for shape, tetromino in zip(self.next_shapes, self.preview_tetrominos):
            tetromino.set_shape(shape)

    def set_state(self, new_state: GameStates, last_mode: str = None):
        self.game.set_state(new_state, last_mode)

    def swap_pieces(self) -> None:
        if self.held_piece is None:
            self.current_piece.state = Tetrominos.is_held
            self.held_piece = deepcopy(self.current_piece)
            self.held_piece.set_pos(HOLD_POS)
            self.held_piece.reset_color()

        elif self.switch_available:
            temp = self.current_piece
            self.current_piece = self.held_piece
            self.held_piece = temp

            self.current_piece.set_pos(gp.SPAWN_LOCATION)
            self.current_piece.state = Tetrominos.falling

            self.held_piece.set_pos(HOLD_POS)
            self.held_piece.state = Tetrominos.is_held
            self.held_piece.reset_color()

            self.switch_available = False

    def render_timer(self) -> pygame.Surface:
        int_timer = round(self.timer.time)
        time = self.game.main_font.render(
            f"TIME : {(int_timer//1000)//60:02d}:{(int_timer//1000)%60:02d}:{(int_timer//10)%100:02d}",
            True,
            gp.WHITE,
        )
        return time

    def resize(self) -> None:
        self.init_surfaces()
        if self.current_piece is not None:
            self.current_piece.resize(self.settings.cell_size)
            self.current_piece.set_pos(gp.SPAWN_LOCATION)
        for tetrmino in self.tetrominos:
            tetrmino.resize(self.settings.cell_size)
        if self.preview_tetrominos is not None:
            for preview_piece in self.preview_tetrominos:
                preview_piece.resize(self.settings.cell_size * 0.80)

    def update_HUD(self, isSet: bool, cleared_lines: int, score_list: list) -> None:
        if self.current_piece.collision_direction[1] == True:
            if self.current_piece.collision_direction[0] == "right":
                self.blit_offset[0] = 0.25 * self.settings.cell_size
                self.current_piece.collision_direction = [None, None]
            elif self.current_piece.collision_direction[0] == "left":
                self.blit_offset[0] = -0.25 * self.settings.cell_size
                self.current_piece.collision_direction = [None, None]

        if self.curr_drop_score is not None:
            if self.curr_drop_score[0] is True:
                self.score += self.curr_drop_score[1] * 2
                self.blit_offset[1] = 0.4 * self.settings.cell_size

                min_x = min(self.current_piece.blocks, key=lambda x: x.map_pos[0]).map_pos[0]
                min_y = min(self.current_piece.blocks, key=lambda x: x.map_pos[1]).map_pos[1]
                max_x = max(self.current_piece.blocks, key=lambda x: x.map_pos[0]).map_pos[0]
                max_y = max(self.current_piece.blocks, key=lambda x: x.map_pos[1]).map_pos[1]

                self.drop_effect = pygame.Rect(
                    (min_x + 1) * self.settings.cell_size,
                    (min_y - 3 - self.curr_drop_score[1]) * self.settings.cell_size,
                    (max_x - min_x + 1) * self.settings.cell_size,
                    (max_y - (min_y - 1 - self.curr_drop_score[1])) * self.settings.cell_size,
                )
                self.drop_effect_surface.set_alpha(225)

            elif self.curr_drop_score[0] is False:
                self.score += self.curr_drop_score[1]
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
                    self.sound.play("clear")
                case 2:
                    self.clearance_type = "Double\n"
                    self.sound.play("clear1")
                case 3:
                    self.clearance_type = "Triple\n"
                    self.sound.play("clear2")
                case 4:
                    self.clearance_type = "Tetris\n"
                    self.sound.play("clear3")
            self.clearance_type += f"{self.last_spin_kick}"
            self.last_spin_kick = ""

            if self.combo > 1:
                self.clearance_type += f"combo x{self.combo}"
                self.score = (self.level + 1) * 50 * self.combo
        elif isSet:
            self.combo = 0
            self.last_spin_kick = ""
        self.cleared_lines += cleared_lines

    def draw(self):
        self.main_surface.fill(gp.BLACK)
        self.draw_board()
        self.draw_HUD()
        self.game.screen.blit(self.main_surface, (0, 0))

    def draw_HUD(self, target_lines: str = "\u221E") -> None:
        self.preview_surface.fill(gp.BLACK)
        self.clearance_type_surf.fill(gp.BLACK)
        a = self.clearance_type_surf.get_alpha()
        curr_time = self.timer.current_time() * 1000
        if a > 0 and curr_time - Game.last_time > 25:
            self.clearance_type_surf.set_alpha(a - 5)
            Game.last_time = curr_time

        LINES = self.game.main_font.render(f"LINES : {self.cleared_lines} / {target_lines}", True, gp.WHITE)
        LEVEL = self.game.main_font.render(f"LEVEL : {self.level}", True, gp.WHITE)
        HOLD = self.game.main_font.render("HOLD : ", True, gp.WHITE)
        NEXT = self.game.main_font.render("NEXT : ", True, gp.WHITE)
        SCORE = self.game.main_font.render(f"SCORE : {self.score}", True, gp.WHITE)
        line_clear_type = self.game.main_font.render(self.clearance_type, True, gp.WHITE)
        self.clearance_type_surf.blit(line_clear_type, (0, 0))
        if self.held_piece:
            self.held_piece.draw(self.main_surface)
        for preview in self.preview_tetrominos:
            preview.draw(self.preview_surface, None, self.placed_blocks)
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
            SCORE,
            (int(elements_coor["score"][0] * self.settings.width), int(elements_coor["score"][1] * self.settings.height)),
        )
        self.main_surface.blit(
            self.clearance_type_surf,
            (
                int(elements_coor["clearance_type"][0] * self.settings.width),
                int(elements_coor["clearance_type"][1] * self.settings.height),
            ),
        )
        if self.blit_offset[0] > 0:
            self.blit_offset[0] = self.blit_offset[0] - self.dt * 2.5 * self.settings.cell_size
        if self.blit_offset[0] < 0:
            self.blit_offset[0] = self.blit_offset[0] + self.dt * 2.5 * self.settings.cell_size

        if self.blit_offset[1] > 0:
            self.blit_offset[1] -= self.dt * 5 * self.settings.cell_size
        if self.blit_offset[1] < 0:
            self.blit_offset[1] += self.dt * 5 * self.settings.cell_size

    def draw_board(self) -> None:
        self.board_surface.fill(gp.BLACK)
        self.shadow_surf.fill(gp.BLACK)
        self.drop_effect_surface.fill(gp.BLACK)

        b = self.drop_effect_surface.get_alpha()
        curr_time = self.timer.current_time() * 1000
        if b > 0 and curr_time - Game.drop_effect_last_tick > Game.drop_effect_time and self.drop_effect:
            amount_x = int(350 * self.dt)
            amount_y = int(1200 * self.dt)

            self.drop_effect.x += amount_x
            self.drop_effect.width -= 2 * amount_x

            self.drop_effect.y += amount_y
            self.drop_effect.height -= amount_y

            self.drop_effect_surface.set_alpha(b - 5)
            Game.drop_effect_last_tick = curr_time
            pygame.draw.rect(self.drop_effect_surface, (255, 255, 255), self.drop_effect)

        self.current_piece.draw(self.board_surface, self.shadow_surf, self.placed_blocks)
        functions.draw_borders(self.board_surface, self.game.settings.grid, (96, 96, 96))

        for block in self.blocks_to_draw:
            block.draw(self.board_surface)
        for tetromino in self.tetrominos:
            tetromino.draw(self.board_surface, None, self.placed_blocks)
            if tetromino.destroy:
                self.destroy.append(tetromino)

        self.board_surface.blit(self.shadow_surf, (0, 0))
        self.board_surface.blit(self.drop_effect_surface, (0, 0))

        self.main_surface.blit(
            self.board_surface,
            (
                int(elements_coor["board"][0] * self.settings.width) + self.blit_offset[0],
                int(elements_coor["board"][1] * self.settings.height) + self.blit_offset[1],
            ),
        )

    def fade(self, direction, condition):
        last_tick = 0
        current_time = pygame.time.get_ticks()
        while condition(self.game.alpha) and self.do_fade:
            if current_time - last_tick > 10:
                if direction == "in":
                    self.game.alpha -= 20
                elif direction == "out":
                    self.game.alpha += 20
                last_tick = current_time
                self.game.transition_surface.set_alpha(self.game.alpha)
            current_time = pygame.time.get_ticks()
            pygame.display.set_caption("Tetris FPS:" + str(round(self.game.clock.get_fps())))
            self.draw()
            self.game.screen.blit(self.game.transition_surface, (0, 0))
            pygame.display.flip()

    def start_clear_animation(self):
        Game.animation_start_time = self.current_time
        self.animate_line_clear = True

    def clear_lines(self):
        if not self.animate_line_clear:
            return
        if self.current_time - Game.animation_start_time < Game.clear_animation_time:
            return
        for i in self.cleared_rows:
            if self.placed_blocks[i][Game.col_index_left].tetromino is not None:
                self.placed_blocks[i][Game.col_index_left].tetromino.blocks.remove(
                    self.placed_blocks[i][Game.col_index_left]
                )
            elif self.blocks_to_draw is not None:
                self.blocks_to_draw.remove(self.placed_blocks[i][Game.col_index_left])

            if self.placed_blocks[i][Game.col_index_right].tetromino is not None:
                self.placed_blocks[i][Game.col_index_right].tetromino.blocks.remove(
                    self.placed_blocks[i][Game.col_index_right]
                )
            elif self.blocks_to_draw is not None:
                self.blocks_to_draw.remove(self.placed_blocks[i][Game.col_index_right])
            self.placed_blocks[i][Game.col_index_left] = None
            self.placed_blocks[i][Game.col_index_right] = None
        lines = len(self.cleared_rows)
        self.blit_offset[0] += random.uniform(-lines * 2.5, lines * 2.5)
        self.blit_offset[1] += random.uniform(-lines, lines * 2)
        Game.animation_start_time = self.current_time
        Game.col_index_left -= 1
        Game.col_index_right += 1
        if Game.col_index_right == gp.PLAYABLE_AREA_CELLS:
            Game.col_index_right = 5
            Game.col_index_left = 4
            self.animate_line_clear = False
            for i in self.cleared_rows:
                functions.shift_blocks_down(self.placed_blocks, gp.PLAYABLE_AREA_CELLS, i)
            return

    def update(self):
        self.destroy = []
        cleared_rows_num = 0
        wasSet = False

        self.current_time = self.timer.current_time() * 1000
        self.timer.update_dt()
        self.dt = min(self.timer.delta_time(), 0.066)
        self.timer.update_timer()
        self.game.clock.tick(gp.FPS)

        if self.current_piece.state == Tetrominos.is_set:
            wasSet = True
            self.cleared_rows = functions.check_line(self.placed_blocks)
            cleared_rows_num = len(self.cleared_rows)

            if cleared_rows_num > 0:
                self.start_clear_animation()

            self.tetrominos.append(self.current_piece)
            if self.mode is Game.Classic or self.shape == "All":
                self.current_piece = self.update_queue()
                self.set_shapes()
            else:
                self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)
            self.switch_available = True

        elif self.current_piece.state == Tetrominos.is_held:
            if self.mode is Game.Classic or self.shape == "All":
                self.current_piece = self.update_queue()
                self.set_shapes()
            else:
                self.current_piece = Tetrominos(gp.SPAWN_LOCATION, self.shape, self.settings.cell_size)
            self.switch_available = False

        if not self.level > 15 and self.cleared_lines > self.completed_sets * 10 and self.increment_level:
            self.level += 1
            self.completed_sets += 1

        self.clear_lines()
        self.update_HUD(wasSet, cleared_rows_num, gp.LINE_NUMBER_SCORE)
        self.current_piece.update(self.level, self.dt, self.current_time, self.placed_blocks, self.sound)
        for tetromino in self.destroy:
            self.destroy.remove(tetromino)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            if event.type == pygame.ACTIVEEVENT:
                if event.state == 2:
                    self.game.last_played = self.mode_state
                    self.state = Game.paused
                    self.set_state(GameStates.paused)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(GameStates.paused, self.mode_state)
                    self.timer.pause_timer()
                    self.music_paused = True
                if event.key == pygame.K_c:
                    if self.switch_available or self.held_piece is None:
                        self.sound.play("hold")
                    self.swap_pieces()

        if not self.animate_line_clear:
            self.curr_drop_score = self.current_piece.handle_events(
                self.current_time, events, self.placed_blocks, self.dt, self.sound
            )

    def update_queue(self) -> Tetrominos:
        shape = self.next_shapes.pop(0)
        self.next_shapes.append(self.shapes_list[self.index])
        self.index = (self.index + 1) % 7
        if self.index == 0:
            random.shuffle(self.shapes_list)
        return Tetrominos(gp.SPAWN_LOCATION, shape, self.settings.cell_size)

    def loop(self):
        self.music_paused = False
        while self.game.state == self.mode_state:
            if functions.game_over(self.placed_blocks, gp.SPAWN_LOCATION[1]):
                self.set_state(GameStates.game_over, self.mode_state)
            pygame.display.set_caption("Tetris FPS:" + str(round(self.game.clock.get_fps())))
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
