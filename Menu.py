from functions import *
from GameStates import GameStates

class Menu:
    def __init__(self,button_list,game):
        self.game=game
        self.button_list=button_list
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
    
    def draw(self):
        if not button:
            return 
        for button in self.button_list:
            button.draw(self.main_surface)
        
    def set_state(self,new_state):
        self.game.set_state(new_state)
            
class PauseScreen(Menu):
    def __init__(self,font,game):
        super().__init__([],game)
        self.transparent_surf=generate_surf((WIDTH,HEIGHT),150)
        self.rect=pygame.Rect(0,0,WIDTH,HEIGHT)
        self.text=font.render("PAUSED",True,WHITE)
        self.transparent_surf.fill(BLUE)
    
    def draw(self,surface):
        blurred_surface=blurSurf(surface,5)
        self.main_surface.blit(blurred_surface,(0,0))
        self.main_surface.blit(self.transparent_surf,(0,0))
        render_position=self.text.get_rect()
        render_position.center=self.rect.center
        self.main_surface.blit(self.text,render_position)
    
    def loop(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type==pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    self.set_state(GameStates.in_game)
