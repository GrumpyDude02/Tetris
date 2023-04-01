from block import block
import random,pygame
from game_parameters import *

class Tetrominos:
    def __init__(self,color:pygame.color,pivot_pos:pygame.Vector2,cooldown:int)->None:
        self.isSet=False
        self.pivot=pivot_pos
        self.blocks=[block((pos+self.pivot),cell_size,color) for pos in shapes["I"]]#random.choice(list(shapes.values()))]
        self.update_time=cooldown
        self.direction_update=0
        self.last_update_time=0
        self.direction=v(0,0)

    def update(self,current_time : int,event : pygame.Event)->None:
        if self.isSet:
            return
        if current_time-self.last_update_time>self.update_time :
            self.last_update_time=current_time
            self.move(moves["down"])
        keys=pygame.key.get_pressed()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                self.rotate()
        if current_time-self.direction_update>FPS+20:
            if keys[pygame.K_DOWN]:
                self.direction_update=current_time
                self.move(moves["down"])
            elif keys[pygame.K_RIGHT]:
                self.direction_update=current_time
                self.move(moves["right"])
            elif keys[pygame.K_LEFT]:
                self.direction_update=current_time
                self.move(moves["left"])
            
    def move(self,direction:pygame.Vector2)->None:
        if self.collide(direction):
            if direction==moves["down"]:
                self.isSet=True
            return 
        for block in self.blocks:
            block.move(direction)
        self.pivot+=direction

    def collide(self,dir:pygame.Vector2)->list[bool]:
        for block in self.blocks:
            if block.collide(block.map_pos+dir):
                return True
        return False
            
    
    def draw(self,window:pygame.Surface)->None:
        for cube in self.blocks:
            cube.draw(window)
     
         
    def rotate(self)->None:
        for block in self.blocks:
            temp=block.map_pos-self.pivot
            block.map_pos[0]=(temp[0]*cos_90-temp[1]*sin_90)+self.pivot[0]
            block.map_pos[1]=((temp[1])*cos_90+(temp[0])*sin_90)+self.pivot[1]
        outside_right_block=max(self.blocks,key= lambda x: x.map_pos[0])
        outside_left_block=min(self.blocks,key=lambda x:x.map_pos[0])
        outside_y_axis=max(self.blocks,key=lambda x:x.map_pos[1])
        if outside_right_block.map_pos[0]>=playable_num:
            shift_l=outside_right_block.map_pos[0]-playable_num+1
            print(shift_l)
            self.pivot[0]-=shift_l
            for block in self.blocks:
                block.map_pos[0]-=shift_l
        if outside_left_block.map_pos[0]<0:
            shift_r=abs(outside_left_block.map_pos[0])
            self.pivot[0]+=shift_r
            for block in self.blocks:
                block.map_pos[0]+=shift_r
        if outside_y_axis.map_pos[1]>=v_cell_number:
            shift_y=outside_y_axis.map_pos[1]-v_cell_number+1
            self.pivot[1]-=shift_y
            for block in self.blocks:
                block.map_pos[1]-=shift_y
