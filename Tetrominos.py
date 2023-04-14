from block import block
import pygame
from copy import deepcopy
from game_parameters import *
from functions import mod

lock_delay=500
shared_lock_timer=0
down_pressed=False
successful_move=True

class Tetrominos:
    def __init__(self,pivot_pos:pygame.Vector2,shape:str,block_width)->None:
        self.isSet=False
        self.pivot=pivot_pos
        self.shape=shape
        self.color=shapes[self.shape][1]
        self.rotation_index=0
        self.blocks=[block((pos+self.pivot),block_width,self.color,self) for pos in shapes[self.shape][0]]
        self.center=self.blocks[0]
        self.acc=0
        self.destroy=False
        self.keys_held=[False,False]
        self.HUpdate=0
        self.VUpdate=0
        self.key_held_time=0
        self.offset_list=None
        if self.shape!='I' and self.shape!='O':
            self.offset_list=offsets_JLZST
        elif self.shape=='I':
            self.offset_list=offsets_I
        
    def update(self,current_time,dt : int,event : pygame.Event,level)->None:
        global down_pressed
        down_pressed=False
        self.acc+=level_speed[level-1]*dt*game_speed
        if not self.blocks:
            self.destroy=True
        if self.isSet:
            return
        if self.acc>1 :
            self.acc=0
            self.move(moves["down"],current_time)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and current_time-self.VUpdate>MOVE_DELAY:
            down_pressed=True
            self.VUpdate=current_time
            self.move(moves["down"],current_time)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                self.SRS_Rotate(True,1)
            elif event.key==pygame.K_z:
                self.SRS_Rotate(False,1)
            elif event.key==pygame.K_a:
                self.SRS_Rotate(True,2)
            elif event.key==pygame.K_SPACE:
                self.move(moves['snap'],current_time)
            elif event.key==pygame.K_LEFT:
                self.keys_held[0]=True
                self.key_held_time=0
                self.move(moves['left'],current_time)
            elif event.key==pygame.K_RIGHT:
                self.keys_held[1]=True
                self.key_held_time=0
                self.move(moves['right'],current_time)
        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                self.keys_held[0]=False
                self.key_held_time=0
            if event.key==pygame.K_RIGHT:
                self.keys_held[1]=False
                self.key_held_time=0
        if self.keys_held[1]:
            self.key_held_time+=1
            if self.key_held_time>15:
                if keys[pygame.K_RIGHT] and current_time-self.HUpdate>MOVE_DELAY:
                    self.HUpdate=current_time
                    self.move(moves['right'],current_time)
        elif self.keys_held[0]:
            self.key_held_time+=1
            if self.key_held_time>15:
                if keys[pygame.K_LEFT] and current_time-self.HUpdate>MOVE_DELAY:
                    self.HUpdate=current_time
                    self.move(moves['left'],current_time)
            
            
           
    def move(self,direction:pygame.Vector2,current_time)->None:
        global shared_lock_timer,down_pressed,successful_move
        if direction==moves['snap']:
            translate=self.project()
            for block in self.blocks:
                block.map_pos[1]+=translate-1
                placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])]=block
            self.isSet=True
        elif not self.collide(direction):
            shared_lock_timer=current_time
            successful_move=True
            for block in self.blocks:
                block.move(direction)
            self.pivot+=direction  
        elif direction==moves['left'] or direction==moves['right']:
            successful_move=False 
        elif direction==moves['down']:
            if down_pressed or not successful_move or current_time-shared_lock_timer>lock_delay :
                self.set_blocks(placed_blocks)
            
          
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
    
    
    def draw(self,window:pygame.Surface,shadow_surf:pygame.Surface)->None:
        for block in self.blocks:
            if block.map_pos-self.pivot==v():
                block.draw(window)
            else:
                block.draw(window)
        if shadow_surf is None:
            return
        if not self.isSet:
            pygame.draw.circle(window,(255,255,255),self.center.r_pos+v(self.center.width/2,self.center.width/2),2)
            shadow=deepcopy(self)
            translate=self.project()
            for block in shadow.blocks:    
                block.map_pos[1]+=translate-1
                block.draw(shadow_surf)
    
#classic rotation but with wall kicks(boundaries only)  
    def rotate(self,clockwise : bool)->None:
        if self.shape=="O":
            return
        old=deepcopy(self.blocks)
        rot=(1,0) if clockwise else (-1,0)
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
        global shared_lock_timer
        if self.shape=="O":
            return
        old_blocks=deepcopy(self.blocks)
        old_r_index=self.rotation_index
        self.rotation_index=mod(self.rotation_index+turns,4) if clockwise else mod(self.rotation_index-turns,4)
        rot=1 if clockwise else -1
        for i in range(0,turns):
            for block in self.blocks:
                temp=block.map_pos-self.pivot
                block.map_pos[0]=(-temp[1]*rot+self.pivot[0])
                block.map_pos[1]=(temp[0]*rot+self.pivot[1])
        for i in range(0,5):
            offset=self.offset_list[old_r_index][i]-self.offset_list[self.rotation_index][i]
            if not self.collide(offset):
                shared_lock_timer=pygame.time.get_ticks()
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
        
    def set_blocks(self,placed_blocks):
        self.isSet=True
        for block in self.blocks:
            placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])]=block 