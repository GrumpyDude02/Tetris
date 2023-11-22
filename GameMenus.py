import Globals as gp
from GameStates import GameStates
from Tools.Buttons import TextButtons, DefaultTemplate
from Primitives.Menu import Menu, Background, TransparentMenu
from Primitives.Game import Game
from Tools.Slider import Slider
from Tools.Carousel import Carousel


class MainMenu(Menu):
    def __init__(self, game, state, backdround: Background = None):
        super().__init__(game, state, bg=game.shared_bg)
        self.buttons = {
            "CLASSIC": TextButtons(
                "CLASSIC",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.05),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "DIG": TextButtons(
                "DIG",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.20),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "PRACTICE": TextButtons(
                "PRACTICE",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.35),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "CUSTOM": TextButtons(
                "CUSTOM",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.50),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "SETTINGS": TextButtons(
                "SETTINGS",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.65),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "EXIT": TextButtons(
                "EXIT",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.80),
                sc_size=(self.settings.width, self.settings.height),
            ),
        }
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CLASSIC"])

        self.buttons["CLASSIC"].next_buttons = [
            self.buttons["EXIT"],
            None,
            self.buttons["DIG"],
            None,
        ]
        self.buttons["DIG"].next_buttons = [
            self.buttons["CLASSIC"],
            None,
            self.buttons["PRACTICE"],
            None,
        ]
        self.buttons["PRACTICE"].next_buttons = [
            self.buttons["DIG"],
            None,
            self.buttons["CUSTOM"],
            None,
        ]
        self.buttons["SETTINGS"].next_buttons = [
            self.buttons["CUSTOM"],
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
        self.buttons["CUSTOM"].next_buttons = [
            self.buttons["PRACTICE"],
            None,
            self.buttons["SETTINGS"],
            None,
        ]

    def handle_events(self):
        super().handle_events()
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["CLASSIC"]:
                self.set_state(GameStates.classic_settings)
            elif b is self.buttons["DIG"]:
                self.set_state(GameStates.dig_settings)
            elif b is self.buttons["PRACTICE"]:
                self.set_state(GameStates.practice_settings)
            elif b is self.buttons["SETTINGS"]:
                self.set_state(GameStates.in_settings)
            elif b is self.buttons["EXIT"]:
                self.set_state(GameStates.quitting)
            elif b is self.buttons["CUSTOM"]:
                self.set_state(GameStates.custom_settings)


class SettingsMenu(Menu):
    def __init__(self, game, state, child_menus: list = None, previous_menu=None, bg: Background = None):
        super().__init__(game, state, child_menus, previous_menu, bg)
        sc_size = (self.settings.width, self.settings.height)
        self.buttons = {
            "VIDEO": TextButtons("VIDEO", DefaultTemplate, self.game.main_font, (0.16, 0.1), (0.42, 0.25), sc_size=sc_size),
            "SOUND": TextButtons("SOUND", DefaultTemplate, self.game.main_font, (0.16, 0.1), (0.42, 0.4), sc_size=sc_size),
            "BACK": TextButtons("BACK", DefaultTemplate, self.game.main_font, (0.16, 0.1), (0.42, 0.70), sc_size=sc_size),
        }
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["VIDEO"])

        self.buttons["VIDEO"].next_buttons = [self.buttons["BACK"], None, self.buttons["SOUND"], None]
        self.buttons["SOUND"].next_buttons = [self.buttons["VIDEO"], None, self.buttons["BACK"], None]
        self.buttons["BACK"].next_buttons = [self.buttons["SOUND"], None, self.buttons["VIDEO"], None]

    def handle_events(self):
        super().handle_events()
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["VIDEO"]:
                self.set_state(GameStates.video_settings)
            elif b is self.buttons["SOUND"]:
                self.set_state(GameStates.sound_settings)
            elif b is self.buttons["BACK"]:
                self.set_state(self.last_state)

    def loop(self, state):
        self.last_state = state
        super().loop()


