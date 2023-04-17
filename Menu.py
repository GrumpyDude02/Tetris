from functions import *
from GameStates import GameStates
import enum,sys


class buttons:
    def __init__(self, text , width : float, height : float, posx : float, posy : float,gui_font,outline : int=False ,color:tuple=(0,0,0),text_color:tuple=(255,255,255),hover_color:tuple=(0,0,0))->None :
        self.pos=[posx,posy]
        self.size=[width,height]
        self.outline_size=outline
        self.lrect=pygame.Rect(self.pos[0]*WIDTH-self.outline_size,
                               self.pos[1]*HEIGHT-self.outline_size,
                               self.size[0]*WIDTH+self.outline_size*2,
                               self.size[1]*HEIGHT+self.outline_size*2
                               ) if self.outline_size else None 
        
        self.rectangle=pygame.Rect(self.pos[0]*WIDTH,
                                   self.pos[1]*HEIGHT,
                                   self.size[0]*WIDTH,
                                   self.size[1]*HEIGHT
                                   )
        self.bg_color=color
        self.color=color
        self.hover_color=hover_color
        self.tex_surf=gui_font.render(text,True,text_color)
        self.text_rect=self.tex_surf.get_rect(center=self.rectangle.center)
        self.clicked=False
        
    def draw(self,screen):
        if self.lrect:
            pygame.draw.rect(screen,(255,255,255),self.lrect)
        pygame.draw.rect(screen,self.color,self.rectangle)
        screen.blit(self.tex_surf,self.text_rect)
        self.checkclick()
    
    def checkclick(self)->bool:
        clicked=False
        mouse_pos=pygame.mouse.get_pos()  
        if self.rectangle.collidepoint(mouse_pos):
            self.color=self.hover_color
            if pygame.mouse.get_pressed()[0] and self.clicked==False:
                clicked=True
        elif not self.rectangle.collidepoint(mouse_pos):
            self.color=self.bg_color
        if not pygame.mouse.get_pressed()[0]:
                self.clicked=False
        return clicked
    
    def resize(font):
        pass
    
class Menu:
    
    def __init__(self,game,child_menus: list=None,previous_menu=None):
        self.game=game
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
        self.child_menus=child_menus
        self.previous_menu=previous_menu
        self.buttons=None
        
    def set_state(self,new_state):
        self.game.set_state(new_state)
    
    def set_pending_state(self,next_state):
        self.game.pending_state=next_state
    
    def draw(self,fill_color:tuple=None):
        if fill_color:
            self.main_surface.fill(fill_color)
        for key in self.buttons.keys():
            self.buttons[key].draw(self.main_surface)
    
    def resize(self):
        pass





class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.buttons={"PLAY":buttons("PLAY",0.16,0.1,0.42,0.35,game.main_font,5,hover_color=BLUE),
                      "EXIT":buttons("EXIT",0.16,0.1,0.42,0.50,game.main_font,5,hover_color=BLUE)}

    def loop(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
        if self.buttons["EXIT"].checkclick():
            self.set_state(GameStates.quitting)
        if self.buttons["PLAY"].checkclick():
                self.set_state(GameStates.in_game)
        self.draw()
            

class PauseScreen(Menu):
    def __init__(self,font,game):
        super().__init__(game)
        self.transparent_surf=generate_surf((WIDTH,HEIGHT),150)
        self.rect=pygame.Rect(0,0,WIDTH,HEIGHT)
        self.text=font.render("PAUSED",True,WHITE)
        self.transparent_surf.fill(BLUE)
        #0.52 0.60 0.32 0.60
        self.buttons= {"EXIT":buttons("EXIT", 0.16 , 0.1, 0.52, 0.60 ,game.main_font,5,hover_color=BLUE),
                       "RESUME":buttons("RESUME", 0.16 , 0.1 , 0.32 ,0.60 ,game.main_font,5,hover_color=BLUE)}
    
    def draw(self,surface):
        blurred_surface=blurSurf(surface,5)
        self.main_surface.blit(blurred_surface,(0,0))
        self.main_surface.blit(self.transparent_surf,(0,0))
        render_position=self.text.get_rect()
        render_position.center=self.rect.center
        self.main_surface.blit(self.text,render_position)
        super().draw()
    
    def loop(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type==pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    self.set_state(GameStates.in_game)
        if self.buttons["EXIT"].checkclick():
            self.set_pending_state(GameStates.main_menu)
            self.set_state(GameStates.resetting)
        elif self.buttons["RESUME"].checkclick():
            self.set_state(GameStates.in_game)