import Globals as gp
from GamePlay import Tetris
import GameMenus
from GameStates import GameStates
import sys, pygame, json


class Main:
    class Settings:
        def __init__(self):
            try:
                with open("Settings.txt") as f:
                    data = json.load(f)
                    self.load_data(data)
            except FileNotFoundError:
                self.load_defaults()

        def InitGrid(self):
            self.grid=[]
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
            self.InitGrid()

        def set_resolution(self, new_resolution):
            self.selected_res = new_resolution
            self.width = self.selected_res[0]
            self.height = self.selected_res[1]
            self.cell_size = round(gp.BASE_CELL_SIZE * (self.height / gp.BASE_RESOLUTION[1]))
            self.font_size = round(gp.BASE_FONT_SIZE * (self.height / gp.BASE_RESOLUTION[1]))
            self.board_width = 12 * self.cell_size
            self.board_height = (gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT) * self.cell_size
            self.InitGrid()
            self.save_settings()

        def load_defaults(self):
            self.selected_res = gp.BASE_RESOLUTION
            self.width = gp.BASE_RESOLUTION[0]
            self.height = gp.BASE_RESOLUTION[1]
            self.cell_size = gp.BASE_CELL_SIZE
            self.font_size = gp.BASE_FONT_SIZE
            self.board_height = (gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT) * self.cell_size
            self.board_width = 12 * self.cell_size
            self.InitGrid()
            self.save_settings()
                
        def save_settings(self):
            with open("Settings.txt","w") as f:
                data = {"SelectedResolution": self.selected_res,
                    "CellSize": self.cell_size,
                    "FontSize": self.font_size,
                    "BoardWidth":self.board_width,
                    "BoardHeight": self.board_height}
                json.dump(data,f,indent=4)

    def __init__(self, sc_size: tuple, full_screen: bool = False, vsync_active: bool = False) -> None:
        window_style = pygame.FULLSCREEN if full_screen else 0
        pygame.init()
        self.settings = Main.Settings()
        bit_depth = pygame.display.mode_ok((self.settings.width,self.settings.height), window_style, 32)
        self.screen = pygame.display.set_mode((self.settings.width,self.settings.height), window_style, bit_depth, vsync=vsync_active)
        pygame.display.set_caption("Tetris")
        pygame.mixer.pre_init(
            frequency=44100,
            size=32,
            channels=2,
            buffer=512,
        )
        self.main_font = pygame.font.SysFont("arialblack", self.settings.font_size)
        self.clock = pygame.time.Clock()
        self.state = GameStates.initilized
        self.game_screens = []
        self.last_played = None
        self.pending_state = None
        self.shared_bg = GameMenus.Background(self.settings)

    def set_state(self, new_state, last_mode: str = None):
        if last_mode:
            self.last_played = last_mode
        self.state = new_state

    def set_pending_state(self, next_state):
        self.pending_state = next_state

    def start_game(self):
        self.GameModes = {GameStates.Tetris: Tetris(self)}
        self.MainMenu = GameMenus.MainMenu(self, backdround=self.shared_bg)
        self.Pause = GameMenus.PauseScreen(self)
        self.SettingsMenu = GameMenus.SettingsMenu(self, backdround=self.shared_bg)
        self.GameOver = GameMenus.GameOver(self)
        self.set_state(GameStates.main_menu)
        self.loop()

    def resize(self):
        self.main_font = pygame.font.SysFont("arialblack", self.settings.font_size)
        bit_depth = pygame.display.mode_ok((self.settings.width, self.settings.height), False, 32)
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height), depth=bit_depth)
        self.MainMenu.resize()
        self.Pause.resize()
        self.SettingsMenu.resize()
        self.GameOver.resize()
        for value in self.GameModes.values():
            value.resize()

    def loop(self):
        while self.state != GameStates.quitting:
            if self.state in list(self.GameModes.keys()):
                self.GameModes[self.state].loop()

            elif self.state == GameStates.main_menu:
                self.MainMenu.loop()

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
        self.settings.save_settings()
        sys.exit()


if __name__ == "__main__":
    Main((gp.WIDTH, gp.HEIGHT), False, False).start_game()
