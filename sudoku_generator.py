import random

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.original_board = [row[:] for row in self.board]
        self.box_length = row_length

    def get_board(self):
        return self.board

    def get_original_board(self):
        return self.original_board

    def print_board(self):
        for row in self.board:
            print(" ".join(str(x) for x in row))

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[i][col] for i in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for row in range(3):
            for col in range(3):
                if self.board[row_start + row][col_start + col] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (
                self.valid_in_row(row, num)
                and self.valid_in_col(col, num)
                and self.valid_in_box(row - row % 3, col - col % 3, num)
        )

    def fill_box(self, row_start, col_start):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for row in range(3):
            for col in range(3):
                self.board[row_start + row][col_start + col] = numbers.pop(0)

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self, row=0, col=0):
        if col >= self.row_length:
            row += 1
            col = 0
        if row >= self.row_length:
            return True
        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0

        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        count = self.removed_cells
        while count > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1


def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    generator.fill_values()
    generator.remove_cells()
    return generator.get_board()


def generate_original_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    return generator.get_original_board()
