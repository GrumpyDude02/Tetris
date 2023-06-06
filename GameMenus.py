import pygame, random, Tools.functions as functions
import game_parameters as gp
from GameStates import GameStates
from Tetrominos import Tetrominos
from Tools.Buttons import Buttons
from Premitives.Menu import Menu, Background, TransparentMenu, direction


class MainMenu(Menu):
    def __init__(self, game, backdround: Background = None):
        super().__init__(game, bg=backdround)
        self.buttons = {
            "PLAY": Buttons(
                "PLAY",
                (0.16, 0.1),
                (0.42, 0.35),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "SETTINGS": Buttons(
                "SETTINGS",
                (0.16, 0.1),
                (0.42, 0.50),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "EXIT": Buttons(
                "EXIT",
                (0.16, 0.1),
                (0.42, 0.65),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
        }
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["PLAY"])

        self.buttons["PLAY"].next_buttons = [
            self.buttons["EXIT"],
            None,
            self.buttons["SETTINGS"],
            None,
        ]
        self.buttons["SETTINGS"].next_buttons = [
            self.buttons["PLAY"],
            None,
            self.buttons["EXIT"],
            None,
        ]
        self.buttons["EXIT"].next_buttons = [
            self.buttons["SETTINGS"],
            None,
            self.buttons["PLAY"],
            None,
        ]

    def handle_events(self):
        if self.mouse_mode:
            for key in self.buttons.keys():
                if self.buttons[key].move_cursor(self.cursor):
                    print(self.button_state[key])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            if event.type == pygame.KEYDOWN:
                self.mouse_mode = False
                if event.key == pygame.K_DOWN:
                    self.cursor.move_to(direction["down"])
                if event.key == pygame.K_UP:
                    self.cursor.move_to(direction["up"])
            if event.type == pygame.MOUSEMOTION:
                self.mouse_mode = True

        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["PLAY"]:
                self.set_state(GameStates.Tetris)
            elif b is self.buttons["SETTINGS"]:
                self.set_state(GameStates.in_settings)
            elif b is self.buttons["EXIT"]:
                self.set_state(GameStates.quitting)

    def loop(self):
        dt = 1 / gp.FPS
        Menu.last_spawn_time = -10000
        self.tetrominos = []
        while self.game.state == GameStates.main_menu:
            current_time = pygame.time.get_ticks()
            self.handle_events()
            self.draw(current_time=current_time, dt=dt)
            dt = self.game.clock.tick(gp.FPS) / 1000
            pygame.display.flip()
            if self.background is not None:
                self.background.destroy_tetrominos()


class PauseScreen(TransparentMenu):
    def __init__(self, game):
        super().__init__(game, "PAUSED")
        self.create_blurred_surface()
        # 0.52 0.60 0.32 0.60
        self.buttons = {
            "EXIT": Buttons(
                "EXIT",
                (0.16, 0.1),
                (0.52, 0.60),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "RESUME": Buttons(
                "RESUME",
                (0.16, 0.1),
                (0.32, 0.60),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "RESET": Buttons(
                "RESET",
                (0.16, 0.1),
                (0.42, 0.75),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
        }

    def resize(self):
        super().resize()
        self.create_blurred_surface()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(self.game.last_played)
        if self.buttons["EXIT"].check_input():
            self.set_pending_state(GameStates.main_menu)
            self.set_state(GameStates.resetting)
        elif self.buttons["RESUME"].check_input():
            self.set_state(self.game.last_played)
        elif self.buttons["RESET"].check_input():
            self.set_state(GameStates.resetting)
            self.set_pending_state(self.game.last_played)

    def loop(self, surface):
        blurred_surface = pygame.transform.gaussian_blur(surface, 4, False)
        while self.game.state == GameStates.paused:
            self.handle_events()
            self.draw(blurred_surface)
            pygame.time.Clock().tick(gp.FPS)
            pygame.display.flip()


class SettingsMenu(Menu):
    def __init__(self, game, backdround: Background = None):
        super().__init__(game, bg=backdround)
        self.buttons = {
            "960x540": Buttons(
                "960x540",
                (0.16, 0.1),
                (0.42, 0.15),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "1024x576": Buttons(
                "1024x576",
                (0.16, 0.1),
                (0.42, 0.25),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "1280x720": Buttons(
                "1280x720",
                (0.16, 0.1),
                (0.42, 0.35),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "1366x768": Buttons(
                "1366x768",
                (0.16, 0.1),
                (0.42, 0.45),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "1600x900": Buttons(
                "1600x900",
                (0.16, 0.1),
                (0.42, 0.55),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "1920x1080": Buttons(
                "1920x1080",
                (0.16, 0.1),
                (0.42, 0.65),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "2560x1440": Buttons(
                "2560x1440",
                (0.16, 0.1),
                (0.42, 0.75),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "BACK": Buttons(
                "BACK",
                (0.16, 0.1),
                (0.42, 0.85),
                self.game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
        }

    def handle_events(self):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
        for key, i in zip(self.buttons.keys(), range(0, 7)):
            if self.buttons[key].check_input():
                gp.selected_res = gp.Resolutions[i]
                self.set_state(GameStates.changing_res)
                self.set_pending_state(GameStates.in_settings)
                break
        if self.buttons["BACK"].check_input():
            self.set_state(GameStates.main_menu)

    def loop(self):
        dt = 1 / gp.FPS
        MainMenu.last_spawn_time = 0
        while self.game.state == GameStates.in_settings:
            time = pygame.time.get_ticks()
            self.handle_events()
            self.draw(current_time=time, dt=dt)
            dt = self.game.clock.tick(gp.FPS) / 1000
            pygame.display.flip()


class GameOver(TransparentMenu):
    def __init__(self, game):
        super().__init__(game, "GAME OVER")
        self.create_blurred_surface()
        self.buttons = {
            "EXIT": Buttons(
                "EXIT",
                (0.16, 0.1),
                (0.52, 0.60),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
            "RESET": Buttons(
                "RESET",
                (0.16, 0.1),
                (0.32, 0.60),
                game.main_font,
                5,
                hover_color=gp.BLUE,
                sc_size=(gp.WIDTH, gp.HEIGHT),
            ),
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
        if self.buttons["EXIT"].check_input():
            self.set_pending_state(GameStates.main_menu)
            self.set_state(GameStates.resetting)
        elif self.buttons["RESET"].check_input():
            self.set_state(GameStates.resetting)
            self.set_pending_state(self.game.last_played)

    def loop(self, surface):
        blurred_surface = pygame.transform.gaussian_blur(surface, 4, False)
        while self.game.state == GameStates.game_over:
            self.handle_events()
            self.draw(blurred_surface)
            pygame.time.Clock().tick(gp.FPS)
            pygame.display.flip()
            if self.background is not None:
                self.background.destroy_tetrominos()
