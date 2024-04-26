import pygame
from cell import Cell

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.screen = screen
        self.width = width
        self.height = height
        self.difficulty = difficulty

        self.board = []
        self.original_board = []
        self.cells = []
        self.selected = None
        self.load_board()

    def load_board(self):
        if self.difficulty == "easy":
            empty_cells = 30
        elif self.difficulty == "medium":
            empty_cells = 40
        else:
            empty_cells = 50

        from sudoku_generator import generate_sudoku
        self.board = generate_sudoku(9, empty_cells)


        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                value = self.board[row][col]
                cell = Cell(value, row, col, self.screen, self.width / 9, self.height / 9)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def draw(self):
        # Draw the grid lines
        box_width = self.width / 3
        box_height = self.height / 3

        for i in range(10):
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (0, i * self.height / 9),
                (self.width, i * self.height / 9),
                2 if i % 3 == 0 else 1
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (i * self.width / 9, 0),
                (i * self.width / 9, self.height),
                2 if i % 3 == 0 else 1
            )

        # Draw each cell
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected:
            self.selected.deselect()
        self.selected = self.cells[row][col]
        self.selected.select()

    def click(self, x, y):
        row = int(y // (self.height / 9))
        col = int(x // (self.width / 9))
        if 0 <= row < 9 and 0 <= col < 9:
            return row, col
        return None

    def place_number(self, value):
        if self.selected:
            self.selected.set_cell_value(value)

    def sketch(self, value):
        if self.selected:
            self.selected.set_sketched_value(value)

    def clear(self):
        if self.selected:
            self.selected.set_cell_value(0)

    def reset_to_original(self):

        if self.difficulty == "easy":
            empty_cells = 30
        elif self.difficulty == "medium":
            empty_cells = 40
        else:
            empty_cells = 50

        from sudoku_generator import generate_original_sudoku
        self.original_board = generate_original_sudoku(9, empty_cells)


        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                value = self.board[row][col]
                cell = Cell(value, row, col, self.screen, self.width / 9, self.height / 9)
                row_cells.append(cell)
            self.cells.append(row_cells)
    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.board[row][col] = self.cells[row][col].value

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return row, col
        return None

    def check_board(self):
        # Check rows, columns, and boxes for duplicates
        # Rows
        for row in self.board:
            if len(set(row)) != 9:
                return False

        # Columns
        for col in range(9):
            column = [self.board[row][col] for row in range(9)]
            if len(set(column)) != 9:
                return False

        # Boxes
        for box_start_row in range(0, 9, 3):
            for box_start_col in range(0, 9, 3):
                box_values = []
                for row in range(3):
                    for col in range(3):
                        box_values.append(self.board[box_start_row + row][box_start_col + col])
                if len(set(box_values)) != 9:
                    return False

        return True
