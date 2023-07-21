import Globals as gp
from GamePlay import Tetris
import GameMenus
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
            self.InitBorders()

        def set_resolution(self, new_resolution):
            self.selected_res = new_resolution
            self.width = self.selected_res[0]
            self.height = self.selected_res[1]
            self.cell_size = round(gp.BASE_CELL_SIZE * (self.height / gp.BASE_RESOLUTION[1]))
            self.font_size = round(gp.BASE_FONT_SIZE * (self.height / gp.BASE_RESOLUTION[1]))
            self.board_width = 12 * self.cell_size
            self.board_height = (gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT) * self.cell_size
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
                }
                json.dump(data, f, indent=4)

    def __init__(self, full_screen: bool = False, vsync_active: bool = False) -> None:
        self.settings = Main.Settings()
        self.editor = Editor(self.settings, (0.745, 0.04))
        self.window_style = pygame.FULLSCREEN | pygame.SCALED if full_screen or self.settings.fullscreen else 0
        pygame.init()
        bit_depth = pygame.display.mode_ok((self.settings.width, self.settings.height), self.window_style, 32)
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), self.window_style | pygame.HWSURFACE, bit_depth, vsync=vsync_active
        )
        pygame.display.set_caption("Tetris")
        pygame.mixer.pre_init(
            frequency=44100,
            size=32,
            channels=2,
            buffer=512,
        )
        self.main_font = pygame.font.Font("Assets/Font/OpenSans-ExtraBold.ttf", self.settings.font_size)
        self.clock = pygame.time.Clock()
        self.state = GameStates.initilized
        self.last_played = None
        self.pending_state = None
        self.shared_bg = GameMenus.Background(self.settings)
        self.transition_surface = pygame.Surface((self.settings.width, self.settings.height), pygame.HWACCEL)
        self.transition_surface.fill(gp.BLACK)
        self.alpha = 255
        self.transition_surface.set_alpha(self.alpha)

    def set_state(self, new_state, last_mode: str = None):
        if last_mode:
            self.last_played = last_mode
        self.state = new_state

    def set_pending_state(self, next_state):
        self.pending_state = next_state

    def start_game(self):
        self.GameModes = {GameStates.Tetris: Tetris(self)}
        self.MainMenu = GameMenus.MainMenu(self, GameStates.main_menu, self.shared_bg)
        self.Pause = GameMenus.PauseScreen(self, GameStates.paused)
        self.SettingsMenu = GameMenus.SettingsMenu(self, GameStates.in_settings, backdround=self.shared_bg)
        self.ClassicSettings = GameMenus.ClassicSettings(self, GameStates.custom_classic, self.shared_bg)
        self.GameOver = GameMenus.GameOver(self, GameStates.game_over)
        self.PracticeMenu = GameMenus.PracticeMenu(self, GameStates.practice)
        self.set_state(GameStates.main_menu)
        self.loop()

    def resize(self):
        self.transition_surface = pygame.Surface((self.settings.width, self.settings.height), pygame.HWACCEL)
        self.main_font = pygame.font.Font("Assets/Font/OpenSans-ExtraBold.ttf", self.settings.font_size)
        bit_depth = pygame.display.mode_ok((self.settings.width, self.settings.height), self.window_style, 32)
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), self.window_style | pygame.HWSURFACE, depth=bit_depth
        )
        self.MainMenu.resize()
        self.Pause.resize()
        self.SettingsMenu.resize()
        self.ClassicSettings.resize()
        self.GameOver.resize()
        for value in self.GameModes.values():
            value.resize()

    def loop(self):
        while self.state != GameStates.quitting:
            if self.state in list(self.GameModes.keys()):
                self.GameModes[self.state].loop()

            elif self.state == GameStates.main_menu:
                self.MainMenu.loop()

            elif self.state == GameStates.custom_classic:
                self.GameModes[GameStates.Tetris].set_attr(self.ClassicSettings.loop())

            elif self.state == GameStates.practice:
                self.PracticeMenu.loop()

            elif self.state == GameStates.changing_res:
                self.resize()
                self.set_state(self.pending_state)

            elif self.state == GameStates.paused:
                self.Pause.loop(self.GameModes[self.last_played].main_surface)

            elif self.state == GameStates.in_settings:
                self.SettingsMenu.loop()

            elif self.state == GameStates.resetting:
                self.GameModes[self.last_played].reset_game()
                self.set_state(self.pending_state)

            elif self.state == GameStates.game_over:
                self.GameOver.loop(self.GameModes[self.last_played].main_surface)
            else:
                print("Failed to enter", self.state)
                break
        self.settings.save_settings()
        sys.exit()


if __name__ == "__main__":
    Main(False, False).start_game()
