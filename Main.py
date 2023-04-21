import game_parameters as gp
from GamePlay import Tetris
from Menu import MainMenu,PauseScreen
from GameStates import GameStates
import sys,pygame



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
        self.main_font=pygame.font.Font("Assets/kimberley bl.otf",gp.font_scale)
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
    
    def resize(self,selected_res):
        scale=gp.change_display_val(selected_res)
        gp.font_scale=int(gp.font_scale*scale[1])
        self.main_font=pygame.font.Font("Assets/kimberley bl.otf",int(gp.font_scale))
        bit_depth=pygame.display.mode_ok((gp.WIDTH,gp.HEIGHT),False,32)
        self.screen=pygame.display.set_mode((gp.WIDTH,gp.HEIGHT),depth=bit_depth)
        self.MainMenu.resize()
        self.Tetris.resize()
     
    def loop(self):
        while self.state!=GameStates.quitting:
            if self.state==GameStates.main_menu:
                self.MainMenu.loop()
            elif self.state==GameStates.in_game:
                self.Tetris.loop()
            elif self.state==GameStates.changing_res:
                self.resize(gp.Resolutions[2])
                self.set_state(self.pending_state)
            elif self.state==GameStates.paused:
                self.Pause.loop(self.Tetris.main_surface)
            elif self.state==GameStates.resetting:
                self.Tetris.reset_game()
                self.set_state(self.pending_state)
            elif self.state==GameStates.game_over:
                pass
        sys.exit()



new_game=Main((gp.WIDTH,gp.HEIGHT),False,False)
new_game.start_game()