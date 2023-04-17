import random
from functions import *
from game_parameters import *
from Tetrominos import Tetrominos
from GameStates import GameStates
from copy import deepcopy

class GameMode:
    def __init__(self,game,shape:str=None) -> None:
        if shape:
            self.shape=shape
            self.current_piece=Tetrominos(SPAWN_LOCATION,self.shape,BLOCK_SIZE)
        self.game=game
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
        self.placed_blocks=[[None for i in range(playable_num)]for j in range(boardy_cell_number)]
        
    def reset_game(self):
        reset_board(placed_blocks,self.tetrominos)
        self.level=1
        self.held_piece=None
        
    def set_state(self,new_state):
        self.game.set_state(new_state)

    def resize(self):
        self.main_surface=pygame.transform.scale(self.main_surface,(WIDTH,HEIGHT))
        self.board_surface=pygame.transform.scale(self.main_surface,(board_width,board_height))
        for line in self.placed_blocks:
            for block in line:
                pass
    def draw(self):
        #self.main_surface.fill(BLACK)
        self.shadow_surf.fill(BLACK)
        self.board_surface.fill(BLACK)
        for line in self.placed_blocks:
            for block in line:
                block.draw(self.board_surface)      
        self.current_piece.draw(self.board_surface,self.shadow_surf,self.placed_blocks)
        draw_grid(self.board_surface,grid,(96,96,96))
        self.board_surface.blit(self.shadow_surf,(0,0))
        self.main_surface.blit(self.board_surface,(((WIDTH-12*cell_size)//2),(HEIGHT-24*cell_size)//2))
    
    def draw_to_screen(self):
        self.game.screen.blit(self.main_surface,(0,0))
        


class Tetris(GameMode):
    destroy=[]
    switch_available=True
    def __init__(self,game) -> None:
        super().__init__(game)
        self.index=1
        self.shapes_list=list(shapes.keys())
        random.shuffle(self.shapes_list)
        self.current_piece=Tetrominos(SPAWN_LOCATION,self.shapes_list[0],BLOCK_SIZE)
        self.next_shape=self.shapes_list[self.index]
        
    def reset_game(self):
        super().reset_game()
        random.shuffle(self.shapes_list)
        self.index=1
        self.next_shape=self.shapes_list[self.index]
        Tetris.destroy=[]
        
    def draw(self):
        #self.main_surface.fill(BLACK)

        self.shadow_surf.fill(BLACK)
        self.board_surface.fill(BLACK)
        for tetromino in self.tetrominos:
            tetromino.draw(self.board_surface,None,self.placed_blocks)
            if tetromino.destroy:
                self.destroy.append(tetromino)        
        self.current_piece.draw(self.board_surface,self.shadow_surf,self.placed_blocks)
        LINES=self.game.main_font.render(f'LINES : {self.cleared_lines}',True,WHITE)
        LEVEL=self.game.main_font.render(f'LEVEL : {self.level}',True,WHITE)
        HOLD=self.game.main_font.render("HOLD : ",True,WHITE)
        NEXT=self.game.main_font.render("NEXT : ",True,WHITE)
        draw_grid(self.board_surface,grid,(96,96,96))
        self.board_surface.blit(self.shadow_surf,(0,0))
        self.main_surface.blit(self.board_surface,(((WIDTH-12*cell_size)//2),(HEIGHT-24*cell_size)//2))
        self.main_surface.blit(NEXT,(round(WIDTH*0.68),(HEIGHT-24*cell_size)//2))
        self.draw_to_screen()
    
    def handle_events(self,current_time):
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.set_state(GameStates.paused)
                if event.key==pygame.K_c:
                    if self.held_piece is None:
                        self.current_piece.isHeld=True
                        self.held_piece=deepcopy(self.current_piece)
                        self.held_piece.isHeld=False
                    elif Tetris.switch_available:
                        temp=self.current_piece
                        self.current_piece=self.held_piece
                        self.held_piece=temp
                        Tetris.switch_available=False              
        self.current_piece.handle_events(current_time,events,self.placed_blocks)
    
    def generate_new_piece(self)->Tetrominos:
        temp=self.next_shape
        self.index+=1
        self.index%=7
        if self.index==0:
            random.shuffle(self.shapes_list)
        self.next_shape=self.shapes_list[self.index]
        return Tetrominos(SPAWN_LOCATION,temp,BLOCK_SIZE)
    
    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.destroy.remove(tetromino)
    
    def update(self,dt,current_time):
        if self.current_piece.isSet:
            self.tetrominos.append(self.current_piece)
            self.current_piece=self.generate_new_piece()
            Tetris.switch_available=True
        elif self.current_piece.isHeld:
            Tetris.switch_available=False
            self.current_piece=self.generate_new_piece()
        self.current_piece.fall(self.level,dt,current_time,self.placed_blocks)
        self.cleared_lines=check_line(self.placed_blocks,playable_num)
        

    def loop(self):
        dt=1/FPS
        while self.game.state==GameStates.in_game:
            self.destroy=[]
            current_time=pygame.time.get_ticks()
            self.handle_events(current_time)
            self.update(dt,current_time)
            self.draw()
            dt=pygame.time.Clock().tick(FPS)/1000
            pygame.display.flip()
            self.destroy_tetrominos()    
           
    


        