import pygame

class Buttons:
    idle="idle"
    armed="armed"
    
    def __init__(self, text ,size:list , pos:list,gui_font,outline : int=False ,color:tuple=(0,0,0),text_color:tuple=(255,255,255),hover_color:tuple=(0,0,0),sc_size:list=(1,1),Next:list=None)->None :
        self.pos=pos
        self.size=size
        self.outline_size=outline
        self.text=text
        self.state="idle"
        self.text_color=text_color
        self.bg_color=color
        self.color=color
        self.hover_color=hover_color
        self.resize(sc_size,gui_font)
        self.clicked=False
        self.next_buttons=Next
        
    def draw(self,screen):
        if self.lrect:
            pygame.draw.rect(screen,(255,255,255),self.lrect)
        pygame.draw.rect(screen,self.color,self.rectangle)
        screen.blit(self.tex_surf,self.text_rect)
        self.checkclick()
    
    def checkclick(self)->bool:
        mouse_pos=pygame.mouse.get_pos()  
        if self.rectangle.collidepoint(mouse_pos):
            self.color=self.hover_color
            if pygame.mouse.get_pressed()[0]:
                self.state=Buttons.armed
            if not pygame.mouse.get_pressed()[0] and self.state==Buttons.armed:
                self.state=Buttons.idle
                return True
        else:
            self.state=Buttons.idle
            self.color=self.bg_color
        return False
    
    def resize(self,sc_size,font):
        self.lrect=pygame.Rect(self.pos[0]*sc_size[0]-self.outline_size,
                               self.pos[1]*sc_size[1]-self.outline_size,
                               self.size[0]*sc_size[0]+self.outline_size*2,
                               self.size[1]*sc_size[1]+self.outline_size*2
                               ) if self.outline_size else None 
        
        self.rectangle=pygame.Rect(self.pos[0]*sc_size[0],
                                   self.pos[1]*sc_size[1],
                                   self.size[0]*sc_size[0],
                                   self.size[1]*sc_size[1]
                                   )
        self.tex_surf=font.render(self.text,True,self.text_color)
        self.text_rect=self.tex_surf.get_rect(center=self.rectangle.center)
        
    def get_attributes(self):
        return (self.rectangle.center,(self.rectangle.width,self.rectangle.height))