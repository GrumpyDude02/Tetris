import pygame
from pygame.math import Vector2 as v

FPS = 60
vShift=2
shift=2
y_border_offset=2
cell_size=20
v_cell_number=22+y_border_offset+shift
h_cell_number=20
playable_num=10

BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,100,255)
WIDTH=h_cell_number*cell_size
HEIGHT=(v_cell_number-shift)*cell_size
MOVE_DELAY=100
BLOCK_SIZE=cell_size-1
SPAWN_LOCATION=[5,3]
PREVIEW_SURF_SIZE=(6*cell_size,5.5*cell_size)

shapes={"T":[[v(0,0),v(-1,0),v(0,-1),v(1,0)],(255, 68, 255)],
        "Z":[[v(0,0),v(-1,-1),v(0,-1),v(1,0)],(255, 0, 0)],
        "S":[[v(0,0),v(1,-1),v(0,-1),v(-1,0)],(0,255,0)],
        "L":[[v(0,0),v(-1,0),v(1,0),v(1,-1)],(255, 129, 0)],
        "I":[[v(0,0),v(-1,0),v(1,0),v(2,0)],(0, 255, 255)],
        "J":[[v(0,0),v(-1,-1),v(-1,0),v(1,0)],(0, 0, 255)],
        "O":[[v(0,0),v(0,-1),v(1,0),v(1,-1)],(255, 255, 0)]
        }

offsets_JLZST=((v(0,0),v(0,0),v(0,0),v(0,0),v(0,0)),
            (v(0,0),v(1,0),v(1,1),v(0,-2),v(1,-2)),
            (v(0,0),v(0,0),v(0,0),v(0,0),v(0,0)),
            (v(0,0),v(-1,0),v(-1,1),v(0,-2),v(-1,-2)))

offsets_I=[(v(0,0),v(-1,0),v(2,0),v(-1,0),v(2,0)),
            (v(-1,0),v(0,0),v(0,0),v(0,1),v(0,2)),
            (v(-1,-1),v(1,-1),v(-2,-1),v(1,0),v(-2,0)),
            (v(0,-1),v(0,-1),v(0,-1),v(0,-1),v(0,-2))]

moves={"left":v(-1,0),"right":v(1,0),"down":v(0,1),"snap":v(0,-100)}


grid=[]
placed_blocks=[[None for i in range(playable_num)]for j in range(v_cell_number)]

for i in range(0,v_cell_number-shift):
    for j in range(playable_num+vShift):
        if j==0 or j==playable_num+1:
            grid.append(pygame.Rect(j*cell_size,i*cell_size,cell_size-1,cell_size-1))
        elif i==0 or i==v_cell_number-shift-1:
            grid.append(pygame.Rect(j*cell_size,i*cell_size,cell_size-1,cell_size-1))
        

def draw_grid(window:pygame.Surface,grid,color)->None:
    for rect in grid:
        pygame.draw.rect(window,color,rect)
        
level_speed=[0.01667,0.021017,0.026977,0.035256,0.04693,0.06361,0.0879, 0.1236,0.1775, 0.2598, 0.388,0.59,0.92,1.42,2.36]
game_speed=60
