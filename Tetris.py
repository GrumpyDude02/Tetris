import pygame,sys
from game_parameters import *
from Tetrominos import *
from functions import *
from copy import deepcopy 

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE|pygame.DOUBLEBUF)
clock = pygame.time.Clock()
font=pygame.font.Font("kimberley bl.otf",30)
NEXT=font.render("NEXT :",True,(255,255,255))
HOLD=font.render("HOLD :",True,(255,255,255))

#-----------initial setup--------------
cleared_lines=0
total_cleared_lines=0
level=1
dt=1/FPS
tetrominos=[]
shapes_list=list(shapes.keys())
display_surface=pygame.Surface((5*cell_size,4*cell_size))
hold_surface=pygame.Surface((5*cell_size,4*cell_size))
shadow_surface=pygame.Surface((WIDTH,HEIGHT),pygame.HWSURFACE)
pygame.key.set_repeat(0,0)
append=True
index=1
switch_available=True
current_piece=Tetrominos([5,1],shapes_list[0],cell_size-1)
next_tetromino_shape=shapes_list[index]
next_tetromino=Tetrominos([1.5,1.5+shift],next_tetromino_shape,cell_size-1)
held_piece=None


shadow_surface.set_colorkey(0)
shadow_surface.set_alpha(150)


#---------main loop---------- 
while (1):
    destroy=[]
    
    #checking game state to reset the game
    if game_over(placed_blocks):
        current_piece.isSet=False
        held_piece=None
        cleared_lines=0
        total_cleared_lines=0
        level=0
        reset_board(placed_blocks,tetrominos)
        
    #filling surfaces 
    screen.fill((0, 0, 0))
    display_surface.fill((255,255,255))
    shadow_surface.fill((0,0,0))
    hold_surface.fill((255,255,255))
    draw_grid(screen,grid,(96,96,96))
    
    #checking for events
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        sys.exit()
        
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_h:
            if held_piece is None:
                held_piece=deepcopy(current_piece)
                held_piece.change_pos([1.5,1.5+shift])
                current_piece.isSet=True
                switch_available=False
                append=False
            elif switch_available:
                temp=held_piece
                held_piece=current_piece
                current_piece=temp
                held_piece.change_pos([1.5,1.5+shift])
                current_piece.change_pos([5,0])
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
        current_piece=Tetrominos([5,1],next_tetromino_shape,cell_size-1)
        next_tetromino_shape=shapes_list[index]
        prev=next_tetromino_shape
        next_tetromino=Tetrominos([1.5,1.5+shift],next_tetromino_shape,cell_size-1)
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
    
    levelCountRender=font.render(f'LEVEL : {level}',True,(255,255,255))
    screen.blit(levelCountRender,(12*cell_size,18*cell_size))
    screen.blit(display_surface,(13*cell_size,5*cell_size))
    screen.blit(hold_surface,(13*cell_size,12*cell_size))
    screen.blit(shadow_surface,(0,0))
    screen.blit(NEXT,(13*cell_size,3*cell_size))
    screen.blit(HOLD,(13*cell_size,10*cell_size))
    dt=clock.tick(FPS)/1000

    #removing tetrominos that have no blocks left 
    if destroy:
        for item in destroy:
            tetrominos.remove(item)
    pygame.display.flip()
