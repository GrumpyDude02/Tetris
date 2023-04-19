from game_parameters import *
from GamePlay import Tetris
from Menu import *
from GameStates import GameStates
from functions import change_display_val
import sys



class Main:
    def __init__(self,sc_size:tuple,full_screen:bool=False,vsync_active:bool=False) -> None:
    
        window_style=pygame.FULLSCREEN if full_screen else 0
        pygame.init()
        bit_depth=pygame.display.mode_ok(sc_size,window_style,32)
        self.screen=pygame.display.set_mode(sc_size,window_style,bit_depth,vsync=vsync_active)
        pygame.display.set_caption("Tetris")
        pygame.mixer.pre_init(
            frequency=44100,
            size=32,
            channels=2,
            buffer=512,
        )
        self.main_font=pygame.font.Font("Assets/kimberley bl.otf",font_scale)
        self.clock=pygame.time.Clock()
        self.state=GameStates.initilized
        self.game_screens=[]
        self.pending_state=None
    
    def set_state(self,new_state):
        if new_state:
            self.state=new_state
    
    def set_pending_state(self,next_state):
        self.pending_state=next_state
    
    def start_game(self):
        self.Tetris=Tetris(self)
        self.MainMenu=MainMenu(self)
        self.Pause=PauseScreen(self.main_font,self)
        self.game_screens.append(self.Tetris)
        self.game_screens.append(self.Pause)
        self.set_state(GameStates.main_menu)
        self.loop()
    
    def resize_window(self,selected_res):
        global font_scale
        scale=change_display_val(selected_res)
        font_scale*=scale
        self.main_font=pygame.font.Font("Assets/kimberley bl.otf",font_scale)
        bit_depth=pygame.display.mode_ok((WIDTH,HEIGHT),False,32)
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT),depth=bit_depth)
        for screen in self.game_screens:
            screen.resize()
     
    def loop(self):
        while self.state!=GameStates.quitting:
            if self.state==GameStates.main_menu:
                self.MainMenu.loop()
            elif self.state==GameStates.in_game:
                self.Tetris.loop()
            elif self.state==GameStates.changing_res:
                last_state=self.state
                self.resize_window()
                self.set_state(last_state)
            elif self.state==GameStates.paused:
                self.Pause.loop(self.Tetris.main_surface)
            elif self.state==GameStates.resetting:
                self.Tetris.reset_game()
                self.set_state(self.pending_state)
            elif self.state==GameStates.game_over:
                pass
        sys.exit()



new_game=Main((WIDTH,HEIGHT),False,False)
new_game.start_game()