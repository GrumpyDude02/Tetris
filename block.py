import pygame
from pygame.math import Vector2 as v
from game_parameters import *

class block:
    def __init__(self,pos,cell_size,color):
        self.map_pos=v(pos[0],pos[1])
        self.width=cell_size
        self.r_pos=self.map_pos*cell_size
        self.color=color
        self.time=0    
    
    def update(self,flag):
        if flag:
            self.map_pos[1]+=1

    def move(self,direction):
        self.map_pos+=direction
        
    def draw(self,window):
        self.r_pos=v(self.map_pos[0]*cell_size,self.map_pos[1]*cell_size)
        pygame.draw.rect(window,self.color,pygame.Rect(self.r_pos[0],self.r_pos[1],cell_size,cell_size))

    def collide(self)->bool:
        if self.map_pos.x>playable_num or self.map_pos.x<0 :
            return True
        return False