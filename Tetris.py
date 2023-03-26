import pygame,sys
from pygame.math import Vector2 as v
from game_parameters import *
from Tetraminos import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

v1=v(0,1)
v1=v1.rotate(90)
direction=v(0,0)
rotate=False
c=Tetraminos([10,10],1000)
pygame.key.set_repeat(0,0)
while (1):
    screen.fill((255, 255, 255))
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        sys.exit()
    c.draw(screen)
    c.update(pygame.time.get_ticks(),event)
    clock.tick(FPS)
    dt=clock.get_fps()
    pygame.display.flip()

