import pygame

class Cell:
    def __init__(self, value, row, col, screen, width, height):
        # Initialize the Cell object with given parameters
        self.value = value  # The value of the cell
        self.row = row      # The row index of the cell
        self.col = col      # The column index of the cell
        self.screen = screen  # The surface to draw the cell on
        self.width = width    # The width of the cell
        self.height = height  # The height of the cell
        self.sketched_value = 0  # The sketched value of the cell
        self.is_selected = False  # Flag to indicate if the cell is selected
        self.locked = value != 0

    def set_cell_value(self, value):
        # Set the value of the cell
        if not self.locked:
            self.value = value

    def set_sketched_value(self, value):
        if not self.locked:
            self.sketched_value = value

    def draw(self):
        # Draw the cell on the screen
        x = self.col * self.width
        y = self.row * self.height

        # Draw cell border
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.width, self.height), 1)

        # Highlight selected cell
        if self.is_selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.width, self.height), 2)

        font = pygame.font.Font(None, 36)

        # Draw cell value or sketched value
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + self.width // 2 - text.get_width() // 2, y + self.height // 2 - text.get_height() // 2))
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, (200, 200, 200))
            self.screen.blit(text, (x + 5, y + 5))

    def select(self):
        # Select the cell
        self.is_selected = True

    def deselect(self):
        # Deselect the cell
        self.is_selected = False
