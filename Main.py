import Globals as gp
import GameMenus
from Primitives.Game import Game
from Editor import Editor
from GameStates import GameStates
import sys, pygame, json, os


os.environ["SDL_VIDEO_CENTERED"] = "1"


class Main:
    class Settings:
        def __init__(self):
            try:
                with open("Settings.txt") as f:
                    data = json.load(f)
                    self.load_data(data)
            except FileNotFoundError:
                self.load_defaults()
            finally:
                self.offset = ((self.width - 12 * self.cell_size) // 2, (self.height - 24 * self.cell_size) // 2)

        def InitBorders(self):
            self.grid = []
            for i in range(0, gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT):
                for j in range(gp.PLAYABLE_AREA_CELLS + gp.X_BORDER_OFFSET):
                    if j == 0 or j == gp.PLAYABLE_AREA_CELLS + gp.X_BORDER_OFFSET - 1:
                        self.grid.append(
                            pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                        )
                    elif i == 0 or i == gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT - 1:
                        self.grid.append(
                            pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                        )

        def load_data(self, data):
            self.selected_res = data["SelectedResolution"]
            self.width = self.selected_res[0]
            self.height = self.selected_res[1]
            self.cell_size = data["CellSize"]
            self.font_size = data["FontSize"]
            self.board_width = data["BoardWidth"]
            self.board_height = data["BoardHeight"]
            self.fullscreen = data["FullScreen"]
            self.resizable = data["Resizable"]
            self.volume = data["SoundLevel"]
            self.play_sound = data["PlaySound"]
            self.InitBorders()

        def set_resolution(self, new_resolution):
            self.selected_res = max(new_resolution, (gp.MIN_WIDTH, gp.MIN_HEIGHT))
            self.width = self.selected_res[0]
            self.height = self.selected_res[1]
            scaling_factor = min((self.width / gp.BASE_RESOLUTION[0]) * 1.4, self.height / gp.BASE_RESOLUTION[1])
            self.cell_size = round(gp.BASE_CELL_SIZE * scaling_factor)
            self.font_size = round(gp.BASE_FONT_SIZE * scaling_factor)
            self.board_width = 12 * self.cell_size
            self.board_height = (gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT) * self.cell_size
            self.offset = ((self.width - 12 * self.cell_size) // 2, (self.height - 24 * self.cell_size) // 2)
            self.InitBorders()
            self.save_settings()

        def load_defaults(self):
            self.selected_res = gp.BASE_RESOLUTION
            self.width = gp.BASE_RESOLUTION[0]
            self.height = gp.BASE_RESOLUTION[1]
            self.cell_size = gp.BASE_CELL_SIZE
            self.font_size = gp.BASE_FONT_SIZE
            self.board_height = (gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT) * self.cell_size
            self.board_width = 12 * self.cell_size
            self.fullscreen = False
            self.resizable = False
            self.volume = 0.5
            self.play_sound = True
            self.InitBorders()
            self.save_settings()

        def save_settings(self):
            with open("Settings.txt", "w") as f:
                data = {
                    "SelectedResolution": self.selected_res,
                    "CellSize": self.cell_size,
                    "FontSize": self.font_size,
                    "BoardWidth": self.board_width,
                    "BoardHeight": self.board_height,
                    "FullScreen": False,
                    "Resizable": self.resizable,
                    "SoundLevel": self.volume,
                    "PlaySound": self.play_sound,
                }
                json.dump(data, f, indent=4)

    class Sound:
        def __init__(self, settings) -> None:
            pygame.mixer.init()
            self.settings = settings
            try:
                self.sounds = {
                    "hit": pygame.mixer.Sound("./Assets/Sounds/hit.mp3"),
                    "harddrop": pygame.mixer.Sound("./Assets/Sounds/harddrop.mp3"),
                    "hold": pygame.mixer.Sound("./Assets/Sounds/hold.ogg"),
                    "clear": pygame.mixer.Sound("./Assets/Sounds/erase1.wav"),
                    "clear1": pygame.mixer.Sound("./Assets/Sounds/erase2.wav"),
                    "clear2": pygame.mixer.Sound("./Assets/Sounds/erase3.wav"),
                    "clear3": pygame.mixer.Sound("./Assets/Sounds/erase4.wav"),
                    "locking": pygame.mixer.Sound("./Assets/Sounds/lock.wav"),
                    "rotate": pygame.mixer.Sound("./Assets/Sounds/rotate.wav"),
                    "gameover": pygame.mixer.Sound("./Assets/Sounds/topout.ogg"),
                }
                self.set_volume(self.settings.volume)
            except FileNotFoundError as e:
                print(e)
                print("Failed to load sounds, path for sounds not found")
                self.sounds = None
                self.settings.play_sound = False

        def set_volume(self, volume):
            self.settings.volume = volume
            for value in self.sounds.values():
                if value is not None:
                    value.set_volume(self.settings.volume)
            self.sounds["harddrop"].set_volume(self.settings.volume * 0.5)

        def play(self, sound_name):
            if self.settings.play_sound is False:
                return
            ref = self.sounds.get(sound_name)
            if ref is None:
                return
            ref.fadeout(500)
            ref.play(fade_ms=50)

    def __init__(self, resizable: bool = False, full_screen: bool = False, vsync_active: bool = False) -> None:
        self.settings = Main.Settings()
        self.sound = Main.Sound(self.settings)
        self.editor = Editor(self.settings, (gp.EDITOR_BOARD_X, 0.04))
        self.update_windows_style()
        pygame.init()
        bit_depth = pygame.display.mode_ok((self.settings.width, self.settings.height), self.window_style, 32)
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), self.window_style | pygame.HWSURFACE, bit_depth, vsync=vsync_active
        )
        pygame.display.set_caption("Tetris")
        self.main_font = pygame.font.Font("Assets/Font/OpenSans-ExtraBold.ttf", self.settings.font_size)
        self.clock = pygame.time.Clock()
        self.state = GameStates.initilized
        self.last_played = None
        self.pending_state = None
        self.previous_state_for_settings = None
        self.shared_bg = GameMenus.Background(self.settings)
        self.transition_surface = pygame.Surface((self.settings.width, self.settings.height), pygame.HWACCEL)
        self.transition_surface.fill(gp.BLACK)
        self.alpha = 255
        self.transition_surface.set_alpha(self.alpha)
        self.data = ()

    def set_state(self, new_state, pending_state: str = None, last_played_mode=None):
        """last_state used for when pausing the game"""
        if pending_state:
            self.pending_state = pending_state
        if last_played_mode:
            self.last_played = last_played_mode
        self.state = new_state

    def start_game(self):
        self.Game = Game(self, GameStates.game)

        self.MainMenu = GameMenus.MainMenu(self, GameStates.main_menu, self.shared_bg)
        self.Pause = GameMenus.PauseScreen(self, GameStates.paused)

        self.SettingsMenu = GameMenus.SettingsMenu(self, GameStates.in_settings, bg=self.shared_bg)
        self.VideoSettings = GameMenus.VideoMenu(self, GameStates.video_settings, backdround=self.shared_bg)
        self.SoundSettings = GameMenus.SoundMenu(self, GameStates.sound_settings, backdround=self.shared_bg)

        self.ClassicSettings = GameMenus.ClassicSettings(self, GameStates.classic_settings, self.shared_bg)
        self.CustomSettings = GameMenus.CustomSettings(self, GameStates.custom_settings)
        self.DigSettings = GameMenus.DigSettings(self, GameStates.dig_settings)

        self.GameOver = GameMenus.GameOver(self, GameStates.game_over)
        self.PracticeMenu = GameMenus.PracticeMenu(self, GameStates.practice_settings)

        self.set_state(GameStates.main_menu)
        self.loop()

    def update_windows_style(self):
        flag = 0
        if self.settings.resizable:
            flag |= pygame.RESIZABLE
        if self.settings.fullscreen:
            flag |= pygame.FULLSCREEN | pygame.SCALED
        self.window_style = flag

    def resize(self):
        self.transition_surface = pygame.Surface((self.settings.width, self.settings.height), pygame.HWACCEL)
        self.main_font = pygame.font.Font("Assets/Font/OpenSans-ExtraBold.ttf", self.settings.font_size)
        bit_depth = pygame.display.mode_ok((self.settings.width, self.settings.height), self.window_style, 32)
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), self.window_style | pygame.HWSURFACE, depth=bit_depth
        )
        self.editor.resize()
        self.MainMenu.resize()
        self.Pause.resize()

        self.SettingsMenu.resize()
        self.SoundSettings.resize()
        self.VideoSettings.resize()

        self.ClassicSettings.resize()
        self.PracticeMenu.resize()
        self.CustomSettings.resize()
        self.DigSettings.resize()
        self.GameOver.resize()
        self.Game.resize()

    def loop(self):
        while self.state != GameStates.quitting:
            if self.state is GameStates.game:
                self.Game.loop()

            elif self.state == GameStates.main_menu:
                self.previous_state_for_settings = GameStates.main_menu
                self.MainMenu.loop()

            elif self.state == GameStates.in_settings:
                self.SettingsMenu.loop(self.previous_state_for_settings)

            elif self.state == GameStates.video_settings:
                self.VideoSettings.loop()

            elif self.state == GameStates.sound_settings:
                self.SoundSettings.loop()

            elif self.state == GameStates.classic_settings:
                self.data = self.ClassicSettings.loop()
                self.Game.init_mode(self.data)

            elif self.state == GameStates.practice_settings:
                self.data = self.PracticeMenu.loop()
                self.Game.init_mode(self.data)

            elif self.state == GameStates.custom_settings:
                self.data = self.CustomSettings.loop()
                self.Game.init_mode(self.data)

            elif self.state == GameStates.dig_settings:
                self.data = self.DigSettings.loop()
                self.Game.init_mode(self.data)

            elif self.state == GameStates.changing_res:
                self.resize()
                self.set_state(self.pending_state)

            elif self.state == GameStates.paused:
                self.previous_state_for_settings = GameStates.paused
                self.Pause.loop(self.Game.main_surface)

            elif self.state == GameStates.resetting:
                self.Game.reset_game()
                self.Game.init_mode(self.data)
                self.set_state(self.pending_state)

            elif self.state == GameStates.game_over:
                self.GameOver.loop(self.Game.main_surface)

            else:
                print("Failed to enter", self.state)
                break
        self.settings.save_settings()
        sys.exit()


if __name__ == "__main__":
    Main(False, False).start_game()
