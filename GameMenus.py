import pygame, random, Tools.functions as functions
import Globals as gp
from GameStates import GameStates
from Tetrominos import Tetrominos
from Tools.Buttons import TextButtons, DefaultTemplate
from Premitives.Menu import Menu, Background, TransparentMenu, direction


class MainMenu(Menu):
    def __init__(self, game, backdround: Background = None):
        super().__init__(game, bg=backdround)
        self.buttons = {
            "PLAY": TextButtons(
                "PLAY",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.35),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "SETTINGS": TextButtons(
                "SETTINGS",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.50),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "EXIT": TextButtons(
                "EXIT",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.65),
                sc_size=(self.settings.width, self.settings.height),
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
            for value in self.buttons.values():
                value.move_cursor(self.cursor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type == pygame.KEYDOWN:
                self.mouse_mode = False
                self.handle_nav(event)
            elif event.type == pygame.MOUSEMOTION:
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
            "EXIT": TextButtons(
                "EXIT",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.52, 0.60),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "RESUME": TextButtons(
                "RESUME",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.32, 0.60),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "RESET": TextButtons(
                "RESET",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.75),
                sc_size=(self.settings.width, self.settings.height),
            ),
        }
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["RESUME"])
        self.buttons["EXIT"].next_buttons = [
            self.buttons["RESET"],
            self.buttons["RESET"],
            self.buttons["RESET"],
            self.buttons["RESUME"],
        ]
        self.buttons["RESUME"].next_buttons = [
            self.buttons["RESET"],
            self.buttons["EXIT"],
            self.buttons["RESET"],
            self.buttons["RESET"],
        ]
        self.buttons["RESET"].next_buttons = [
            self.buttons["RESUME"],
            self.buttons["RESUME"],
            self.buttons["EXIT"],
            self.buttons["EXIT"],
        ]

    def resize(self):
        super().resize()
        self.create_blurred_surface()

    def handle_events(self):
        if self.mouse_mode:
            for item in self.buttons.values():
                item.move_cursor(self.cursor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type == pygame.KEYDOWN:
                self.mouse_mode = False
                self.handle_nav(event)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_mode = True

        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["RESUME"]:
                self.set_state(self.game.last_played)
            elif b is self.buttons["RESET"]:
                self.set_state(GameStates.resetting)
                self.set_pending_state(self.game.last_played)
            elif b is self.buttons["EXIT"]:
                self.set_pending_state(GameStates.main_menu)
                self.set_state(GameStates.resetting)

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

        self.buttons = {}
        y_pos = 0.05
        for resolution in gp.RESOLUTIONS:
            key = "x".join([str(resolution[0]), str(resolution[1])])
            self.buttons[key] = TextButtons(
                key,DefaultTemplate, self.game.main_font,(0.16, 0.1), (0.42, y_pos),  sc_size=(self.settings.width, self.settings.height)
            )
            y_pos += 0.12
        self.buttons["BACK"] = TextButtons(
            "BACK",DefaultTemplate, self.game.main_font,(0.16, 0.1), (0.42, 0.88),  sc_size=(self.settings.width, self.settings.height)
        )

        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["960x540"])
        self.buttons["960x540"].next_buttons = [self.buttons["BACK"], None, self.buttons["1024x576"], None]
        self.buttons["BACK"].next_buttons = [self.buttons["2560x1440"], None, self.buttons["960x540"], None]
        keys = list(self.buttons.keys())
        for i in range(1, len(keys) - 1):
            self.buttons[keys[i]].next_buttons = [self.buttons[keys[i - 1]], None, self.buttons[keys[i + 1]], None]

    def handle_events(self):
        if self.mouse_mode:
            for value in self.buttons.values():
                value.move_cursor(self.cursor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type == pygame.KEYDOWN:
                self.mouse_mode = False
                self.handle_nav(event)
                if event.key == pygame.K_ESCAPE:
                    self.set_state(GameStates.main_menu)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_mode = True

        if self.cursor.button.check_input(self.mouse_mode):
            for key, i in zip(self.buttons.keys(), range(0, 7)):
                if self.cursor.button is self.buttons[key]:
                    self.settings.set_resolution(gp.RESOLUTIONS[i])
                    self.set_state(GameStates.changing_res)
                    self.set_pending_state(GameStates.in_settings)
                    break
            if self.cursor.button is self.buttons["BACK"]:
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
            "EXIT": TextButtons(
                "EXIT",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.52, 0.60),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "RESET": TextButtons(
                "RESET",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.32, 0.60),
                sc_size=(self.settings.width, self.settings.height),
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
