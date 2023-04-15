import random
from functions import *
from game_parameters import *
from Tetrominos import Tetrominos
from GameStates import GameStates


class Tetris:
    def __init__(self,game) -> None:
        self.game=game
        self.shapes_list=list(shapes.keys())
        random.shuffle(self.shapes_list)
        self.index=1
        self.next_shape=self.shapes_list[self.index]
        self.current_piece=Tetrominos(SPAWN_LOCATION,self.shapes_list[0],BLOCK_SIZE)
        self.held_piece=None
        self.destroy=[]
        self.tetrominos=[]
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
        self.shadow_surf=generate_surf((WIDTH,HEIGHT),150)
        self.hold_surface=generate_surf(PREVIEW_SURF_SIZE,0)
        self.preview_surface=generate_surf(PREVIEW_SURF_SIZE,0)
        self.score=0
        self.level=1
        self.cleared_lines=0
        
    def reset_game(self):
        reset_board(placed_blocks,self.tetrominos)
        random.shuffle(self.shapes_list)
        self.index=1
        self.level=1
        self.current_piece=self.current_piece=Tetrominos(SPAWN_LOCATION,self.shapes_list[0],BLOCK_SIZE)
        self.next_shape=self.shapes_list[self.index]
        self.held_piece=None
    
    def set_state(self,new_state):
        self.game.set_state(new_state)
        
    def draw(self):
        self.main_surface.fill(BLACK)
        self.shadow_surf.fill(BLACK)
        for tetromino in self.tetrominos:
            tetromino.draw(self.main_surface,None)        
        self.current_piece.draw(self.main_surface,self.shadow_surf)
        self.main_surface.blit(self.shadow_surf,(0,0))
        draw_grid(self.main_surface,grid,(96,96,96))
        
    def loop(self,events_list):
        current_time=pygame.time.get_ticks()
        for event in events_list:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.set_state(GameStates.paused)
        self.current_piece.update(current_time,self.game.dt,events_list,self.level)
        self.draw()


        