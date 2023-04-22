import pygame,random,Tools.functions as functions
import game_parameters as gp
from GameStates import GameStates
from Tetrominos import Tetrominos
from Tools.Buttons import Buttons

    
class Menu:
    
    def __init__(self,game,child_menus: list=None,previous_menu=None):
        self.game=game
        self.main_surface=functions.generate_surf((gp.WIDTH,gp.HEIGHT),0)
        self.child_menus=child_menus
        self.previous_menu=previous_menu
        self.buttons=None
        
    def set_state(self,new_state):
        self.game.set_state(new_state)
    
    def set_pending_state(self,next_state):
        self.game.pending_state=next_state
    
    def draw(self,fill_color:tuple=None):
        if fill_color:
            self.main_surface.fill(fill_color)
        for key in self.buttons.keys():
            self.buttons[key].draw(self.main_surface)
        self.game.screen.blit(self.main_surface,(0,0))
    
    def resize(self):
        self.main_surface=functions.generate_surf((gp.WIDTH,gp.HEIGHT),0)
        for button in self.buttons.values():
            button.resize((gp.WIDTH,gp.HEIGHT),self.game.main_font)





class MainMenu(Menu):
    last_spawn_time=0
    def __init__(self, game):
        super().__init__(game)
        self.tetrominos=[]
        self.destroy=[]
        self.buttons={"PLAY":Buttons("PLAY",(0.16,0.1),(0.42,0.35),game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      "SETTINGS":Buttons("SETTINGS",(0.16,0.1),(0.42,0.50),game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      "EXIT":Buttons("EXIT",(0.16,0.1),(0.42,0.65),game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT))}

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
        if self.buttons["EXIT"].checkclick():
            self.set_state(GameStates.quitting)
        if self.buttons["PLAY"].checkclick():
            self.set_state(GameStates.in_game)  
        if self.buttons["SETTINGS"].checkclick():
            self.set_state(GameStates.in_settings)
    
    def generate_tetromino(self)->Tetrominos:
        t=Tetrominos([random.randrange(2,(gp.WIDTH//gp.cell_size)-4,4),0],random.choice(list(gp.shapes.keys())),gp.cell_size)
        t.SRS_Rotate(random.choice([bool("True"),bool("False")]),random.randint(0,2))
        return t
    
    def draw_and_update(self,current_time,dt):
        self.destroy=[]
        self.main_surface.fill(gp.BLACK)
        if current_time-MainMenu.last_spawn_time>random.randrange(1200,6000,500):
            MainMenu.last_spawn_time=current_time
            self.tetrominos.append(self.generate_tetromino())
        for tetromino in self.tetrominos:
            tetromino.smooth_fall(4,dt)
            tetromino.draw(self.main_surface)
            if tetromino.pivot.y>gp.HEIGHT//gp.cell_size+5:
                self.destroy.append(tetromino)
        for key,item in self.buttons.items():
            item.draw(self.main_surface)
        self.game.screen.blit(self.main_surface,(0,0))
        
    
    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.tetrominos.remove(tetromino)
    
    def loop(self):
        dt=1/gp.FPS
        MainMenu.last_spawn_time=-10000
        self.tetrominos=[]
        while self.game.state==GameStates.main_menu:
            current_time=pygame.time.get_ticks()
            self.handle_events()
            self.draw_and_update(current_time,dt)
            dt=self.game.clock.tick(gp.FPS)/1000
            pygame.display.flip()
            self.destroy_tetrominos()
            
            

class PauseScreen(Menu):
    
    def create_blurred_surface(self):
        self.transparent_surf=functions.generate_surf((gp.WIDTH,gp.HEIGHT),150)
        self.rect=pygame.Rect(0,0,gp.WIDTH,gp.HEIGHT)
        self.text=self.game.main_font.render("PAUSED",True,gp.WHITE)
        self.transparent_surf.fill(gp.BLUE)
    
    def __init__(self,game):
        super().__init__(game)
        self.create_blurred_surface()
        #0.52 0.60 0.32 0.60
        self.buttons= {"EXIT":Buttons("EXIT",( 0.16 , 0.1), (0.52, 0.60) ,game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                       "RESUME":Buttons("RESUME", (0.16 , 0.1) , (0.32 ,0.60) ,game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT))}
    
    def resize(self):
        super().resize()
        self.create_blurred_surface()
            
    def handl_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                    self.set_state(GameStates.quitting)
            elif event.type==pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    self.set_state(GameStates.in_game)
    
    def draw(self,blurred_surface):
        self.main_surface.blit(blurred_surface,(0,0))
        self.main_surface.blit(self.transparent_surf,(0,0))
        render_position=self.text.get_rect()
        render_position.center=self.rect.center
        self.main_surface.blit(self.text,render_position)
        super().draw()
    
    def loop(self,surface):
        blurred_surface=functions.blurSurf(surface,5)
        while self.game.state==GameStates.paused:
            self.handl_events()
            if self.buttons["EXIT"].checkclick():
                self.set_pending_state(GameStates.main_menu)
                self.set_state(GameStates.resetting)
            elif self.buttons["RESUME"].checkclick():
                self.set_state(GameStates.in_game)
            self.draw(blurred_surface)
            pygame.time.Clock().tick(gp.FPS)
            pygame.display.flip()
            
            
class SettingsMenu(Menu):
    def __init__(self,game):
        super().__init__(game)
        self.buttons={'960x540':Buttons('960x540',(0.16,0.1),(0.42,0.15),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      '1024x576':Buttons('1024x576',(0.16,0.1),(0.42,0.25),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      '1280x720':Buttons('1280x720',(0.16,0.1),(0.42,0.35),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      '1366x768':Buttons('1366x768',(0.16,0.1),(0.42,0.45),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      '1600x900':Buttons('1600x900',(0.16,0.1),(0.42,0.55),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      '1920x1080':Buttons('1920x1080',(0.16,0.1),(0.42,0.65),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      '2560x1440':Buttons('2560x1440',(0.16,0.1),(0.42,0.75),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT)),
                      'BACK':Buttons('BACK',(0.16,0.1),(0.42,0.85),self.game.main_font,5,hover_color=gp.BLUE,sc_size=(gp.WIDTH,gp.HEIGHT))}
        
    def handle_events(self):
        ev=pygame.event.get()
        for event in ev:
            if event.type==pygame.QUIT:
                self.set_state(GameStates.quitting)
        for key,i in zip(self.buttons.keys(),range(0,7)):
            if self.buttons[key].checkclick():
                gp.selected_res=gp.Resolutions[i]
                self.set_state(GameStates.changing_res)
                self.set_pending_state(GameStates.in_settings)
                break
        if self.buttons['BACK'].checkclick():
            self.set_state(GameStates.main_menu)
    
    def loop(self):
        while self.game.state==GameStates.in_settings:
            self.handle_events()
            self.draw()
            pygame.time.Clock().tick(gp.FPS)
            pygame.display.flip()
            