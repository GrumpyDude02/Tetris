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
        text: str = None,
    ) -> None:
        self.list = table
        self.position = position
        self.current_index = 0
        self.button = button
        self.configuration = configuration
        self.template = template
        self.title_text = text
        self.size = size
        self.InitArrows(sc_size[0], sc_size[1], font)

    def InitArrows(self, width: int, height: int, font: pygame.font.Font):
        self.font = font
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
            if self.title_text is not None:
                self.rendered_title = self.font.render(self.title_text, True, self.template.text_color)
                self.title_rect = self.rendered_title.get_rect(
                    centery=self.bounding_rect.centery, right=self.bounding_rect.left - 40
                )
            else:
                self.rendered_title = None
                self.title_rect = None
        else:
            raise Exception("Not Implemented or Invalid configuration")

    def resize(self, sc_size, font):
        self.InitArrows(sc_size[0], sc_size[1], font)

    def update_text(self):
        self.rendered_text = self.font.render(self.list[self.current_index], True, self.template.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.bounding_rect.center)

    def draw(self, surface: pygame.Surface):
        self.arrow1.draw(surface)
        self.arrow2.draw(surface)
        if self.rendered_title:
            surface.blit(self.rendered_title, self.title_rect)
        surface.blit(self.rendered_text, self.text_rect)

    def check_input(self) -> tuple[bool, str]:
        if self.arrow2.check_input():
            self.current_index += 1
            self.current_index %= self.length()
            self.update_text()
            return (True, self.list[self.current_index])
        if self.arrow1.check_input():
            self.current_index -= 1
            self.current_index %= self.length()
            self.update_text()
            return (True, self.list[self.current_index])
        return (False, None)

    def current_item(self):
        return self.list[self.current_index]

    def add_element(self, element):
        self.list.append(element)

    def length(self) -> int:
        return len(self.list)

    def pop(self, index):
        self.list.pop(index)
