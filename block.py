import pygame
from pygame.math import Vector2 as v
from game_parameters import *

class block:
    def __init__(self,pos,cell_size,isEmpty):
        self.map_pos=v(pos[0],pos[1])
        self.width=cell_size
        self.r_pos=self.map_pos*cell_size
        if isEmpty:
            self.color=(0,0,0)
        else:
            self.color=(255,255,255)
        self.time=0    
    
    def update(self,flag,direction):
        if flag:
            self.map_pos[1]+=1
        self.move(direction)
        
    def move(self,direction):
        self.map_pos+=direction
        
    def draw(self,window):
        self.r_pos=v(self.map_pos[0]*cell_size,self.map_pos[1]*cell_size)
        pygame.draw.rect(window,(0,0,0),pygame.Rect(self.r_pos[0],self.r_pos[1],cell_size,cell_size))
