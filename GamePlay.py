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
        self.board_surface=generate_surf((board_width,board_height),0)
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
        self.shadow_surf=generate_surf((12*cell_size,HEIGHT),80)
        self.hold_surface=generate_surf(PREVIEW_SURF_SIZE,0)
        self.preview_surface=generate_surf(PREVIEW_SURF_SIZE,0)
        self.score=0
        self.level=1
        self.cleared_lines=0
        self.last_played_mode=None
        
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
        #self.main_surface.fill(BLACK)
        self.shadow_surf.fill(BLACK)
        self.board_surface.fill(BLACK)
        for tetromino in self.tetrominos:
            tetromino.draw(self.board_surface,None)        
        self.current_piece.draw(self.board_surface,self.shadow_surf)
        draw_grid(self.board_surface,grid,(96,96,96))
        self.board_surface.blit(self.shadow_surf,(0,0))
        self.main_surface.blit(self.board_surface,(((WIDTH-12*cell_size)//2),(HEIGHT-24*cell_size)//2))
    
    def resize(self):
        self.main_surface=pygame.transform.scale(self.main_surface,(WIDTH,HEIGHT))
        self.board_surface=pygame.transform.scale(self.main_surface,(board_width,board_height))
        for tetromino in self.tetrominos:
            for block in self.tetrominos:
                pass
        
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
        
    


        