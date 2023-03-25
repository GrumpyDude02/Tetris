from block import block
import random
from game_parameters import *

class Tetrominos:
    def __init__(self,pivot_pos):
        self.pivot=pivot_pos
        self.blocks=[block((pos+self.pivot),cell_size,False) for pos in shapes["L"]]
        self.update_time=1000
        self.last_update_time=0


    def update(self,current_time,direction):
        update=False
        if current_time-self.last_update_time>self.update_time:
            self.last_update_time=current_time
            self.pivot[1]+=1
            update=True
        self.pivot+=direction
        for cube in self.blocks:
            cube.update(update,direction)
            
    def move(self,direction):
        for block in self.blocks:
            block.move(direction) 
        
    def draw(self,window):
        for cube in self.blocks:
            cube.draw(window)
          
    def rotate(self,angle):
        match angle:
            case 0:
                cos_a=cos_n90
                sin_a=sin_n90
            case 1:
                cos_a=cos_90
                sin_a=sin_90
        for cube in self.blocks:
            temp=cube.map_pos-self.pivot
            print(temp)
            print(temp)
            cube.map_pos[0]=(temp[0]*cos_a-temp[1]*sin_a)+self.pivot[0]
            cube.map_pos[1]=((temp[1])*cos_a+(temp[0])*sin_a)+self.pivot[1]
