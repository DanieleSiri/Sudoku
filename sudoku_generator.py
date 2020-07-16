import random
import sudoku_class


def randomize_position():
    random_x = random.randint(0, 8)
    random_y = random.randint(0, 8)
    return random_x, random_y


def randomize_first_box():
    """used to break most easy patterns in the first box"""
    random_x = random.randint(0, 3)
    random_y = random.randint(0, 3)
    return random_x, random_y


class SudokuGenerator:
    def __init__(self, board):
        self.board = sudoku_class.SudokuSolver(board)

    def randomize(self, pos):
        """
        Randomizes the number on board
        :param pos: (x, y)
        :return: None
        """
        random_value = random.randint(1, 9)
        if self.board.valid(pos, random_value):
            self.board.update_board(pos, random_value)
        else:
            self.randomize(pos)

    def generate(self):
        """generates the random board"""
        for i in range(4):
            random_first = randomize_first_box()
            self.randomize(random_first)
        for i in range(9):
            random_pos = randomize_position()
            self.randomize(random_pos)
        self.board.solve()

    def remove_numbers(self):
        """removes some numbers from the solution in order to have the solvable board"""
        for i in range(len(self.board.board[0])):
            while self.board.board[i].count(0) < 6:
                random_val = random.randint(0, 8)
                self.board.update_board((i, random_val), 0)

    def get_board(self):
        return self.board.board
