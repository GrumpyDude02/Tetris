import pygame, Tools.functions as functions
import Globals as gp
from GameStates import GameStates
from Tetrominos import Tetrominos
from Tools.Buttons import TextButtons, DefaultTemplate
from Premitives.Menu import Menu, Background, TransparentMenu, direction
from Tools.Slider import Slider
from Tools.Carousel import Carousel


class MainMenu(Menu):
    def __init__(self, game, state, backdround: Background = None):
        super().__init__(game, state, bg=backdround)
        self.buttons = {
            "CLASSIC": TextButtons(
                "CLASSIC",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.25),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "PRACTICE": TextButtons(
                "PRACTICE",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.40),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "SETTINGS": TextButtons(
                "SETTINGS",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.55),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "EXIT": TextButtons(
                "EXIT",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.70),
                sc_size=(self.settings.width, self.settings.height),
            ),
        }
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CLASSIC"])

        self.buttons["CLASSIC"].next_buttons = [
            self.buttons["EXIT"],
            None,
            self.buttons["PRACTICE"],
            None,
        ]
        self.buttons["PRACTICE"].next_buttons = [
            self.buttons["CLASSIC"],
            None,
            self.buttons["SETTINGS"],
            None,
        ]
        self.buttons["SETTINGS"].next_buttons = [
            self.buttons["PRACTICE"],
            None,
            self.buttons["EXIT"],
            None,
        ]
        self.buttons["EXIT"].next_buttons = [
            self.buttons["SETTINGS"],
            None,
            self.buttons["CLASSIC"],
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
            if b is self.buttons["CLASSIC"]:
                self.set_state(GameStates.custom_classic)
            elif b is self.buttons["PRACTICE"]:
                self.set_state(GameStates.practice)
            elif b is self.buttons["SETTINGS"]:
                self.set_state(GameStates.in_settings)
            elif b is self.buttons["EXIT"]:
                self.set_state(GameStates.quitting)


class SettingsMenu(Menu):
    def __init__(self, game, state, backdround: Background = None):
        super().__init__(game, state, bg=backdround)

        self.buttons = {}
        y_pos = 0.05
        for resolution in gp.RESOLUTIONS:
            key = "x".join([str(resolution[0]), str(resolution[1])])
            self.buttons[key] = TextButtons(
                key,
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, y_pos),
                sc_size=(self.settings.width, self.settings.height),
            )
            y_pos += 0.12
        self.buttons["BACK"] = TextButtons(
            "BACK",
            DefaultTemplate,
            self.game.main_font,
            (0.16, 0.1),
            (0.42, 0.88),
            sc_size=(self.settings.width, self.settings.height),
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


class ClassicSettings(Menu):
    def __init__(self, game, state, backdround: Background = None):
        super().__init__(game, state, bg=backdround)
        self.buttons = {
            "CONFIRM": TextButtons(
                "CONFIRM",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.30, 0.86),
                (self.settings.width, self.settings.height),
            ),
            "BACK": TextButtons(
                "BACK",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.50, 0.86),
                (self.settings.width, self.settings.height),
            ),
        }
        self.sliders = {
            "Level": Slider(
                DefaultTemplate,
                "Level",
                self.game.main_font,
                (0.41, 0.5),
                (0.16, 0.05),
                (0, 15),
                (self.settings.width, self.settings.height),
                True,
            )
        }
        self.buttons["CONFIRM"].next_buttons = [None, self.buttons["BACK"], None, self.buttons["BACK"]]
        self.buttons["BACK"].next_buttons = [None, self.buttons["CONFIRM"], None, self.buttons["CONFIRM"]]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CONFIRM"])

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
            if b is self.buttons["CONFIRM"]:
                self.set_state(GameStates.Tetris)
            elif b is self.buttons["BACK"]:
                self.set_state(GameStates.main_menu)

    def loop(self) -> int:
        super().loop()
        return self.sliders["Level"].output


class PracticeMenu(Menu):
    def __init__(self, game, state):
        super().__init__(game, state, bg=game.shared_bg)
        self.sliders = {
            "Level": Slider(
                DefaultTemplate,
                "Level",
                self.game.main_font,
                (0.31, 0.30),
                (0.16, 0.05),
                (0, 15),
                (self.settings.width, self.settings.height),
                True,
            )
        }
        self.buttons = {
            "CONFIRM": TextButtons(
                "CONFIRM",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.30, 0.86),
                (self.settings.width, self.settings.height),
            ),
            "BACK": TextButtons(
                "BACK",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.50, 0.86),
                (self.settings.width, self.settings.height),
            ),
        }
        carousel_list = ["I-spin", "L-spin", "T-spin", "S-spint", "Z-spin"]
        self.carousels = {
            "PresetSelector": Carousel(
                carousel_list,
                DefaultTemplate,
                (0.75, 0.85),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
            )
        }
        self.buttons["CONFIRM"].next_buttons = [None, self.buttons["BACK"], None, self.buttons["BACK"]]
        self.buttons["BACK"].next_buttons = [None, self.buttons["CONFIRM"], None, self.buttons["CONFIRM"]]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CONFIRM"])
        self.game.editor.select_preset(carousel_list[0])

    def draw(self):
        super().draw()
        self.game.editor.draw(self.game.screen)

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
            if b is self.buttons["CONFIRM"]:
                self.set_state(GameStates.Tetris)
            elif b is self.buttons["BACK"]:
                self.set_state(GameStates.main_menu)
        t = self.carousels["PresetSelector"].check_input()
        if t[0]:
            self.game.editor.select_preset(t[1])


class PauseScreen(TransparentMenu):
    def __init__(self, game, state):
        super().__init__(game, state, "PAUSED")
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
        self.do_fade = True

    def handle_events(self):
        self.do_fade = True
        if self.mouse_mode:
            for item in self.buttons.values():
                item.move_cursor(self.cursor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(self.game.last_played)
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


class GameOver(TransparentMenu):
    def __init__(self, game, state):
        super().__init__(game, state, "GAME OVER")
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
