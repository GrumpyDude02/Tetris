import pygame, pygame.gfxdraw
from Tools.Buttons import Buttons


class Arrow:
    def __init__(
        self,
        position: tuple,
        size: tuple,
        direction: str,
        sc_size: tuple = (1, 1),
        color: tuple = (255, 255, 255),
        bg_color: tuple = (0, 0, 0),
    ) -> None:
        self.position = position
        self.size = size
        self.direction = direction
        self.color = color
        self.bg_color = bg_color
        try:
            self.set_vertecies(sc_size[0], sc_size[1])
        except:
            print("Failure")

    def set_vertecies(self, width, height) -> None:
        x = self.position[0]
        y = self.position[1]
        size = self.size
        if self.direction == "left":
            self.vertecies = [
                (round((x)), round((y + size[1] / 2) * height)),
                (round((x + size[0]) * width), round(y * height)),
                (round((x + size[0]) * width), round((y + size[1]) * height)),
            ]
        elif self.direction == "right":
            self.vertecies = [
                (round((x) * width), round(y * height)),
                (round((x + size[0]) * width), round((y + size[1] / 2) * height)),
                (round(x * width), round((y + size[1]) * height)),
            ]
        elif self.direction == "top":
            self.vertecies = [
                (round((x + size[0] / 2) * width), round(y * height)),
                (round(x * width), round((y + size[1]) * height)),
                (round((x + size[0]) * width), round((y + size[1]) * height)),
            ]
        elif self.direction == "bottom":
            self.vertecies = [
                (round(x * width), round(y * height)),
                (round((x + size[0]) * width), round((y + size[1] / 2) * height)),
                (round((x + size[1]) * width), round((y + size[1]) * height)),
            ]
        else:
            raise Exception("Direction must be str and either top, bottom, left or right")
        self.bounding_rect = pygame.Rect(
            self.position[0] * width,
            self.position[1] * height,
            self.size[0] * width,
            self.size[1] * height,
        )

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.bg_color, self.bounding_rect)
        pygame.draw.aalines(
            surface=surface,
            color=self.color,
            closed=True,
            points=self.vertecies,
        )

    def update(self) -> bool:
        if self.bounding_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True


class Carousel:
    def __init__(
        self,
        table: list[str],
        position: tuple,
        font: pygame.font.Font,
        size: tuple,
        sc_size: tuple = (1, 1),
        button: Buttons = None,
        color: tuple = (255, 255, 255),
        bg_color: tuple = (255, 255, 255),
        configuration: str = "horizontal",
    ) -> None:
        self.list = table
        self.len = len(self.list)
        self.color = color
        self.bg_color = bg_color
        self.position = position
        self.current_index = 0
        self.button = button
        self.configuration = configuration
        self.size = size

    def resize(self, width: int, height: int, font: pygame.font.Font):
        self.bounding_rect = pygame.Rect(
            round(self.position[0] * width),
            round(self.position[1] * height),
            round(self.size[0] * width),
            round(self.size[1] * height),
        )
        if self.configuration == "horizontal":
            self.arrow1 = Arrow(
                self.bounding_rect.topleft,
                (self.bounding_rect.width * 0.2, self.bounding_rect.height),
                "left",
            )
            self.rendered_text = font.render(self.list[self.current_index], True, self.color)
            self.text_rect = self.rendered_text.get_rect(center=self.bounding_rect.center)
            self.arrow2 = Arrow(
                (self.bounding_rect.right - self.bounding_rect.width * 0.2, self.bounding_rect.top),
                (self.bounding_rect.width * 0.2, self.bounding_rect.height),
                "right",
            )
        else:
            raise Exception("Not Implemented or Invalid configuration")

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.bg_color, self.bounding_rect)
        self.arrow1.draw(surface)
        self.arrow2.draw(surface)
        surface.blit(self.rendered_text, self.text_rect)

    def update(self):
        if self.arrow1.update():
            self.current_index += 1
            self.current_index %= self.len
        elif self.arrow2.update():
            self.current_index -= 1
            self.current_index %= self.len
