import pygame, random, Tools.functions as functions
import Globals as gp
from GameStates import GameStates
from Tetrominos import Tetrominos
from Tools.Buttons import Buttons


direction = {"up": 0, "right": 1, "down": 2, "left": 3}


class Background:
    def __init__(self) -> None:
        self.objects = []
        self.destroy = []

    def generate_tetromino(self) -> Tetrominos:
        t = Tetrominos(
            [random.randrange(2, (gp.WIDTH // gp.cell_size) - 4, 4), 0],
            random.choice(list(gp.SHAPES.keys())),
            gp.cell_size,
        )
        t.SRS_rotate(random.choice([True, False]), random.randint(0, 2))
        return t

    def draw_and_update(self, surface, current_time, dt):
        self.destroy = []
        surface.fill(gp.BLACK)
        if current_time - Menu.last_spawn_time > random.randrange(1200, 6000, 500):
            Menu.last_spawn_time = current_time
            self.objects.append(self.generate_tetromino())
        for tetromino in self.objects:
            tetromino.smooth_fall(4, dt)
            tetromino.draw(surface)
            if tetromino.pivot.y > gp.HEIGHT // gp.cell_size + 5:
                self.destroy.append(tetromino)

    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.objects.remove(tetromino)


class Menu:
    last_spawn_time = 0

    class Cursor:
        def set_attr(self):
            attr = self.button.get_attributes()
            self.rect.width = attr[1][0]
            self.rect.height = attr[1][1]
            self.rect.center = attr[0]

        def __init__(self, color, button):
            self.index = 0
            self.button = button
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.set_attr()
            self.color = color

        def move_to(self, direction: int = None, button: Buttons = None):
            if button:
                self.button = button
                self.set_attr()
            elif self.button.next_buttons[direction]:
                self.button = self.button.next_buttons[direction]
                self.set_attr()

        def draw(self, surface):
            pygame.draw.rect(surface, self.color, self.rect, width=5)

    def __init__(self, game, child_menus: list = None, previous_menu=None, bg: Background = None):
        self.game = game
        self.background = bg
        self.main_surface = functions.generate_surf((gp.WIDTH, gp.HEIGHT), 0)
        self.child_menus = child_menus
        self.previous_menu = previous_menu
        self.buttons = None
        self.cursor = None
        self.mouse_mode = True

    def set_state(self, new_state, last_mode: str = None):
        self.game.set_state(new_state, last_mode)

    def set_pending_state(self, next_state):
        self.game.pending_state = next_state

    def switch_input(self, event: pygame.event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_mode = True
        elif event.type == pygame.KEYDOWN:
            self.mouse_mode = False

    def draw(self, fill_color: tuple = None, current_time: float = 0, dt: float = 1 / 60):
        if fill_color:
            self.main_surface.fill(fill_color)
        if self.background is not None:
            self.background.draw_and_update(self.main_surface, current_time, dt)
        for key in self.buttons.keys():
            self.buttons[key].draw(self.main_surface)
        if self.cursor is not None:
            self.cursor.draw(self.main_surface)
        self.game.screen.blit(self.main_surface, (0, 0))

    def resize(self):
        self.main_surface = functions.generate_surf((gp.WIDTH, gp.HEIGHT), 0)
        for button in self.buttons.values():
            button.resize((gp.WIDTH, gp.HEIGHT), self.game.main_font)

    def handle_nav(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            self.mouse_mode = False
            if event.key == pygame.K_DOWN:
                self.cursor.move_to(direction["down"])
            if event.key == pygame.K_UP:
                self.cursor.move_to(direction["up"])
            if event.key == pygame.K_LEFT:
                self.cursor.move_to(direction["left"])
            if event.key == pygame.K_RIGHT:
                self.cursor.move_to(direction["right"])
        if event.type == pygame.MOUSEMOTION:
            self.mouse_mode = True


class TransparentMenu(Menu):
    def create_blurred_surface(self, color: tuple = gp.BLUE):
        self.transparent_surf = functions.generate_surf((gp.WIDTH, gp.HEIGHT), 150, (0, 0, 0))
        self.text_render = self.game.main_font.render(self.text, True, gp.WHITE)
        self.title_pos = self.text_render.get_rect(center=pygame.Rect(0, 0, gp.WIDTH, gp.HEIGHT).center)
        self.transparent_surf.fill(color)

    def __init__(self, game, text: str = "Place Holder"):
        super().__init__(game)
        self.text = text
        self.create_blurred_surface()

    def resize(self):
        super().resize()
        self.create_blurred_surface()

    def draw(self, blurred_surface):
        self.main_surface.blit(blurred_surface, (0, 0))
        self.main_surface.blit(self.transparent_surf, (0, 0))
        self.main_surface.blit(self.text_render, self.title_pos)
        super().draw()
