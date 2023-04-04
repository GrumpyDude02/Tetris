import pygame,sys
from pygame.math import Vector2 as v
from game_parameters import *
from Tetrominos import *
from functions import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

v1=v(0,1)
v1=v1.rotate(90)
direction=v(0,0)
rotate=False
tetrominos=[Tetrominos([5,0],500,random.choice(list(shapes.keys())))]
display_surface=pygame.Surface((5*cell_size,4*cell_size))
shadow_surface=pygame.Surface((WIDTH,HEIGHT),pygame.HWSURFACE)
pygame.key.set_repeat(0,0)
append=False
#main loop

next_tetromino=Tetrominos([5,0],500,random.choice(list(shapes.keys())))
display_tetromino=Tetrominos([1.5,1.5+shift],500,next_tetromino.shape)


shadow_surface.set_colorkey(0)
shadow_surface.set_alpha(150)

while (1):
    destroy=[]
    if game_over(placed_blocks):
        reset_game(placed_blocks,tetrominos)
    if append:
        tetrominos.append(next_tetromino)
        next_tetromino=Tetrominos([5,0],500,random.choice(list(shapes.keys())))
        display_tetromino=Tetrominos([1.5,1.5+shift],500,next_tetromino.shape)
    #filling surfaces 
    screen.fill((0, 0, 0))
    display_surface.fill((255,255,255))
    shadow_surface.fill((0,0,0))
    display_tetromino.draw(display_surface,shadow_surface,True)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        sys.exit()
    draw_grid(screen,grid,(255,255,255))
    append=True if all(tetromino.isSet for tetromino in tetrominos) else False
    for tetromino in tetrominos:
        tetromino.update(pygame.time.get_ticks(),event)
        tetromino.draw(screen,shadow_surface,False)
        if tetromino.destroy:
            destroy.append(tetromino)
    check_line(placed_blocks,playable_num)
    screen.blit(display_surface,(13*cell_size,5*cell_size))
    screen.blit(shadow_surface,(0,0))
    clock.tick(FPS)
    if destroy:
        for item in destroy:
            tetrominos.remove(item)
    pygame.display.flip()
