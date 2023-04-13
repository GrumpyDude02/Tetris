import pygame
from pygame.math import Vector2 as v
from game_parameters import *

class block:
    def __init__(self,pos:pygame.Vector2,cell_size:int,color:pygame.color,tetromino)->None:
        self.map_pos=v(pos[0],pos[1])
        self.width=cell_size
        self.r_pos=self.map_pos*cell_size
        self.color=color
        self.tetromino=tetromino
    
    def update(self)->None:
        self.map_pos[1]+=1

    def move(self,direction:pygame.Vector2)->None:
        self.map_pos+=direction
       
    def draw(self,window:pygame.Surface,shadow:bool)->None:
        self.r_pos=v((self.map_pos[0]+vShift-1)*cell_size,(self.map_pos[1]-y_border_offset-1)*cell_size)
        pygame.draw.rect(window,self.color,pygame.Rect(self.r_pos[0],self.r_pos[1],self.width,self.width))

    
    def overlap(self,pos):
        if int(pos.y<=1):
            return False
        return bool(placed_blocks[int(pos.y)][int(pos.x)])

    def in_bounds(self,pos):
        return (0<=pos.x<playable_num) and pos.y<v_cell_number
    
    def collide(self,pos:pygame.Vector2)->bool:
        if self.in_bounds(pos) and not self.overlap(pos):
            return False
        return True