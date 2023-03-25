from block import block
import random,pygame
from game_parameters import *

class Tetraminos:
    def __init__(self,pivot_pos:pygame.Vector2)->None:
        self.pivot=pivot_pos
        self.blocks=[block((pos+self.pivot),cell_size,False) for pos in shapes["I"]]
        self.update_time=1000
        self.direction_update=0
        self.last_update_time=0
        self.direction=v(0,0)


    def update(self,current_time: int ,event:pygame.Event)->None:
        update=False
        if current_time-self.last_update_time>self.update_time:
            self.last_update_time=current_time
            self.pivot[1]+=1
            update=True
        for block in self.blocks:
            block.update(update)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                self.rotate()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and current_time-self.u>75:
            self.direction_update=current_time
            self.move(moves["right"])
        if keys[pygame.K_LEFT] and current_time-self.u>75:
            self.direction_update=current_time
            self.move(moves["left"])


            
    def move(self,direction:pygame.Vector2):
        self.pivot+=direction
        for block in self.blocks:
            block.move(direction) 
        
    def draw(self,window:pygame.Surface):
        for cube in self.blocks:
            cube.draw(window)
          
    def rotate(self)->None:
        for cube in self.blocks:
            temp=cube.map_pos-self.pivot
            cube.map_pos[0]=(temp[0]*cos_90-temp[1]*sin_90)+self.pivot[0]
            cube.map_pos[1]=((temp[1])*cos_90+(temp[0])*sin_90)+self.pivot[1]