class VideoMenu(Menu):
    def __init__(self, game, state, backdround: Background = None):
        super().__init__(game, state, bg=backdround)

        self.buttons = {
            "BACK": TextButtons(
                "BACK",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.60, 0.70),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "APPLY": TextButtons(
                "APPLY",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.25, 0.70),
                sc_size=(self.settings.width, self.settings.height),
            ),
        }
        self.carousels = {
            "RESOLUTION": Carousel(
                ["x".join((str(i[0]), str(i[1]))) for i in gp.RESOLUTIONS],
                DefaultTemplate,
                (0.35, 0.2),
                self.game.main_font,
                (0.3, 0.2),
                sc_size=(self.settings.width, self.settings.height),
                text="Resolution:",
            ),
            "FULLSCREEN": Carousel(
                [str(self.settings.fullscreen), str(not self.settings.fullscreen)],
                DefaultTemplate,
                (0.35, 0.35),
                self.game.main_font,
                (0.3, 0.2),
                (self.settings.width, self.settings.height),
                text="Full-Screen:",
            ),
        }
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["BACK"])
        self.buttons["BACK"].next_buttons = [None, self.buttons["APPLY"], None, self.buttons["APPLY"]]
        self.buttons["APPLY"].next_buttons = [None, self.buttons["BACK"], None, self.buttons["BACK"]]
        self.check_resolution()

    def handle_events(self):
        super().handle_events()
        if self.cursor.button.check_input(self.mouse_mode):
            if self.cursor.button is self.buttons["BACK"]:
                self.set_state(GameStates.in_settings)
            if self.cursor.button is self.buttons["APPLY"]:
                self.settings.fullscreen = True if self.carousels["FULLSCREEN"].current_item() == "True" else False
                new_res = tuple([int(i) for i in self.carousels["RESOLUTION"].current_item().split("x")])
                self.settings.set_resolution(new_res)
                self.set_state(GameStates.changing_res, pending_state=GameStates.video_settings)
        for value in self.carousels.values():
            value.check_input()

    def check_resolution(self):
        exists = (self.settings.width, self.settings.height) in gp.RESOLUTIONS
        if self.carousels["RESOLUTION"].length() > len(gp.RESOLUTIONS) and exists:
            self.carousels["RESOLUTION"].pop(-1)
        elif self.carousels["RESOLUTION"].length() > len(gp.RESOLUTIONS) and not exists:
            self.carousels["RESOLUTION"].current_index = -1
            self.carousels["RESOLUTION"].list[self.carousels["RESOLUTION"].current_index] = "x".join(
                [str(i) for i in (self.settings.width, self.settings.height)]
            )
        elif self.carousels["RESOLUTION"].length() == len(gp.RESOLUTIONS) and not exists:
            self.carousels["RESOLUTION"].add_element("x".join([str(i) for i in (self.settings.width, self.settings.height)]))
            self.carousels["RESOLUTION"].current_index = -1
        self.carousels["RESOLUTION"].update_text()

    def resize(self):
        super().resize()
        self.check_resolution()


class SoundMenu(Menu):
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
            "SOUND VOLUME": Slider(
                DefaultTemplate,
                "Sound Level",
                self.game.main_font,
                (0.45, 0.35),
                (0.16, 0.05),
                (0, 100),
                (self.settings.width, self.settings.height),
            )
        }
        self.carousels = {
            "MUTE": Carousel(
                [str(not self.settings.play_sound), str(self.settings.play_sound)],
                DefaultTemplate,
                (0.44, 0.45),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
                text="MUTE",
            ),
        }
        self.buttons["CONFIRM"].next_buttons = [None, self.buttons["BACK"], None, self.buttons["BACK"]]
        self.buttons["BACK"].next_buttons = [None, self.buttons["CONFIRM"], None, self.buttons["CONFIRM"]]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CONFIRM"])

    def handle_events(self):
        super().handle_events()
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["CONFIRM"]:
                self.game.sound.set_volume(self.sliders["SOUND VOLUME"].output / 100)
                self.settings.play_sound = False if self.carousels["MUTE"].current_item() == "True" else True
                self.set_state(GameStates.in_settings)
            elif b is self.buttons["BACK"]:
                self.set_state(GameStates.in_settings)

        self.carousels["MUTE"].check_input()

    def loop(self):
        self.sliders["SOUND VOLUME"].set_output(self.settings.volume * 100)
        super().loop()


class ControlsMenu(Menu):
    pass


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
                (0.45, 0.35),
                (0.16, 0.05),
                (1, 15),
                (self.settings.width, self.settings.height),
                True,
            )
        }
        self.carousels = {
            "LockSpeed": Carousel(
                ["False", "True"],
                DefaultTemplate,
                (0.44, 0.45),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
                text="Lock Speed",
            ),
        }
        self.buttons["CONFIRM"].next_buttons = [None, self.buttons["BACK"], None, self.buttons["BACK"]]
        self.buttons["BACK"].next_buttons = [None, self.buttons["CONFIRM"], None, self.buttons["CONFIRM"]]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CONFIRM"])

    def handle_events(self):
        super().handle_events()
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["CONFIRM"]:
                self.set_state(GameStates.game)
            elif b is self.buttons["BACK"]:
                self.set_state(GameStates.main_menu)

        self.carousels["LockSpeed"].check_input()

    def loop(self) -> int:
        super().loop()
        lock = True if self.carousels["LockSpeed"].current_item() == "True" else False
        return {
            "Mode": Game.Classic,
            "Shape": "All",
            "Grid": None,
            "Level": self.sliders["Level"].output - 1,
            "LockSpeed": lock,
        }


