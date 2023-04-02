import math,pygame
from pygame.math import Vector2 as v

FPS = 60
cell_size=20
v_cell_number=24
h_cell_number=20
playable_num=10
WIDTH=h_cell_number*cell_size
HEIGHT=v_cell_number*cell_size

shapes={"T":[v(-1,0),v(0,0),v(0,-1),v(1,0)],
        "Z":[v(-1,-1),v(0,-1),v(0,0),v(1,0)],
        "S":[v(1,-1),v(0,-1),v(0,0),v(-1,0)],
        "L":[v(-1,0),v(0,0),v(1,0),v(1,-1)],
        "I":[v(-1,0),v(0,0),v(1,0),v(2,0)],
        "J":[v(-1,-1),v(-1,0),v(0,0),v(1,0)],
        "O":[v(0,-1),v(0,0),v(1,0),v(1,-1)]
        }

moves={"left":v(-1,0),"right":v(1,0),"down":v(0,1)}
sin_90=math.sin(math.radians(90))
cos_90=math.cos(math.radians(90))
sin_n90=math.sin(math.radians(-90))
cos_n90=math.cos(math.radians(-90))

grid=[]
placed_blocks=[[None for i in range(playable_num)]for j in range(v_cell_number)]

for i in range(v_cell_number):
    for j in range(playable_num):
        grid.append(pygame.Rect(j*cell_size,i*cell_size,cell_size-1,cell_size-1))


def draw_grid(window:pygame.Surface,grid,color)->None:
    for rect in grid:
        pygame.draw.rect(window,color,rect)
