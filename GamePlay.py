import random
from functions import *
from game_parameters import *
from Tetrominos import Tetrominos
from GameStates import GameStates
from copy import deepcopy

preview_tetrominos_pos=[[10,4],[10,6],[10,8],[10,10],[10,12],[10,14],[10,16]]

class GameMode:
    resumed="resumed"
    paused="paused"
    initialized="initialized"
    running="running"
    start_time=0
    def __init__(self,game,shape:str=None) -> None:
        if shape:
            self.shape=shape
            self.curret_piece=Tetrominos(SPAWN_LOCATION,self.shape,BLOCK_SIZE)
            self.preview_tetrominos=[Tetrominos(pos,self.shape,BLOCK_SIZE) for pos in preview_tetrominos_pos]
        self.game=game
        self.held_piece=None
        self.destroy=[]
        self.tetrominos=[]
        self.board_surface=generate_surf((board_width,board_height),0)
        self.main_surface=generate_surf((WIDTH,HEIGHT),0)
        self.shadow_surf=generate_surf((12*cell_size,HEIGHT),80)
        self.score=0
        self.level=15
        self.cleared_lines=0
        self.switch_available=False
        self.time=0
        self.placed_blocks=[[None for i in range(playable_num)]for j in range(boardy_cell_number)]
        
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
        #shuffling 
        random.shuffle(self.shapes_list)
        self.next_shapes=[shape for shape in self.shapes_list]
        self.current_piece=Tetrominos(SPAWN_LOCATION,self.next_shapes.pop(0),BLOCK_SIZE)
        random.shuffle(self.shapes_list)
        self.next_shapes.append(self.shapes_list[self.index])
        self.preview_tetrominos=[Tetrominos(pos,shape,BLOCK_SIZE) for pos,shape in zip(preview_tetrominos_pos,self.shapes_list)]
        self.index+=1  
        self.timer_state=GameMode.running  
        
    def reset_game(self):
        super().reset_game()
        random.shuffle(self.shapes_list)
        self.next_shapes=[shape for shape in self.shapes_list]
        random.shuffle(self.shapes_list)
        self.current_piece=self.update_queue()
        self.destroy=[]
        
    def draw(self):
        self.main_surface.fill(BLACK)
        self.shadow_surf.fill(BLACK)
        self.board_surface.fill(BLACK)
        for tetromino in self.tetrominos:
            tetromino.draw(self.board_surface,None,self.placed_blocks)
            if tetromino.destroy:
                self.destroy.append(tetromino)
        for preview in self.preview_tetrominos:
            preview.draw(self.main_surface,None,self.placed_blocks)     
        self.current_piece.draw(self.board_surface,self.shadow_surf,self.placed_blocks)
        LINES=self.game.main_font.render(f'LINES : {self.cleared_lines}',True,WHITE)
        LEVEL=self.game.main_font.render(f'LEVEL : {self.level}',True,WHITE)
        HOLD=self.game.main_font.render("HOLD : ",True,WHITE)
        NEXT=self.game.main_font.render("NEXT : ",True,WHITE)
        time=self.game.main_font.render(f'TIME : {self.time//60:02d}:{self.time%60:02d}',True,WHITE)
        draw_grid(self.board_surface,grid,(96,96,96))
        self.board_surface.blit(self.shadow_surf,(0,0))
        self.main_surface.blit(self.board_surface,(((WIDTH-12*cell_size)//2),(HEIGHT-24*cell_size)//2))
        self.main_surface.blit(NEXT,(round(WIDTH*0.68),(HEIGHT-24*cell_size)//2))
        self.main_surface.blit(time,(50,50))
        self.draw_to_screen()
    
    def handle_events(self,current_time):
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.set_state(GameStates.paused)
                    self.timer_state=Tetris.paused
                if event.key==pygame.K_c:
                    self.swap_pieces()           
        self.current_piece.handle_events(current_time,events,self.placed_blocks)
    
    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.destroy.remove(tetromino)
    
    def update_queue(self)->Tetrominos:
        self.next_shapes.append(self.shapes_list[self.index])
        self.index+=1
        self.index%=7
        if self.index==0:
            random.shuffle(self.shapes_list)
        shape=self.next_shapes.pop(0)
        return Tetrominos(SPAWN_LOCATION,shape,BLOCK_SIZE)

    def set_shapes(self):
        for shape,tetromino in zip(self.next_shapes,self.preview_tetrominos):
            tetromino.set_shape(shape)

    def update(self,dt,current_time):
        if self.current_piece.isSet:
            self.tetrominos.append(self.current_piece)
            self.current_piece=self.update_queue()
            self.set_shapes()
            self.switch_available=True
        elif self.current_piece.isHeld:
            self.current_piece=self.update_queue()
            self.set_shapes()
            self.switch_available=False
        if self.cleared_lines>self.level*10:
            self.level+=1
        self.current_piece.fall(self.level,dt,current_time,self.placed_blocks)
        self.cleared_lines+=check_line(self.placed_blocks,playable_num)
        

    def loop(self):
        dt=1/FPS
        temp=0
        GameMode.start_time=pygame.time.get_ticks()
        if self.timer_state==GameMode.paused:
            temp=self.time
            self.timer_state=GameMode.resumed
        while self.game.state==GameStates.in_game:
            self.destroy=[]
            current_time=pygame.time.get_ticks()
            self.time=temp+(current_time-GameMode.start_time)//1000 #in seconds   
            self.handle_events(current_time)
            self.update(dt,current_time)
            self.draw()
            dt=pygame.time.Clock().tick(FPS)/1000
            pygame.display.flip()
            self.destroy_tetrominos()    
           
    


        