class DigSettings(Menu):
    def __init__(self, game, state):
        super().__init__(game, state, bg=game.shared_bg)
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
                (0.45, 0.35),
                (0.16, 0.05),
                (1, 15),
                (self.settings.width, self.settings.height),
                True,
            )
        }
        self.carousels = {
            "LockSpeed": Carousel(
                ["False", "True"],
                DefaultTemplate,
                (0.44, 0.45),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
                text="Lock Speed",
            ),
            "ShapeSelector": Carousel(
                ["I", "J", "L", "S", "T", "Z", "All"],
                DefaultTemplate,
                (0.44, 0.60),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
                text="Shape",
            ),
        }
        self.buttons["CONFIRM"].next_buttons = [None, self.buttons["BACK"], None, self.buttons["BACK"]]
        self.buttons["BACK"].next_buttons = [None, self.buttons["CONFIRM"], None, self.buttons["CONFIRM"]]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CONFIRM"])

    def handle_events(self):
        Menu.handle_events(self)
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["CONFIRM"]:
                self.set_state(GameStates.game)
            elif b is self.buttons["BACK"]:
                self.set_state(GameStates.main_menu)

        self.carousels["LockSpeed"].check_input()
        self.carousels["ShapeSelector"].check_input()

    def loop(self) -> int:
        super().loop()
        lock = True if self.carousels["LockSpeed"].current_item() == "True" else False
        return {
            "Mode": Game.Dig,
            "Grid": None,
            "Shape": self.carousels["ShapeSelector"].list[self.carousels["ShapeSelector"].current_index],
            "Level": self.sliders["Level"].output - 1,
            "LockSpeed": lock,
        }


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
                (1, 15),
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
        carousel_list = ["I-spin", "J-spin", "L-spin", "T-spin", "S-spin", "Z-spin"]
        self.carousels = {
            "PresetSelector": Carousel(
                carousel_list,
                DefaultTemplate,
                (gp.EDITOR_BOARD_X, 0.85),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
            ),
            "LockSpeed": Carousel(
                ["False", "True"],
                DefaultTemplate,
                (0.31, 0.45),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
                text="Lock Speed",
            ),
        }
        self.buttons["CONFIRM"].next_buttons = [None, self.buttons["BACK"], None, self.buttons["BACK"]]
        self.buttons["BACK"].next_buttons = [None, self.buttons["CONFIRM"], None, self.buttons["CONFIRM"]]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CONFIRM"])
        self.game.editor.select_preset(carousel_list[0])

    def draw(self):
        super().draw()
        self.game.editor.draw(self.game.screen)

    def handle_events(self):
        super().handle_events()

        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["CONFIRM"]:
                self.set_state(GameStates.game)
            elif b is self.buttons["BACK"]:
                self.set_state(GameStates.main_menu)
        t = self.carousels["PresetSelector"].check_input()
        self.carousels["LockSpeed"].check_input()
        if t[0]:
            self.game.editor.select_preset(t[1])

    def loop(self) -> int:
        self.game.editor.select_preset(self.carousels["PresetSelector"].list[self.carousels["PresetSelector"].current_index])
        super().loop()
        lock = True if self.carousels["LockSpeed"].current_item == "True" else False
        return {
            "Mode": Game.Practice,
            "Level": self.sliders["Level"].output - 1,
            "Grid": self.game.editor.placed_blocks_reference,
            "Shape": self.carousels["PresetSelector"].list[self.carousels["PresetSelector"].current_index].split("-")[0],
            "LockSpeed": lock,
        }


