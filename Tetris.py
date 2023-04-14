import pygame,sys
from game_parameters import *
from Tetrominos import *
from functions import *
from copy import deepcopy 

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.DOUBLEBUF)
clock = pygame.time.Clock()
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,100,255)
font=pygame.font.Font("kimberley bl.otf",24)
NEXT=font.render("NEXT :",True,WHITE)
HOLD=font.render("HOLD :",True,WHITE)
PAUSED=font.render("PAUSED",True,WHITE)
SC_RECT=pygame.Rect(0,0,WIDTH,HEIGHT)
font_rect=PAUSED.get_rect()
font_rect.center=SC_RECT.center
BLOCK_SIZE=cell_size-1


#-----------initial varibale values--------------
cleared_lines=0
spawn_column=3
total_cleared_lines=0
level=1
dt=1/FPS
tetrominos=[]
shapes_list=list(shapes.keys())
index=0
held_piece=None

#------------surfaces-------------
display_surface=pygame.Surface((6*cell_size,5.5*cell_size))
hold_surface=pygame.Surface((6*cell_size,6*cell_size))
shadow_surface=pygame.Surface((WIDTH,HEIGHT),pygame.HWACCEL)
pause_surface=pygame.Surface((WIDTH,HEIGHT),pygame.HWACCEL)

pause_surface.set_colorkey(0)
shadow_surface.set_colorkey(0)
shadow_surface.set_alpha(100)
pause_surface.set_alpha(150)

pygame.draw.rect(pause_surface,BLUE,SC_RECT)
#pygame.key.set_repeat(0,0)

#----------flags------------
append=True
switch_available=True
reset=False
paused=False

#-----------------------------
current_piece=Tetrominos([5,spawn_column],shapes_list[0],BLOCK_SIZE)
next_tetromino_shape=shapes_list[index]
next_tetromino=Tetrominos([1.5,1.5+shift+1],next_tetromino_shape,BLOCK_SIZE)






#---------main loop---------- 
while (1):
    destroy=[]
    
    #checking game state to reset the game
    if game_over(placed_blocks,spawn_column) or reset:
        random.shuffle(shapes_list)
        index=0
        current_piece=Tetrominos([5,spawn_column],shapes_list[0],BLOCK_SIZE)
        index+=1
        next_tetromino_shape=shapes_list[index]
        next_tetromino=Tetrominos([1.5,1.5+shift+1],next_tetromino_shape,BLOCK_SIZE)
        held_piece=None
        cleared_lines=0
        total_cleared_lines=0
        level=0
        reset_board(placed_blocks,tetrominos)
        
    reset=False 
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
        if event.key==pygame.K_h and not paused:
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
        if event.key==pygame.K_r and not paused:
            reset=True
        if event.key==pygame.K_ESCAPE:
            paused=not paused
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
         
        
    #updating elements
    if paused:
        blured_surf=blurSurf(screen,10)
        #For newer version of pygame
        #blured_surf=pygame.transform.gaussian_blur(screen,10)
        screen.blit(blured_surf,(0,0))
        screen.blit(pause_surface,(0,0))
        screen.blit(PAUSED,font_rect)
        dt=clock.tick(FPS)/1000
        pygame.display.flip()
        continue
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
        next_tetromino=Tetrominos([1.5,1.5+shift+1],next_tetromino_shape,BLOCK_SIZE)
        append=True
    current_piece.update(pygame.time.get_ticks(),dt,event,level)
    
    #checking any full lines
    cleared_lines=check_line(placed_blocks,playable_num)
    total_cleared_lines+=cleared_lines
    if total_cleared_lines>=10*(level):
        level+=1
        level=min(level,15)
        
    #removing tetrominos that have no blocks left 
    dt=clock.tick(FPS)/1000
    pygame.display.flip()
    if destroy:
        for item in destroy:
            tetrominos.remove(item)
