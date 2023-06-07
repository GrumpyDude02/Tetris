import pygame
from pygame.math import Vector2 as v


Resolutions=[(960,540),(1024,576),(1280,720),(1366,768),(1600,900),(1920,1080),(2560,1440)]
base_cell_size=22
base_resolution=Resolutions[0]
selected_res=Resolutions[1]
WIDTH=(selected_res[0])
HEIGHT=(selected_res[1])
base_font_scale=22

cell_size=round(base_cell_size*(HEIGHT/base_resolution[1]))

FPS = 60
shift=2
y_border_offset=2
x_border_offset=2

boardy_cell_number=22+y_border_offset+shift
boardx_cell_number=WIDTH//cell_size
playable_num=10

board_width=12*cell_size
board_height=(boardy_cell_number-shift)*cell_size
MOVE_DELAY=100
SPAWN_LOCATION=[5,3]
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,100,255)

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


level_speed=[0.01667,0.021017,0.026977,0.035256,0.04693,0.06361,0.0879, 0.1236,0.1775, 0.2598, 0.388,0.59,0.92,1.42,2.36]
score_lines=[100,300,500,800]
game_speed=60

grid=[]
placed_blocks=[[None for i in range(playable_num)]for j in range(boardy_cell_number)]

for i in range(0,boardy_cell_number-shift):
    for j in range(playable_num+x_border_offset):
        if j==0 or j==playable_num+x_border_offset-1:
            grid.append(pygame.Rect(j*cell_size,i*cell_size,cell_size-1,cell_size-1))
        elif (i==0 or i==boardy_cell_number-shift-1):
            grid.append(pygame.Rect(j*cell_size,i*cell_size,cell_size-1,cell_size-1))
        
        
def change_display_val(selected_res)->tuple[float]:
    global WIDTH,HEIGHT,board_width,board_height,cell_size,grid
    WIDTH=selected_res[0]
    HEIGHT=selected_res[1]
    scale_factor_x=WIDTH/base_resolution[0]
    scale_factor_y=HEIGHT/base_resolution[1]
    cell_size=round(base_cell_size*scale_factor_y)
    board_width=12*cell_size
    board_height=(boardy_cell_number-shift)*cell_size
    grid=[]
    for i in range(0,boardy_cell_number-shift):
        for j in range(playable_num+x_border_offset):
            if j==0 or j==playable_num+x_border_offset-1:
                grid.append(pygame.Rect(j*cell_size,i*cell_size,cell_size-1,cell_size-1))
            elif (i==0 or i==boardy_cell_number-shift-1):
                grid.append(pygame.Rect(j*cell_size,i*cell_size,cell_size-1,cell_size-1))

    return (scale_factor_x,scale_factor_y)        