class CustomSettings(Menu):
    def __init__(self, game, state):
        super().__init__(game, state, bg=game.shared_bg)
        self.sliders = {
            "Level": Slider(
                DefaultTemplate,
                "Level",
                self.game.main_font,
                (0.31, 0.30),
                (0.16, 0.05),
                (1, 15),
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
            "ERASE": TextButtons(
                "ERASE",
                DefaultTemplate,
                self.game.main_font,
                (0.11, 0.09),
                (0.31, 0.65),
                (self.settings.width, self.settings.height),
            ),
        }
        self.carousels = {
            "ShapeSelector": Carousel(
                ["I", "J", "L", "S", "T", "Z", "All"],
                DefaultTemplate,
                (0.31, 0.40),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
                text="Shape",
            ),
            "LockSpeed": Carousel(
                ["False", "True"],
                DefaultTemplate,
                (0.31, 0.50),
                self.game.main_font,
                (0.2, 0.1),
                (self.settings.width, self.settings.height),
                text="Lock Speed",
            ),
        }
        self.buttons["CONFIRM"].next_buttons = [
            self.buttons["ERASE"],
            self.buttons["BACK"],
            self.buttons["ERASE"],
            self.buttons["BACK"],
        ]
        self.buttons["BACK"].next_buttons = [
            self.buttons["ERASE"],
            self.buttons["CONFIRM"],
            self.buttons["ERASE"],
            self.buttons["CONFIRM"],
        ]
        self.buttons["ERASE"].next_buttons = [
            self.buttons["BACK"],
            None,
            self.buttons["BACK"],
            None,
        ]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["CONFIRM"])

    def draw(self):
        super().draw()
        self.game.editor.draw(self.game.screen)

    def update(self):
        super().update()
        self.game.editor.update()

    def handle_events(self):
        super().handle_events()
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["CONFIRM"]:
                self.set_state(GameStates.game)
            elif b is self.buttons["BACK"]:
                self.set_state(GameStates.main_menu)
            elif b is self.buttons["ERASE"]:
                self.game.editor.erase()
        self.carousels["ShapeSelector"].check_input()
        self.carousels["LockSpeed"].check_input()

    def loop(self) -> int:
        self.game.editor.select_preset("Custom")
        super().loop()
        lock = True if self.carousels["LockSpeed"].list[self.carousels["LockSpeed"].current_index] == "True" else False
        return {
            "Mode": Game.Custom,
            "Shape": self.carousels["ShapeSelector"].current_item(),
            "Level": self.sliders["Level"].output - 1,
            "Grid": self.game.editor.placed_blocks_reference,
            "LockSpeed": lock,
        }


class PauseScreen(TransparentMenu):
    def create_blurred_surface(self):
        super().create_blurred_surface()
        self.title_pos.y *= 0.3

    def __init__(self, game, state):
        super().__init__(game, state, "PAUSED")
        self.create_blurred_surface()
        self.buttons = {
            "RESUME": TextButtons(
                "RESUME",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.30),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "SETTINGS": TextButtons(
                "SETTINGS",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.45),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "RESET": TextButtons(
                "RESET",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.60),
                sc_size=(self.settings.width, self.settings.height),
            ),
            "EXIT": TextButtons(
                "EXIT",
                DefaultTemplate,
                self.game.main_font,
                (0.16, 0.1),
                (0.42, 0.75),
                sc_size=(self.settings.width, self.settings.height),
            ),
        }
        self.buttons["RESUME"].next_buttons = [
            self.buttons["EXIT"],
            None,
            self.buttons["SETTINGS"],
            None,
        ]
        self.buttons["SETTINGS"].next_buttons = [
            self.buttons["RESUME"],
            None,
            self.buttons["RESET"],
            None,
        ]
        self.buttons["RESET"].next_buttons = [
            self.buttons["SETTINGS"],
            None,
            self.buttons["EXIT"],
            None,
        ]
        self.buttons["EXIT"].next_buttons = [
            self.buttons["RESET"],
            None,
            self.buttons["RESUME"],
            None,
        ]
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["RESUME"])
        self.do_fade = True

    def handle_events(self):
        super().handle_events()
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["RESUME"]:
                self.set_state(self.game.last_played)
            elif b is self.buttons["SETTINGS"]:
                self.set_state(GameStates.in_settings)
            elif b is self.buttons["RESET"]:
                self.set_state(GameStates.resetting, pending_state=self.game.last_played)
            elif b is self.buttons["EXIT"]:
                self.set_state(GameStates.resetting, pending_state=GameStates.main_menu)


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
        self.cursor = Menu.Cursor(gp.BLUE, self.buttons["RESET"])
        self.buttons["EXIT"].next_buttons = [None, self.buttons["RESET"], None, self.buttons["RESET"]]
        self.buttons["RESET"].next_buttons = [None, self.buttons["EXIT"], None, self.buttons["EXIT"]]

    def handle_events(self):
        super().handle_events()
        b = self.cursor.button
        if b.check_input(self.mouse_mode):
            if b is self.buttons["RESET"]:
                self.set_state(GameStates.resetting, last_played_mode=self.game.last_played)
            if b is self.buttons["EXIT"]:
                self.set_state(GameStates.resetting, pending_state=GameStates.main_menu)
