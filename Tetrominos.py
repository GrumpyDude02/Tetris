from block import block
import random,pygame
from game_parameters import *

class Tetrominos:
    def __init__(self,color:pygame.color,pivot_pos:pygame.Vector2,cooldown:int)->None:
        self.isSet=False
        self.pivot=pivot_pos
        self.blocks=[block((pos+self.pivot),cell_size,color,self) for pos in shapes["I"]]#random.choice(list(shapes.values()))]
        self.update_time=cooldown
        self.destroy=False
        self.direction_update=0
        self.last_update_time=0
        self.direction=v(0,0)

    def update(self,current_time : int,event : pygame.Event)->None:
        if not self.blocks:
            self.destroy=True
        if self.isSet:
            return
        if current_time-self.last_update_time>self.update_time :
            self.last_update_time=current_time
            self.move(moves["down"])
        keys=pygame.key.get_pressed()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                self.rotate()
            if keys[pygame.K_DOWN]:
                self.direction_update=current_time
                self.move(moves["down"])
            elif keys[pygame.K_LEFT]:
                self.direction_update=current_time
                self.move(moves["left"])
            elif keys[pygame.K_RIGHT]:
                self.direction_update=current_time
                self.move(moves["right"])
            
    def move(self,direction:pygame.Vector2)->None:
        if not self.collide(direction):
            for block in self.blocks:
                block.move(direction)
            self.pivot+=direction     
        elif direction==moves["down"]:
            self.isSet=True
            for block in self.blocks:
                placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])]=block


    def collide(self,dir:pygame.Vector2)->bool:
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
            block.map_pos[0]=round(temp[0]*cos_90-temp[1]*sin_90+self.pivot[0])
            block.map_pos[1]=round((temp[1])*cos_90+(temp[0])*sin_90+self.pivot[1])
        outside_right_block=max(self.blocks,key= lambda x: x.map_pos[0])
        
        outside_y_axis=max(self.blocks,key=lambda x:x.map_pos[1])
        if outside_right_block.map_pos[0]>=playable_num:
            shift_l=outside_right_block.map_pos[0]-playable_num+1
            self.pivot[0]-=shift_l
            for block in self.blocks:
                block.map_pos[0]-=shift_l
        outside_left_block=min(self.blocks,key=lambda x:x.map_pos[0])
        if outside_left_block.map_pos[0]<0:
            shift_r=-(outside_left_block.map_pos[0])
            self.pivot[0]+=shift_r
            for block in self.blocks:
                block.map_pos[0]+=shift_r
        if outside_y_axis.map_pos[1]>=v_cell_number:
            shift_y=outside_y_axis.map_pos[1]-v_cell_number+1
            self.pivot[1]-=shift_y
            for block in self.blocks:
                block.map_pos[1]-=shift_y
