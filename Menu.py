from functions import *
from GameStates import GameStates
import enum,sys


class buttons:
    def __init__(self,text,width:int,height:int,posx:int,posy:int,hover_color:tuple,color:tuple,text_color:tuple,gui_font)->None :
        self.lrect=pygame.Rect(posx-5,posy-5,width+10,height+10)
        self.rectangle=pygame.Rect(posx,posy,width,height)
        self.bg_color=color
        self.color=color
        self.hover_color=hover_color
        self.tex_surf=gui_font.render(text,True,text_color)
        self.text_rect=self.tex_surf.get_rect(center=self.rectangle.center)
        self.clicked=False
        
    def draw(self,screen):
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
    
    def set_size(font):
        pass
    
class Menu:
    def __init__(self,game,next_game_state,previous_game_state):
        self.game=game
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
        self.next_game_state=next_game_state
        self.previous_game_state=previous_game_state
        
    def set_state(self,new_state):
        self.game.set_state(new_state)






class MainMenu(Menu):
    def __init__(self, game, next_game_state, previous_game_state):
        super().__init__(game, next_game_state, previous_game_state)
        self.buttons={"PLAY":buttons("PLAY",int(WIDTH*0.16),int(HEIGHT*0.1),int(0.42*WIDTH),int(0.35*HEIGHT),BLUE,(0,0,0),(255,255,255),game.main_font),
                      "EXIT":buttons("EXIT",int(WIDTH*0.16),int(HEIGHT*0.1),int(0.42*WIDTH),int(0.50*HEIGHT),BLUE,(0,0,0),(255,255,255),game.main_font)}
    
    def draw(self):
        self.main_surface.fill((0,0,0))
        self.buttons["PLAY"].draw(self.main_surface)
        self.buttons["EXIT"].draw(self.main_surface)

    def loop(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
        if self.buttons["PLAY"].checkclick():
                self.set_state(GameStates.in_game)
        self.draw()
            

class PauseScreen(Menu):
    def __init__(self,font,game):
        super().__init__(game,None,None)
        self.transparent_surf=generate_surf((WIDTH,HEIGHT),150)
        self.rect=pygame.Rect(0,0,WIDTH,HEIGHT)
        self.text=font.render("PAUSED",True,WHITE)
        self.transparent_surf.fill(BLUE)
        self.buttons= {"EXIT":buttons("EXIT",int(WIDTH*0.16),int(HEIGHT*0.1),int(0.52*WIDTH),int(0.60*HEIGHT),BLUE,(0,0,0),(255,255,255),game.main_font),
                       "RESUME":buttons("RESUME",int(WIDTH*0.16),int(HEIGHT*0.1),int(0.32*WIDTH),int(0.60*HEIGHT),BLUE,(0,0,0),(255,255,255),game.main_font)}
    
    def draw(self,surface):
        blurred_surface=blurSurf(surface,5)
        self.main_surface.blit(blurred_surface,(0,0))
        self.main_surface.blit(self.transparent_surf,(0,0))
        render_position=self.text.get_rect()
        render_position.center=self.rect.center
        self.main_surface.blit(self.text,render_position)
        self.buttons["EXIT"].draw(self.main_surface)
        self.buttons["RESUME"].draw(self.main_surface)
    
    def loop(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type==pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    self.set_state(GameStates.in_game)
        if self.buttons["EXIT"].checkclick():
            self.set_state(GameStates.quitting)
        elif self.buttons["RESUME"].checkclick():
            self.set_state(GameStates.in_game)