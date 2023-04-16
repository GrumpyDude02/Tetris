from functions import *
from GameStates import GameStates
import enum


class buttons:
    def __init__(self,text,width,height,posx,posy,hover_color,color) :
        gui_font=pygame.font.SysFont("arialblack",40)
        self.lrect=pygame.Rect(posx-5,posy-5,width+10,height+10)
        self.rectangle=pygame.Rect(posx,posy,width,height)
        self.color=color
        self.hover_color=hover_color
        self.tex_surf=gui_font.render(text,True,(255,255,255))
        self.text_rect=self.tex_surf.get_rect(center=self.rectangle.center)
        self.clicked=False
        
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.lrect)
        pygame.draw.rect(screen,self.color,self.rectangle)
        screen.blit(self.tex_surf,self.text_rect)
        self.checkclick()
    
    def checkclick(self)->bool:
        clicked=False
        temp=self.color
        mouse_pos=pygame.mouse.get_pos()  
        if self.rectangle.collidepoint(mouse_pos):
            self.color=self.hover_color
            if pygame.mouse.get_pressed()[0] and self.clicked==False:
                clicked=True
        if not pygame.mouse.get_pressed()[0]:
                self.clicked=False
                self.color=temp
        return clicked

class MenuStates(enum.Enum):
    main_screen="main_screen"
    modes_menu="modes_menu"
    settings_menu="setings_menu"
    controls_menu="controls_menu"


class Menu:
    def __init__(self,button_list,game,child_menus,parent_menu):
        self.game=game
        self.button_list=button_list
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
        self.child_menus=child_menus
        self.parent_menu=parent_menu
    
    def draw(self):
        if not button:
            return 
        for button in self.button_list:
            button.draw(self.main_surface)
        
    def set_state(self,new_state):
        self.game.set_state(new_state)



class PauseScreen(Menu):
    def __init__(self,font,game):
        super().__init__([],game,[],None)
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
