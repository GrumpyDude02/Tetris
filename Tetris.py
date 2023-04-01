import pygame,sys
from pygame.math import Vector2 as v
from game_parameters import *
from Tetrominos import *
from functions import check_line

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE|pygame.DOUBLEBUF)
hidden_sc=pygame.Surface((WIDTH,HEIGHT))
clock = pygame.time.Clock()

v1=v(0,1)
v1=v1.rotate(90)
direction=v(0,0)
rotate=False
tetrominos=[Tetrominos((255, 165, 0),[5,-1],500)]
pygame.key.set_repeat(0,0)
                           
#main loop

while (1):
    destroy=[]
    screen.fill((255, 255, 255))
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        sys.exit()
    draw_grid(screen,grid,(0,0,0))
    if all(tetromino.isSet for tetromino in tetrominos):
        tetrominos.append(Tetrominos((255, 165, 0),[5,0],500))
    for tetromino in tetrominos:
        tetromino.update(pygame.time.get_ticks(),event)
        tetromino.draw(screen)
        if tetromino.destroy:
            destroy.append(tetromino)
    check_line(placed_blocks,playable_num)
    print(len(tetrominos))
    clock.tick(FPS)
    if destroy:
        for item in destroy:
            tetrominos.remove(item)
    pygame.display.flip()

