import pygame
from pygame.math import Vector2 as v
from game_parameters import *

class block:
    def __init__(self,pos:pygame.Vector2,cell_size:int,color:pygame.color)->None:
        self.map_pos=v(pos[0],pos[1])
        self.width=cell_size
        self.r_pos=self.map_pos*cell_size
        self.color=color
        self.time=0    
    
    def update(self)->None:
        self.map_pos[1]+=1

    def move(self,direction:pygame.Vector2)->None:
        self.map_pos+=direction
       
    def draw(self,window:pygame.Surface)->None:
        self.r_pos=v(self.map_pos[0]*cell_size,self.map_pos[1]*cell_size)
        pygame.draw.rect(window,self.color,pygame.Rect(self.r_pos[0],self.r_pos[1],cell_size,cell_size))

    def collide(self,dir:pygame.Vector2)->list:
        if (self.map_pos.x+dir.x>=playable_num or self.map_pos.x+dir.x<=-1) and self.map_pos.y+dir.y>=v_cell_number:
            return (True,True)
        elif self.map_pos.x+dir.x>=playable_num or self.map_pos.x+dir.x<=-1:
            return (True,False)
        elif self.map_pos.y+dir.y>=v_cell_number:
            return (False,True)
        return (False,False)