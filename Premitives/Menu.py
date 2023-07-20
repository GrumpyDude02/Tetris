import pygame, random, Tools.functions as functions
import Globals as gp
from GameStates import GameStates
from Tetrominos import Tetrominos
from Tools.Buttons import Buttons


direction = {"up": 0, "right": 1, "down": 2, "left": 3}


class Background:
    def __init__(self, settings) -> None:
        self.objects = []
        self.destroy = []
        self.settings = settings

    def generate_tetromino(self) -> Tetrominos:
        t = Tetrominos(
            [random.randrange(2, (self.settings.width // self.settings.cell_size) - 4, 4), 0],
            random.choice(list(gp.SHAPES.keys())),
            self.settings.cell_size,
        )
        t.SRS_rotate(random.choice([True, False]), random.randint(0, 2))
        return t

    def draw(self, surface):
        surface.fill(gp.BLACK)
        for tetromino in self.objects:
            tetromino.draw(surface)

    def update(self, current_time, dt):
        self.destroy = []
        if current_time - Menu.last_spawn_time > random.randrange(1200, 6000, 500):
            Menu.last_spawn_time = current_time
            self.objects.append(self.generate_tetromino())
        for object in self.objects:
            object.smooth_fall(1, dt)
            if object.pivot.y > self.settings.height // self.settings.cell_size + 5:
                self.destroy.append(object)

    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.objects.remove(tetromino)

    def resize(self):
        for object in self.objects:
            object.resize(self.settings.cell_size)


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
        self.settings = game.settings
        self.background = bg
        self.child_menus = child_menus
        self.previous_menu = previous_menu
        self.do_fade = True
        self.buttons = None
        self.sliders = None
        self.courasels = None
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

    def draw(self, fill_color: tuple = None):
        if fill_color:
            self.main_surface.fill(fill_color)

        if self.background is not None:
            self.background.draw(self.game.screen)
        if self.buttons is not None:
            for key in self.buttons.keys():
                self.buttons[key].draw(self.game.screen)

        if self.sliders is not None:
            for slider in self.sliders.values():
                slider.draw(self.game.screen)

        if self.courasels is not None:
            for courasel in self.courasels.values:
                courasel.draw(self.main_surface)

        if self.cursor is not None:
            self.cursor.draw(self.game.screen)

    def update(self):
        dt = 1 / self.game.clock.tick(gp.FPS)
        if self.background is not None:
            current_time = pygame.time.get_ticks()
            self.background.update(current_time, dt)
        if self.sliders is not None:
            for slider in self.sliders.values():
                slider.update()

    def clean(self):
        if self.background is not None:
            self.background.destroy_tetrominos()

    def resize(self):
        if self.background is not None:
            self.background.resize()
        if self.buttons is not None:
            for button in self.buttons.values():
                button.resize((self.settings.width, self.settings.height), self.game.main_font)
        if self.sliders is not None:
            for slider in self.sliders.values():
                slider.resize((self.settings.width, self.settings.height), self.game.main_font)
        if self.cursor is not None:
            self.cursor.set_attr()

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

    def handle_events(self):
        raise Exception("Not yet implemented")

    def fade(self, direction, condition):
        last_tick = 0
        current_time = pygame.time.get_ticks()
        while condition(self.game.alpha) and self.do_fade:
            if current_time - last_tick > 10:
                if direction == "in":
                    self.game.alpha -= 10
                elif direction == "out":
                    self.game.alpha += 10
                self.game.transition_surface.set_alpha(self.game.alpha)
                last_tick = current_time
            current_time = pygame.time.get_ticks()
            self.handle_events()
            self.update()
            self.draw()
            self.game.screen.blit(self.game.transition_surface, (0, 0))
            pygame.display.flip()
            self.clean()


class TransparentMenu(Menu):
    def create_blurred_surface(self, color: tuple = gp.BLUE):
        self.transparent_surf = functions.generate_surf((self.settings.width, self.settings.height), 150, (0, 0, 0))
        self.back_surface = None
        self.text_render = self.game.main_font.render(self.text, True, gp.WHITE)
        self.title_pos = self.text_render.get_rect(
            center=pygame.Rect(0, 0, self.settings.width, self.settings.height).center
        )
        self.transparent_surf.fill(color)

    def __init__(self, game, text: str = "Place Holder"):
        super().__init__(game)
        self.text = text
        self.create_blurred_surface()

    def resize(self):
        super().resize()
        self.create_blurred_surface()

    def draw(self):
        self.game.screen.blit(self.back_surface, (0, 0))
        self.game.screen.blit(self.transparent_surf, (0, 0))
        self.game.screen.blit(self.text_render, self.title_pos)
        super().draw()
