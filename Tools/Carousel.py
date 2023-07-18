import pygame, pygame.gfxdraw
from Tools.Buttons import TextButtons, Arrow, ButtonTemplate, DefaultTemplate


class Carousel:
    ARROW_WIDTH = 0.12
    ARROW_HEIGHT = 0.5
    ARROW_Y_POS = (1 - ARROW_HEIGHT) / 2

    def __init__(
        self,
        table: list[str],
        template: ButtonTemplate,
        position: tuple,
        font: pygame.font.Font,
        size: tuple,
        sc_size: tuple = (1, 1),
        button: TextButtons = None,
        configuration: str = "horizontal",
    ) -> None:
        self.list = table
        self.len = len(self.list)
        self.font = font
        self.position = position
        self.current_index = 0
        self.button = button
        self.configuration = configuration
        self.template = template
        self.size = size
        self.InitArrows(sc_size[0], sc_size[1], font)

    def InitArrows(self, width: int, height: int, font: pygame.font.Font):
        self.bounding_rect = pygame.Rect(
            round(self.position[0] * width),
            round(self.position[1] * height),
            round(self.size[0] * width),
            round(self.size[1] * height),
        )
        if self.configuration == "horizontal":
            self.arrow1 = Arrow(
                "left",
                template=self.template,
                size=(self.bounding_rect.width * Carousel.ARROW_WIDTH, self.bounding_rect.height * Carousel.ARROW_HEIGHT),
                pos=(self.bounding_rect.left, self.bounding_rect.top + self.bounding_rect.height * Carousel.ARROW_Y_POS),
            )
            self.update_text()
            self.arrow2 = Arrow(
                "right",
                template=self.template,
                size=(self.bounding_rect.width * Carousel.ARROW_WIDTH, self.bounding_rect.height * Carousel.ARROW_HEIGHT),
                pos=(
                    self.bounding_rect.right - self.bounding_rect.width * Carousel.ARROW_WIDTH,
                    self.bounding_rect.top + self.bounding_rect.height * Carousel.ARROW_Y_POS,
                ),
            )
        else:
            raise Exception("Not Implemented or Invalid configuration")

    def update_text(self):
        self.rendered_text = self.font.render(self.list[self.current_index], True, self.template.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.bounding_rect.center)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 0, 0), self.bounding_rect)
        self.arrow1.draw(surface)
        self.arrow2.draw(surface)
        surface.blit(self.rendered_text, self.text_rect)

    def update(self):
        if self.arrow2.check_input():
            self.current_index += 1
            self.current_index %= self.len
            self.update_text()
        elif self.arrow1.check_input():
            self.current_index -= 1
            self.current_index %= self.len
            self.update_text()