import pygame

class Buttons:
    def __init__(self, text ,size:list , pos:list,gui_font,outline : int=False ,color:tuple=(0,0,0),text_color:tuple=(255,255,255),hover_color:tuple=(0,0,0),sc_size:list=(1,1))->None :
        self.pos=pos
        self.size=size
        self.outline_size=outline
        self.text_color=color
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
    
    def resize(self,sc_size):
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
        
        self.text_rect=self.tex_surf.get_rect(center=self.rectangle.center)