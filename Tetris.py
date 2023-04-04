import pygame,sys
from game_parameters import *
from Tetrominos import *
from functions import *
from copy import deepcopy 

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

#-----------initial setup--------------
tetrominos=[]
display_surface=pygame.Surface((5*cell_size,4*cell_size))
hold_surface=pygame.Surface((5*cell_size,4*cell_size))
shadow_surface=pygame.Surface((WIDTH,HEIGHT),pygame.HWSURFACE)
pygame.key.set_repeat(0,0)
append=True
current_piece=Tetrominos([5,0],500,random.choice(list(shapes.keys())))
next_tetromino_shape=random.choice(list(shapes.keys()))
next_tetromino=Tetrominos([1.5,1.5+shift],500,next_tetromino_shape)
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
        reset_game(placed_blocks,tetrominos)
        
    #filling surfaces 
    screen.fill((0, 0, 0))
    display_surface.fill((255,255,255))
    shadow_surface.fill((0,0,0))
    hold_surface.fill((255,255,255))
    next_tetromino.draw(display_surface,shadow_surface,True)
    if held_piece is not None:
        held_piece.draw(hold_surface,shadow_surface,True)
    
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
                append=False
            else:
                temp=held_piece
                held_piece=current_piece
                current_piece=temp
                held_piece.change_pos([1.5,1.5+shift])
                current_piece.change_pos([5,0])
                
        
    #drawing elements on screen 
    if current_piece.isSet:
        if append:
            tetrominos.append(current_piece)
        current_piece=Tetrominos([5,0],500,next_tetromino_shape)
        next_tetromino_shape=random.choice(list(shapes.keys()))
        next_tetromino=Tetrominos([1.5,1.5+shift],500,next_tetromino_shape)
        append=True
        
    draw_grid(screen,grid,(255,255,255))
    current_piece.draw(screen,shadow_surface,False)
    current_piece.update(pygame.time.get_ticks(),event)
    
    for tetromino in tetrominos:
        tetromino.draw(screen,shadow_surface,False)
        if tetromino.destroy:
            destroy.append(tetromino)
    
    #checking any full lines
    check_line(placed_blocks,playable_num)
    
    #bliting elements surfaces on the main screen
    screen.blit(display_surface,(13*cell_size,5*cell_size))
    screen.blit(hold_surface,(13*cell_size,10*cell_size))
    screen.blit(shadow_surface,(0,0))
    clock.tick(FPS)
    
    #removing tetrominos that have no blocks left 
    if destroy:
        for item in destroy:
            tetrominos.remove(item)
    pygame.display.flip()
