import pygame
import Globals as gp
import json
import Tools.functions as functions
from Editor import Editor

# Define your window dimensions and other settings
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CELL_SIZE = 25
PLAYABLE_AREA_CELLS = gp.PLAYABLE_AREA_CELLS
BOARD_Y_CELL_NUMBER = gp.BOARD_Y_CELL_NUMBER

# Set up Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Editor Test")


# Define your settings object and Editor instance
class Settings:
    def __init__(self, board_width, board_height, cell_size):
        self.board_width = board_width
        self.board_height = board_height
        self.width = 600
        self.height = 600
        self.cell_size = cell_size
        self.grid = []
        for i in range(0, gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT):
            for j in range(gp.PLAYABLE_AREA_CELLS + gp.X_BORDER_OFFSET):
                if j == 0 or j == gp.PLAYABLE_AREA_CELLS + gp.X_BORDER_OFFSET - 1:
                    self.grid.append(
                        pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                    )
                elif i == 0 or i == gp.BOARD_Y_CELL_NUMBER - gp.BOARD_SHIFT - 1:
                    self.grid.append(
                        pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1)
                    )


settings = Settings(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
editor = Editor(None, settings)  # Pass game as None since it's not required in the constructor

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the update and draw methods of the editor
    editor.update()

    window.fill((255, 255, 255))  # Fill the window with white color
    # Draw your board or any other elements here if required.

    editor.draw(window)  # Call the draw method of the editor to draw the blocks

    pygame.display.flip()  # Update the display

# Quit Pygame
pygame.quit()
