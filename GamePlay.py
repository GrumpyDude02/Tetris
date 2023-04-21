import random,pygame,Tools.functions as functions
from Tools.Timer import Timer
import game_parameters as gp
from Tetrominos import Tetrominos
from GameStates import GameStates
from Tools.Position import Position
from copy import deepcopy

preview_pos=pygame.Vector2(1,6)


elements_coor={'board':Position(0.364,0.01666,gp.WIDTH,gp.HEIGHT),
               'next_text':Position(0.68,0.01666,gp.WIDTH,gp.HEIGHT),
               'hold_text':Position(0.24,0.40,gp.WIDTH,gp.HEIGHT),
               'line_text':Position(0.15,0.26,gp.WIDTH,gp.HEIGHT),
               'level_text':Position(0.15,0.173,gp.WIDTH,gp.HEIGHT),
               'preview_surface':Position(0.68,0.05,gp.WIDTH,gp.HEIGHT),
               'time':Position(0.15,0.08,gp.WIDTH,gp.HEIGHT)}

preview_tetrominos_pos=[[preview_pos.x,preview_pos.y+i] for i in range(0,21,3)]

HOLD_POS=(10,16)

class GameMode:
    resumed="resumed"
    paused="paused"
    initialized="initialized"
    start_time=0
    
    def init_surfaces(self):
        self.board_surface=functions.generate_surf((gp.board_width,gp.board_height),0)
        self.main_surface=functions.generate_surf((gp.WIDTH,gp.HEIGHT),0)
        self.shadow_surf=functions.generate_surf((12*gp.cell_size,gp.HEIGHT),80)
        self.preview_surface=functions.generate_surf((5*gp.cell_size,gp.HEIGHT),0)
        self.preview_surface.set_colorkey(gp.BLACK)
    
    def __init__(self,game,shape:str=None) -> None:
        if shape:
            self.shape=shape
            self.currnet_piece=Tetrominos(gp.SPAWN_LOCATION,self.shape,gp.cell_size)
            self.preview_tetrominos=[Tetrominos(pos,self.shape,gp.cell_size/2) for pos in preview_tetrominos_pos]
        self.init_surfaces()
        self.game=game
        self.held_piece=None
        self.destroy=[]
        self.tetrominos=[]
        self.score=0
        self.level=1
        self.state=GameMode.initialized  
        self.cleared_lines=0
        self.switch_available=False
        self.timer=Timer()
        self.placed_blocks=[[None for i in range(gp.playable_num)]for j in range(gp.boardy_cell_number)]
        
    def reset_game(self):
        functions.reset_board(self.placed_blocks,self.tetrominos)
        self.timer.reset()
        self.level=1
        self.cleared_lines=0
        self.held_piece=None
        
    def set_state(self,new_state):
        self.game.set_state(new_state)

    def swap_pieces(self):
        if self.held_piece is None:
            self.current_piece.isHeld=True
            self.held_piece=deepcopy(self.current_piece)
            self.held_piece.set_pos(HOLD_POS)
            self.held_piece.isHeld=False
        elif self.switch_available:
            temp=self.current_piece
            self.current_piece=self.held_piece
            self.current_piece.set_pos(gp.SPAWN_LOCATION)
            self.held_piece=temp
            self.held_piece.set_pos(HOLD_POS)
            self.switch_available=False
    
    def render_timer(self)->pygame.Surface:
        int_timer=int(self.timer.time)
        time=self.game.main_font.render(f'TIME : {(int_timer//1000)//60:02d}:{(int_timer//1000)%60:02d}:{(int_timer//10)%100}',True,gp.WHITE)
        return time

    def resize(self):
        self.init_surfaces()
        for key,position in elements_coor.items():
            position.update(gp.WIDTH,gp.HEIGHT)
        for line in self.placed_blocks:
            for block in line:
                if block is not None:
                    block.resize()
        self.current_piece.resize()
        for tetrmino in self.tetrominos:
            tetrmino.resize()
        for preview_piece in self.preview_tetrominos:
            preview_piece.resize(gp.cell_size*0.80)     
    
    def draw(self):
        #self.main_surface.fill(BLACK)
        self.shadow_surf.fill(gp.BLACK)
        self.board_surface.fill(gp.BLACK)
        for line in self.placed_blocks:
            for block in line:
                block.draw(self.board_surface)      
        self.current_piece.draw(self.board_surface,self.shadow_surf,self.placed_blocks)
        functions.draw_grid(self.board_surface,gp.grid,(96,96,96))
        self.board_surface.blit(self.shadow_surf,(0,0))
        self.main_surface.blit(self.board_surface,(((gp.WIDTH-12*gp.cell_size)//2),(gp.HEIGHT-24*gp.cell_size)//2))
    
    def draw_to_screen(self):
        self.game.screen.blit(self.main_surface,(0,0))
        


class Tetris(GameMode):
    switch_available=True
    def __init__(self,game) -> None:
        super().__init__(game)
        self.index=0
        self.shapes_list=list(gp.shapes.keys())
        #shuffling 
        random.shuffle(self.shapes_list)
        self.next_shapes=[shape for shape in self.shapes_list]
        self.current_piece=Tetrominos(gp.SPAWN_LOCATION,self.next_shapes.pop(0),gp.cell_size)
        random.shuffle(self.shapes_list)
        self.next_shapes.append(self.shapes_list[self.index])
        self.preview_tetrominos=[Tetrominos(pos,shape,gp.cell_size*0.80) for pos,shape in zip(preview_tetrominos_pos,self.shapes_list)]
        self.index+=1  
        
    def reset_game(self):
        super().reset_game()
        random.shuffle(self.shapes_list)
        self.next_shapes=[shape for shape in self.shapes_list]
        random.shuffle(self.shapes_list)
        self.current_piece=self.update_queue()
        self.state=GameMode.initialized
        self.destroy=[]
    
    def handle_events(self,current_time,dt):
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
            if event.type==pygame.ACTIVEEVENT:
                if event.state==2:
                    print("gg")
                    self.state=GameMode.paused
                    self.set_state(GameStates.paused)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.set_state(GameStates.paused)
                    self.timer.pause_timer()
                    self.state=GameMode.paused
                if event.key==pygame.K_c:
                    self.swap_pieces()        
        self.current_piece.handle_events(current_time,events,self.placed_blocks,dt)
    
    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.destroy.remove(tetromino)

    def set_shapes(self):
        for shape,tetromino in zip(self.next_shapes,self.preview_tetrominos):
            tetromino.set_shape(shape)

    def update_queue(self)->Tetrominos:
        self.next_shapes.append(self.shapes_list[self.index])
        self.index+=1
        self.index%=7
        if self.index==0:
            random.shuffle(self.shapes_list)
        shape=self.next_shapes.pop(0)
        return Tetrominos(gp.SPAWN_LOCATION,shape,gp.cell_size)
    
    def update(self,current_time,dt):
        self.timer.update_timer()
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
        self.cleared_lines+=functions.check_line(self.placed_blocks,gp.playable_num)
    
    def draw(self):
        self.main_surface.fill(gp.BLACK)
        self.shadow_surf.fill(gp.BLACK)
        self.board_surface.fill(gp.BLACK)
        self.preview_surface.fill(gp.BLACK)
        LINES=self.game.main_font.render(f'LINES : {self.cleared_lines} / \u221E',True,gp.WHITE)
        LEVEL=self.game.main_font.render(f'LEVEL : {self.level}',True,gp.WHITE)
        HOLD=self.game.main_font.render("HOLD : ",True,gp.WHITE)
        NEXT=self.game.main_font.render("NEXT : ",True,gp.WHITE)
        #blit coordonates
        #timer_coor=(260,60)
        #line_coor=(260,110)
        #level_coor=(260,160)
        #hold_coor=(0.24,0.40)
        if self.held_piece:
            self.held_piece.draw(self.main_surface)
        for tetromino in self.tetrominos:
            tetromino.draw(self.board_surface,None,self.placed_blocks)
            if tetromino.destroy:
                self.destroy.append(tetromino)         
        for preview in self.preview_tetrominos:
            preview.draw(self.preview_surface,None,self.placed_blocks)  
        self.current_piece.draw(self.board_surface,self.shadow_surf,self.placed_blocks)
            
        functions.draw_grid(self.board_surface,gp.grid,(96,96,96))
        
        
        
        self.board_surface.blit(self.shadow_surf,(0,0))
        self.main_surface.blit(self.board_surface,elements_coor['board'].get_pos())
        self.main_surface.blit(HOLD,elements_coor['hold_text'].get_pos())
        self.main_surface.blit(NEXT,elements_coor['next_text'].get_pos())
        self.main_surface.blit(self.render_timer(),elements_coor['time'].get_pos())
        self.main_surface.blit(LEVEL,elements_coor['level_text'].get_pos())
        self.main_surface.blit(LINES,elements_coor['line_text'].get_pos())
        self.main_surface.blit(self.preview_surface,elements_coor['preview_surface'].get_pos())
        
        self.draw_to_screen()
     
    def loop(self):
        self.timer.start_timer()
        while self.game.state==GameStates.in_game:
            dt=min(self.timer.delta_time(),0.066)
            self.destroy=[]
            current_time=self.timer.current_time()*1000
            #----------debug section-------------
            #print(pygame.mouse.get_pos())
            #------------------------------------
            pygame.display.set_caption("Tetris FPS:"+str(round(self.game.clock.get_fps())))
            self.handle_events(current_time,dt)
            self.update(current_time,dt)
            self.draw()
            self.game.clock.tick(gp.FPS)/1000
            pygame.display.flip()
            self.destroy_tetrominos()    
 
  
        