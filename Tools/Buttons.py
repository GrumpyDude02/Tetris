import pygame,pygame.gfxdraw
from dataclasses import dataclass

@dataclass
class ButtonTemplate:
        text_color : tuple
        bg_color : tuple
        hover_color : tuple
        outline_color : tuple
        border_radius : int
        outline_size : int
        outline_radius : int
        secondary_color : tuple = None
  
  
DefaultTemplate = ButtonTemplate((255,255,255),(0,0,0),(0,50,200),(255,255,255), -1 ,4, -1, None)     

class Buttons:
    idle = "idle"
    armed = "armed"
    hover = "hover"
    
    def __init__(self,template : ButtonTemplate,size: list,pos: list,sc_size: list,Next: list = None) -> None:
        self.pos = pos
        self.size = size
        self.template = template
        self.color = self.template.bg_color
        self.clicked = False
        self.next_buttons = Next
        self.state = Buttons.idle
        self.set_size(sc_size)

    
    def set_size(self, sc_size):
        self.outline_rect = pygame.Rect( self.pos[0] * sc_size[0] - self.template.outline_size,
            self.pos[1] * sc_size[1] - self.template.outline_size,
            self.size[0] * sc_size[0] + self.template.outline_size * 2,
            self.size[1] * sc_size[1] + self.template.outline_size * 2,
            ) if self.template.outline_size else None
    
        self.rectangle = pygame.Rect(
            self.pos[0] * sc_size[0], self.pos[1] * sc_size[1], self.size[0] * sc_size[0], self.size[1] * sc_size[1]
        )

    def move_cursor(self, cursor):
        mouse_pos = pygame.mouse.get_pos()
        if self.rectangle.collidepoint(mouse_pos):
            cursor.move_to(button=self)
            self.color = self.template.hover_color
        else:
            self.color = self.template.bg_color

    def check_input(self, mouse_mode: bool = True):
        if not mouse_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.state = Buttons.armed
            elif self.state == Buttons.armed:
                self.state = Buttons.idle
                return True
            return False
        else:
            mouse_pos = pygame.mouse.get_pos()
            if self.rectangle.collidepoint(mouse_pos):
                self.color = self.template.hover_color
                if pygame.mouse.get_pressed()[0]:
                    self.state = Buttons.armed
                elif self.state == Buttons.armed:
                    self.state = Buttons.idle
                    return True
            else:
                self.color = self.template.bg_color
                self.state = Buttons.idle
            return False

    def draw(self, screen):
        if self.outline_rect:
            pygame.draw.rect(screen, self.template.outline_color, self.outline_rect, border_radius = self.template.outline_radius)
        pygame.draw.rect(screen, self.color, self.rectangle , border_radius= self.template.border_radius)

    def get_attributes(self):
        return (self.rectangle.center, (self.rectangle.width, self.rectangle.height))




class TextButtons(Buttons):
    def __init__(self, text : str, template :ButtonTemplate, font, size: list, pos: list,sc_size: list = (1, 1)) -> None:
        super().__init__(template, size, pos, sc_size)
        self.text = text
        self.resize(sc_size,font)
    
    def resize(self, sc_size : tuple, font : pygame.font.Font):
        super().set_size(sc_size)
        self.tex_surf = font.render(self.text, True, self.template.text_color)
        self.text_rect = self.tex_surf.get_rect(center=self.rectangle.center)
    
    def draw(self,surface : pygame.Surface):
        super().draw(surface)
        surface.blit(self.tex_surf, self.text_rect)  
        
        
class Arrow(Buttons):
    def __init__(self, direction : str, template : ButtonTemplate, size: list, pos: list, sc_size: list = (1, 1)):
        super().__init__(template, size, pos, sc_size)
        self.direction = direction
        self.set_vertecies(sc_size[0],sc_size[1])
        
      
    def set_vertecies(self, width, height) -> None:
        x = self.pos[0]
        y = self.pos[1]
        size = self.size
        offset = 10
        self.vertecies = []
        if self.direction == "left":
                self.vertecies=[
                    (round((x) * width + offset), round((y + size[1] / 2) * height)),
                    (round((x + size[0]) * width - offset), round(y * height + offset )),
                    (round((x + size[0]) * width - offset), round((y + size[1]) * height - offset )),
                ]
        elif self.direction == "right":
                self.vertecies = [
                    (round((x) * width + offset ), round(y * height + offset )),
                    (round((x + size[0]) * width - offset ), round((y + size[1] / 2) * height)),
                    (round(x * width + offset ), round((y + size[1]) * height - offset )),
                ]
        else:
            raise Exception("Direction must be str and either top, bottom, left or right")
        self.rectangle = pygame.Rect(
            self.pos[0] * width,
            self.pos[1] * height,
            self.size[0] * width,
            self.size[1] * height,
        )
        
    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        pygame.gfxdraw.aapolygon(surface,self.vertecies,self.template.outline_color)
        pygame.draw.polygon(surface,self.template.outline_color,self.vertecies)
            