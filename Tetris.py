import pygame,sys,Tetraminos
from pygame.math import Vector2 as v
from game_parameters import *

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

v1=v(0,1)
v1=v1.rotate(90)

c=Tetraminos.Tetrominos([10,10])
while (1):
    screen.fill((255, 255, 255))
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        sys.exit()
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_r:
            c.rotate(0)
        elif event.key==pygame.K_t:
            c.rotate(1)
    c.update(pygame.time.get_ticks(),v(0,0))
    c.draw(screen)
    clock.tick(FPS)
    dt=clock.get_fps()
    pygame.display.flip()

