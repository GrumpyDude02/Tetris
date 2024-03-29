import pygame, random, Tools.functions as functions
import Globals as gp
from GameStates import GameStates
from Tetrominos import Tetrominos
from Tools.Buttons import Buttons
from Tools.Particles import Particle


direction = {"up": 0, "right": 1, "down": 2, "left": 3}


class Background:
    def __init__(self, settings) -> None:
        self.objects = []
        self.destroy = []
        self.settings = settings
        self.generate_particles()

    def generate_tetromino(self) -> Tetrominos:
        t = Tetrominos(
            [random.randrange(2, (self.settings.width // self.settings.cell_size) - 4, 4), 0],
            random.choice(list(gp.SHAPES.keys())),
            self.settings.cell_size,
            state=0,
        )
        t.SRS_rotate(random.choice([True, False]), random.randint(0, 2))
        return t

    def generate_particles(self):
        n = random.randint(100, 300)
        self.particles = [
            Particle(
                [random.randint(0, self.settings.width), random.randint(-10, self.settings.height)],
                (0, 0),
                None,
                random.uniform(0.5, 2),
                None,
            )
            for k in range(n)
        ]

    def draw(self, surface):
        surface.fill(gp.BLACK)
        for particle in self.particles:
            pygame.draw.circle(surface, particle.color, particle.pos, particle.size)
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

        for particle in self.particles:
            particle.pos[1] += 10 * dt
            if particle.pos[1] > self.settings.height + 5:
                particle.pos = [random.randint(0, self.settings.width), -50]

    def destroy_tetrominos(self):
        for tetromino in self.destroy:
            self.objects.remove(tetromino)

    def resize(self):
        for object in self.objects:
            object.resize(self.settings.cell_size)
        self.generate_particles()


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

    def __init__(self, game, state, child_menus: list = None, previous_menu=None, bg: Background = None):
        self.game = game
        self.settings = game.settings
        self.background = bg
        self.child_menus = child_menus
        self.previous_menu = previous_menu
        self.do_fade = True
        self.buttons = {}
        self.sliders = {}
        self.carousels = {}
        self.cursor = None
        self.mouse_mode = True
        self.state = state

    def set_state(self, new_state, pending_state: str = None, last_played_mode=None):
        self.game.set_state(new_state, pending_state, last_played_mode)

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

        for button in self.buttons.values():
            button.draw(self.game.screen)

        for slider in self.sliders.values():
            slider.draw(self.game.screen)

        for carousel in self.carousels.values():
            carousel.draw(self.game.screen)

        if self.cursor is not None:
            self.cursor.draw(self.game.screen)

    def update(self):
        dt = 1 / (self.game.clock.tick(gp.FPS) + 1e-16)
        if self.background is not None:
            current_time = pygame.time.get_ticks()
            self.background.update(current_time, dt)
        for slider in self.sliders.values():
            slider.update()

    def clean(self):
        if self.background is not None:
            self.background.destroy_tetrominos()

    def resize(self):
        if self.background is not None:
            self.background.resize()
        for button in self.buttons.values():
            button.resize((self.settings.width, self.settings.height), self.game.main_font)
        for slider in self.sliders.values():
            slider.resize((self.settings.width, self.settings.height), self.game.main_font)
        for carousel in self.carousels.values():
            carousel.resize((self.settings.width, self.settings.height), self.game.main_font)

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
        if self.mouse_mode and self.cursor is not None:
            for value in self.buttons.values():
                value.move_cursor(self.cursor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameStates.quitting)
            elif event.type == pygame.KEYDOWN:
                self.mouse_mode = False
                self.handle_nav(event)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_mode = True
            elif event.type == pygame.VIDEORESIZE:
                self.settings.set_resolution((event.w, event.h))
                self.set_state(GameStates.changing_res, pending_state=self.state)

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

    def loop(self):
        self.fade("in", lambda alpha: alpha > 0)
        while self.game.state == self.state:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.background.destroy_tetrominos()
        self.fade("out", lambda alpha: alpha < 255)


class TransparentMenu(Menu):
    def create_blurred_surface(self, color: tuple = gp.BLUE):
        self.transparent_surf = functions.generate_surf((self.settings.width, self.settings.height), 150, (0, 0, 0))
        self.back_surface = None
        self.text_render = self.game.main_font.render(self.text, True, gp.WHITE)
        self.title_pos = self.text_render.get_rect(
            center=pygame.Rect(0, 0, self.settings.width, self.settings.height).center
        )
        self.transparent_surf.fill(color)

    def __init__(self, game, state, text: str = "Place Holder"):
        super().__init__(game, state)
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

    def loop(self, surface):
        self.back_surface = pygame.transform.gaussian_blur(surface, 4, False)
        self.fade("in", lambda alpha: alpha > 0)
        while self.game.state == self.state:
            self.handle_events()
            self.draw()
            pygame.time.Clock().tick(gp.FPS)
            pygame.display.flip()
        self.fade("out", lambda alpha: alpha < 255)
