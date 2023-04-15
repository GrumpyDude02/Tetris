from game_parameters import *
from GamePlay import Tetris
from Menu import Menu,PauseScreen
from GameStates import GameStates
import sys



class Main:
    def __init__(self,sc_size:tuple,full_screen:bool=False,vsync_active:bool=False) -> None:
        try:
            window_style=pygame.FULLSCREEN if full_screen else 0
            pygame.init()
            bit_depth=pygame.display.mode_ok(sc_size,window_style,32)
            self.screen=pygame.display.set_mode(sc_size,window_style,bit_depth,vsync=vsync_active)
            pygame.mixer.pre_init(
                frequency=44100,
                size=32,
                channels=2,
                buffer=512,
            )
            self.MainFont=pygame.font.Font("kimberley bl.otf",24)
        except(Exception):
            raise "cannot initialize pygame"
        self.font=pygame.Font("kimberley bl.otf",30)
        self.clock=pygame.time.Clock()
        self.dt=1/FPS
        self.state=GameStates.in_game
    
    def set_state(self,new_state):
        self.state=new_state
    
    def start_game(self):
        self.Tetris=Tetris(self)
        self.Pause=PauseScreen(self.font,self)
        self.set_state(GameStates.in_game)
        self.loop()
       
    def loop(self):
        while self.state!=GameStates.quitting:
            events=pygame.event.get()
            if self.state==GameStates.in_game:
                self.Tetris.loop(events)
                self.screen.blit(self.Tetris.main_surface,(0,0))
            elif self.state==GameStates.paused:
                self.Pause.loop(events)
                self.Pause.draw(self.Tetris.main_surface)
                self.screen.blit(self.Pause.main_surface,(0,0))
            elif self.state==GameStates.game_over:
                pass
            
            self.dt=self.clock.tick(FPS)/1000
            pygame.display.flip()
        sys.exit()



new_game=Main((WIDTH,HEIGHT),False,False)
new_game.start_game()