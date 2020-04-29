import copy


class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        # solve the board
        position = self.find_empty()
        if not position:
            return True

        for num in range(1, 10):
            # if number is valid, assign it to the position
            if self.valid(position, num):
                self.update_board(position, num)

                if self.solve():
                    return True

                # if consecutive recursion call is invalid, assign the value to 0 and try with the number incremented
                # by 1
                self.update_board(position, 0)

        return False

    def valid(self, pos, num):
        """
        checks if the number is valid
        :param pos: position in the board (row, col)
        :param num: number to check (int)
        :return: boolean
        """
        # check row
        for i in range(len(self.board[1])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # check column
        for i in range(len(self.board[0])):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # check box
        box_x = pos[0]//3
        box_y = pos[1]//3
        for i in range((box_x * 3), (box_x * 3 + 3)):
            for j in range((box_y * 3), (box_y * 3 + 3)):
                if self.board[i][j] == num and pos != (i, j):
                    return False
        return True

    def find_empty(self):
        # find empty slot on the board and returns its position
        for i in range(len(self.board[0])):
            for j in range(len(self.board[1])):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def update_board(self, pos, num):
        """
        Updates the value inside 1 cell of the board
        :param pos: (x, y)
        :param num: int
        :return: None
        """
        self.board[pos[0]][pos[1]] = num

    def get_value(self, pos):
        return self.board[pos[0]][pos[1]]

    def copy_board(self):
        return copy.deepcopy(self.board)
