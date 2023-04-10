from block import block
import pygame
from copy import deepcopy
from game_parameters import *
from functions import mod

class Tetrominos:
    def __init__(self,pivot_pos:pygame.Vector2,cooldown:int,shape:str,block_width)->None:
        self.isSet=False
        self.pivot=pivot_pos
        self.shape=shape
        self.color=shapes[self.shape][1]
        self.rotation_index=0
        self.blocks=[block((pos+self.pivot),block_width,self.color,self) for pos in shapes[self.shape][0]]
        self.update_time=cooldown
        self.destroy=False
        self.direction_update=0
        self.last_update_time=0
        self.direction=v(0,0)
        self.offset_list=None
        if self.shape!='I' and self.shape!='O':
            self.offset_list=offsets_JLZST
        elif self.shape=='I':
            self.offset_list=offsets_I

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
                self.SRS_Rotate(True,1)
            elif event.key==pygame.K_z:
                self.SRS_Rotate(False,1)
            elif event.key==pygame.K_a:
                self.SRS_Rotate(True,2)
            elif event.key==pygame.K_DOWN:
                self.direction_update=current_time
                self.move(moves["down"])
            elif event.key==pygame.K_LEFT:
                self.direction_update=current_time
                self.move(moves["left"])
            elif event.key==pygame.K_RIGHT:
                self.direction_update=current_time
                self.move(moves["right"])
            elif event.key==pygame.K_SPACE:
                self.move(moves["snap"])    
           
    def move(self,direction:pygame.Vector2)->None:
        if direction==moves["snap"]:
            translate=self.project()
            for block in self.blocks:
                block.map_pos[1]+=translate-1
                placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])]=block
            self.isSet=True
        elif not self.collide(direction):
            for block in self.blocks:
                block.move(direction)
            self.pivot+=direction     
        elif direction==moves["down"]:
            for block in self.blocks:
                placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])]=block
            self.isSet=True
          
    def project(self)->int:
        translate=0
        while(translate<v_cell_number):
            if any(int(block.map_pos[1])+translate >= v_cell_number or placed_blocks[int(block.map_pos[1])+translate][int(block.map_pos[0])] for block in self.blocks):
                break
            translate+=1
        return translate
           
    def collide(self,dir:pygame.Vector2)->bool:
        for block in self.blocks:
            if block.collide(block.map_pos+dir):
                return True
        return False            
    
    
    def draw(self,window:pygame.Surface,shadow_surf:pygame.Surface,hold:bool)->None:
        for block in self.blocks:
            block.draw(window)
        if hold:
            return
        if hold or not self.isSet:
            shadow=deepcopy(self)
            translate=self.project()
            for block in shadow.blocks:
                block.map_pos[1]+=translate-1
                block.draw(shadow_surf)
    
#classic rotation but with wall kicks  
    def rotate(self,clockwise : bool)->None:
        if self.shape=="O":
            return
        old=deepcopy(self.blocks)
        rot=(cos_90,sin_90) if clockwise else (cos_n90,sin_n90)
        for block in self.blocks:
            temp=block.map_pos-self.pivot
            block.map_pos[0]=round(temp[0]*rot[0]-temp[1]*rot[1]+self.pivot[0])
            block.map_pos[1]=round((temp[1])*rot[0]+temp[0]*rot[1]+self.pivot[1])
        self.rotation_index=mod(self.rotation_index,4)   
        outside_right_block=max(self.blocks,key= lambda x: x.map_pos[0])
        outside_left_block=min(self.blocks,key=lambda x:x.map_pos[0])
        outside_y_axis=max(self.blocks,key=lambda x:x.map_pos[1])
        if outside_right_block.map_pos[0]>=playable_num:
            shift_l=outside_right_block.map_pos[0]-playable_num+1
            self.pivot[0]-=shift_l
            for block in self.blocks:
                block.map_pos[0]-=shift_l
        elif outside_left_block.map_pos[0]<0:
            shift_r=-(outside_left_block.map_pos[0])
            self.pivot[0]+=shift_r
            for block in self.blocks:
                block.map_pos[0]+=shift_r
        elif outside_y_axis.map_pos[1]>=v_cell_number:
            shift_y=outside_y_axis.map_pos[1]-v_cell_number+1
            self.pivot[1]-=shift_y
            for block in self.blocks:
                block.map_pos[1]-=shift_y
        for block in self.blocks:
            if block.overlap(block.map_pos):
                self.blocks=old
                return  
  
#Super Rotation System  
    def SRS_Rotate(self,clockwise:bool,turns)->None:
        if self.shape=="O":
            return
        old_blocks=deepcopy(self.blocks)
        old_r_index=self.rotation_index
        self.rotation_index=mod(self.rotation_index+turns,4) if clockwise else mod(self.rotation_index-turns,4)
        rot=1 if clockwise else -1
        for i in range(0,turns):
            for block in self.blocks:
                temp=block.map_pos-self.pivot
                block.map_pos[0]=round(-temp[1]*rot+self.pivot[0])
                block.map_pos[1]=round(temp[0]*rot+self.pivot[1])
        for i in range(0,5):
            offset=self.offset_list[old_r_index][i]-self.offset_list[self.rotation_index][i]
            if not self.collide(offset):
                self.pivot+=offset
                for block in self.blocks:
                    block.move(offset)
                return
        self.blocks=old_blocks
        self.rotation_index=old_r_index
       
            
    def change_pos(self,new_pos:pygame.Vector2)->None:
        for block in self.blocks:
            block.map_pos-=self.pivot
            block.map_pos+=new_pos
        self.pivot=new_pos