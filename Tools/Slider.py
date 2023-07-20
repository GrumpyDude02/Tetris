import pygame
from Tools.Buttons import Buttons, ButtonTemplate, DefaultTemplate
import Tools.functions as func


class Slider:
    ARMED = "ARMED"
    HOVER = "HOVER"
    IDLE = "IDLE"

    def __init__(
        self,
        template: ButtonTemplate,
        text: str,
        font: pygame.font.Font,
        position: tuple,
        size: tuple,
        slide_range: tuple,
        sc_size: tuple = (1, 1),
        rounding: bool = False,
    ) -> None:
        self.position = position
        self.template = template
        self.size = size
        self.state = Slider.IDLE
        self.range = slide_range
        self.output = self.range[0]
        self.round = rounding
        self.button_color = self.template.bg_color
        self.text = text
        self.resize(sc_size, font)

    def resize(self, sc_size, font):
        self.font = font
        self.rendered_text = font.render(self.text, True, self.template.text_color)
        self.rectangle_bar = pygame.Rect(
            self.position[0] * sc_size[0],
            self.position[1] * sc_size[1],
            self.size[0] * sc_size[0],
            self.size[1] * sc_size[1],
        )
        self.text_position = (
            self.position[0] * sc_size[0] - self.rendered_text.get_width() - 40,
            self.position[1] * sc_size[1],
        )

        button_size = (max(self.rectangle_bar.width * 0.04, 10), max(self.rectangle_bar.height * 1.5, 30))

        button_position = (
            self.rectangle_bar.left - self.rectangle_bar.width * 0.04 / 2,
            self.rectangle_bar.centery - self.rectangle_bar.height * 1.5 / 2,
        )

        self.button_rect = pygame.Rect(button_position, button_size)

        self.button_outline = (
            pygame.Rect(
                self.button_rect.left - self.template.outline_size,
                self.button_rect.top - self.template.outline_size,
                self.button_rect.width + self.template.outline_size * 2,
                self.button_rect.height + self.template.outline_size * 2,
            )
            if self.template.outline_size > 0
            else None
        )

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_color = self.template.bg_color
        if self.rectangle_bar.collidepoint(mouse_pos):
            self.state = Slider.HOVER
            self.button_color = self.template.hover_color
            if pygame.mouse.get_pressed()[0]:
                self.state = Slider.ARMED
        if not pygame.mouse.get_pressed()[0]:
            self.state = Slider.IDLE
        if self.state == Slider.ARMED:
            self.button_color = self.template.hover_color
            self.button_rect.centerx = max(
                self.rectangle_bar.left,
                min(mouse_pos[0], self.rectangle_bar.width + self.rectangle_bar.left),
            )
            self.output = round(
                func.map_values(
                    self.button_rect.centerx,
                    (self.rectangle_bar.left, self.rectangle_bar.left + self.rectangle_bar.width),
                    self.range,
                )
            )
            if self.round:
                self.button_rect.centerx = func.map_values(
                    self.output,
                    self.range,
                    (self.rectangle_bar.left, self.rectangle_bar.left + self.rectangle_bar.width),
                )
            self.button_outline.center = self.button_rect.center

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface,
            self.template.slider_bar_color,
            self.rectangle_bar,
            self.template.slider_bar_width,
            border_radius=self.template.slider_bar_radius,
        )
        pygame.draw.rect(
            surface, self.template.outline_color, self.button_outline, border_radius=self.template.outline_radius
        )
        output = self.font.render(str(self.output), True, self.template.text_color)
        if self.button_outline:
            pygame.draw.rect(surface, self.button_color, self.button_rect, border_radius=self.template.border_radius)
        surface.blit(
            output,
            (self.rectangle_bar.left + self.rectangle_bar.width + 10, self.rectangle_bar.top - 1),
        )
        surface.blit(
            self.rendered_text,
            self.text_position,
        )
