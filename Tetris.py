import pygame,sys
from game_parameters import *
from Tetrominos import *
from functions import *
from copy import deepcopy 

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE|pygame.DOUBLEBUF)
clock = pygame.time.Clock()
BLACK=(0,0,0)
WHITE=(255,255,255)
font=pygame.font.Font("kimberley bl.otf",24)
NEXT=font.render("NEXT :",True,WHITE)
HOLD=font.render("HOLD :",True,WHITE)
BLOCK_SIZE=cell_size-1


#-----------initial setup--------------
cleared_lines=0
spawn_column=4
total_cleared_lines=0
level=15
dt=1/FPS
tetrominos=[]
shapes_list=list(shapes.keys())
display_surface=pygame.Surface((6*cell_size,5.5*cell_size))
hold_surface=pygame.Surface((6*cell_size,6*cell_size))
shadow_surface=pygame.Surface((WIDTH,HEIGHT),pygame.HWSURFACE)
pygame.key.set_repeat(0,0)
append=True
index=1
switch_available=True
current_piece=Tetrominos([5,spawn_column],shapes_list[0],BLOCK_SIZE)
next_tetromino_shape=shapes_list[index]
next_tetromino=Tetrominos([1.5,1.5+shift+1],next_tetromino_shape,BLOCK_SIZE)
held_piece=None


shadow_surface.set_colorkey(0)
shadow_surface.set_alpha(100)


#---------main loop---------- 
while (1):
    destroy=[]
    
    #checking game state to reset the game
    if game_over(placed_blocks,spawn_column):
        random.shuffle(shapes_list)
        index=0
        current_piece=Tetrominos([5,spawn_column],shapes_list[0],BLOCK_SIZE)
        held_piece=None
        cleared_lines=0
        total_cleared_lines=0
        level=0
        reset_board(placed_blocks,tetrominos)
        
    #filling surfaces 
    screen.fill(BLACK)
    display_surface.fill(BLACK)
    hold_surface.fill(BLACK)
    shadow_surface.fill(BLACK)
    
    #checking for events
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        sys.exit()
        
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_h:
            if held_piece is None:
                held_piece=deepcopy(current_piece)
                held_piece.change_pos([1.5,1.5+shift+1])
                current_piece.isSet=True
                switch_available=False
                append=False
            elif switch_available:
                temp=held_piece
                held_piece=current_piece
                current_piece=temp
                held_piece.change_pos([1.5,1.5+shift+1])
                current_piece.change_pos([5,spawn_column])
                switch_available=False
                
        
    #drawing elements on screen 
    if current_piece.isSet:
        index+=1
        index%=7
        if index==0:
            random.shuffle(shapes_list)
        if append:
            tetrominos.append(current_piece)
            switch_available=True
        else:
            switch_available=False
        current_piece=Tetrominos([5,spawn_column],next_tetromino_shape,BLOCK_SIZE)
        next_tetromino_shape=shapes_list[index]
        prev=next_tetromino_shape
        next_tetromino=Tetrominos([1.5,1.5+shift+1],next_tetromino_shape,BLOCK_SIZE)
        append=True
    
    current_piece.update(pygame.time.get_ticks(),dt,event,level)
    
    #checking any full lines
    cleared_lines=check_line(placed_blocks,playable_num)
    total_cleared_lines+=cleared_lines
    if total_cleared_lines>=10*(level):
        level+=1
        level=min(level,15)
        
    #bliting elements surfaces on the main screen(find a system to place ui elements)
    for tetromino in tetrominos:
        tetromino.draw(screen,None)
        if tetromino.destroy:
            destroy.append(tetromino)
            
    current_piece.draw(screen,shadow_surface)
    next_tetromino.draw(display_surface,None)
    if held_piece is not None:
        held_piece.draw(hold_surface,None)
    levelCountRender=font.render(f'LEVEL : {level}',True,WHITE)
    lines=font.render(f'LINES : {total_cleared_lines}',True,WHITE)
    screen.blit(display_surface,(13*cell_size,4*cell_size))
    screen.blit(hold_surface,(13*cell_size,12*cell_size))
    screen.blit(shadow_surface,(0,0))
    
    draw_grid(screen,grid,(96,96,96))
    
    screen.blit(NEXT,(13*cell_size,2*cell_size))
    screen.blit(HOLD,(13*cell_size,10*cell_size))
    screen.blit(levelCountRender,(13*cell_size,19*cell_size))
    screen.blit(lines,(13*cell_size,21*cell_size))
    dt=clock.tick(FPS)/1000

    #removing tetrominos that have no blocks left 
    if destroy:
        for item in destroy:
            tetrominos.remove(item)
    pygame.display.flip()
