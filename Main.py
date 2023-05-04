import game_parameters as gp
from GamePlay import Tetris
import Menu
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
        self.main_font=pygame.font.SysFont("arialblack",gp.base_font_scale)
        self.clock=pygame.time.Clock()
        self.state=GameStates.initilized
        self.game_screens=[]
        self.last_played=None
        self.pending_state=None
    
    def set_state(self,new_state,last_mode:str=None):
        if last_mode:
            self.last_played=last_mode
        self.state=new_state
    
    
    def set_pending_state(self,next_state):
        self.pending_state=next_state
    
    def start_game(self):
        self.GameModes={GameStates.Tetris:Tetris(self)}
        self.MainMenu=Menu.MainMenu(self)
        self.Pause=Menu.PauseScreen(self)
        self.Settings=Menu.SettingsMenu(self)
        self.set_state(GameStates.main_menu)
        self.loop()
    
    def resize(self,selected_res):
        scale=gp.change_display_val(selected_res)
        self.main_font=pygame.font.SysFont("arialblack",int(gp.base_font_scale*scale[1]))#pygame.font.Font("Assets/kimberley bl.otf",int(gp.base_font_scale*scale[1]))
        bit_depth=pygame.display.mode_ok((gp.WIDTH,gp.HEIGHT),False,32)
        self.screen=pygame.display.set_mode((gp.WIDTH,gp.HEIGHT),depth=bit_depth)
        self.MainMenu.resize()
        self.Pause.resize()
        self.Settings.resize()
        for key,item in self.GameModes.items():
            item.resize()
     
    def loop(self):
        while self.state!=GameStates.quitting:
            if self.state in list(self.GameModes.keys()):
                self.GameModes[self.state].loop()

            elif self.state==GameStates.main_menu:
                self.MainMenu.loop()
                
            elif self.state==GameStates.changing_res:
                self.resize(gp.selected_res)
                self.set_state(self.pending_state)
                
            elif self.state==GameStates.paused:
                self.Pause.loop(self.GameModes[self.last_played].main_surface)
                
            elif self.state==GameStates.in_settings:
                self.Settings.loop()
                
            elif self.state==GameStates.resetting:
                self.GameModes[self.last_played].reset_game()
                self.set_state(self.pending_state)
                
            elif self.state==GameStates.game_over:
                pass

        sys.exit()



new_game=Main((gp.WIDTH,gp.HEIGHT),False,False)
new_game.start_game()