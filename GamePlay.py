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
            self.next_tetrominos=[Tetrominos(SPAWN_LOCATION,self.shape,BLOCK_SIZE) for i in range(0,6)]
            self.curret_piece=Tetrominos(SPAWN_LOCATION,self.shape,BLOCK_SIZE)
        self.game=game
        self.held_piece=None
        self.destroy=[]
        self.tetrominos=[]
        self.board_surface=generate_surf((board_width,board_height),0)
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
        self.shadow_surf=generate_surf((12*cell_size,HEIGHT),80)
        self.score=0
        self.level=1
        self.cleared_lines=0
        self.switch_available=False
        self.placed_blocks=[[None for i in range(playable_num)]for j in range(boardy_cell_number)]
     
    def add_to_queue(self)->Tetrominos:
        self.next_tetrominos.append(Tetrominos(SPAWN_LOCATION,self.shapes_list[self.index],BLOCK_SIZE))
        return self.next_tetrominos.pop(0)
        
    def reset_game(self):
        reset_board(self.placed_blocks,self.tetrominos)
        self.level=1
        self.held_piece=None
        
    def set_state(self,new_state):
        self.game.set_state(new_state)

    def swap_pieces(self):
        if self.held_piece is None:
            self.current_piece.isHeld=True
            self.held_piece=deepcopy(self.current_piece)
            self.held_piece.isHeld=False
        elif self.switch_available:
            temp=self.current_piece
            self.current_piece=self.held_piece
            self.held_piece=temp
            self.switch_available=False
    
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
        self.index=0
        self.shapes_list=list(shapes.keys())
        random.shuffle(self.shapes_list)
        self.next_tetrominos=[Tetrominos(SPAWN_LOCATION,shape,BLOCK_SIZE) for shape in self.shapes_list]
        self.current_piece=self.next_tetrominos.pop(0)
        random.shuffle(self.shapes_list)
        self.next_tetrominos.append(Tetrominos(SPAWN_LOCATION,self.shapes_list[self.index],BLOCK_SIZE))
        self.index+=1    
        
    def reset_game(self):
        super().reset_game()
        random.shuffle(self.shapes_list)
        self.next_tetrominos=[Tetrominos(SPAWN_LOCATION,shape,BLOCK_SIZE) for shape in self.shapes_list]
        random.shuffle(self.shapes_list)
        self.current_piece=self.add_to_queue()
        self.destroy=[]
        
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
                    self.swap_pieces()           
        self.current_piece.handle_events(current_time,events,self.placed_blocks)
    
    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.destroy.remove(tetromino)
    
    def add_to_queue(self)->Tetrominos:
        self.next_tetrominos.append(Tetrominos(SPAWN_LOCATION,self.shapes_list[self.index],BLOCK_SIZE))
        self.index+=1
        self.index%=7
        if self.index==0:
            random.shuffle(self.shapes_list)
        return self.next_tetrominos.pop(0)

    def update(self,dt,current_time):
        if self.current_piece.isSet:
            self.tetrominos.append(self.current_piece)
            self.current_piece=self.add_to_queue()
            self.switch_available=True
        elif self.current_piece.isHeld:
            self.current_piece=self.add_to_queue()
            self.switch_available=False
        if self.cleared_lines>self.level*10:
            self.level+=1
        print(self.level,self.cleared_lines)
        self.current_piece.fall(self.level,dt,current_time,self.placed_blocks)
        self.cleared_lines+=check_line(self.placed_blocks,playable_num)
        

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
           
    


        