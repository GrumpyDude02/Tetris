import math
from pygame.math import Vector2 as v

FPS = 60
cell_size=20
cell_number=30
playable_num=10
WIDTH=cell_number*cell_size
HEIGHT=cell_number*cell_size
t=(v(-1,0),v(0,0),v(0,-1),v(1,0))
z=[v(-1,0),v(0,0),v(1,0),v(1,1)]
shapes={"T":[v(-1,0),v(0,0),v(0,-1),v(1,0)],
        "Z":[v(-1,-1),v(0,-1),v(0,0),v(1,0)],
        "S":[v(1,-1),v(0,-1),v(0,0),v(0,-1)],
        "L":[v(0,-2),v(0,-1),v(0,0),v(1,0)],
        "I":[v(-2,0),v(-1,0),v(0,0),v(1,0)]
        }

moves={"left":v(-1,0),"right":v(1,0)}

sin_90=math.sin(math.radians(90))
cos_90=math.cos(math.radians(90))
sin_n90=math.sin(math.radians(-90))
cos_n90=math.cos(math.radians(-90))