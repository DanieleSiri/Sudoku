import pygame
import sudoku_class
import time

pygame.init()
color_dict = {'grey': (240, 240, 240),
              'black': (0, 0, 0),
              'yellow': (255, 255, 0),
              'red': (255, 0, 0),
              'white': (255, 255, 255)}


class SudokuGUI:
    def __init__(self, board, width=756, height=756, font="Times New Roman", loading_font="Georgia"):
        # aggiungere check per il font se esiste
        self.width = width
        self.height = height
        self.grid = []
        self.available_cell_list = []
        self.font = pygame.font.SysFont(font, 80)
        self.part_font = pygame.font.SysFont(font, 30)
        self.loading_font = pygame.font.SysFont(loading_font, 25)
        self.title_font = pygame.font.SysFont(loading_font, 80)
        self.solved_board = sudoku_class.SudokuSolver(board)
        self.board = sudoku_class.SudokuSolver(board)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.loading_screen = pygame.display.set_mode((self.width, self.height))

    def initialize(self):
        self.solved_board.solve()
        self.screen.fill(color_dict['grey'])
        # initialize grid
        for i in range(1, 4):
            for j in range(1, 4):
                pygame.draw.rect(self.screen, color_dict['black'], (0, 0, self.width // 3 * i, self.height // 3 * j), 5)
        # rectangle matrix
        for i in range(len(self.board.board[0])):
            grid_y = []
            for j in range(len(self.board.board[1])):
                grid_y.append(pygame.Rect(self.width // 9 * j, self.height // 9 * i, self.width // 9, self.height // 9))
            self.grid.append(grid_y)

        for i in range(len(self.grid[0])):
            for j in range(len(self.grid[1])):
                pygame.draw.rect(self.screen, color_dict['black'], self.grid[i][j], 2)

    def initialize_loading(self):
        """
        Initializes the loading screen
        :return: None
        """
        self.loading_screen.fill(color_dict['white'])
        welcome = self.title_font.render("Welcome!", 1, color_dict['black'])
        press_enter = self.loading_font.render("Press ENTER to play the game", 1, color_dict['red'])
        self.loading_screen.blit(welcome, (self.width//3, self.height//4))
        self.loading_screen.blit(press_enter, (self.width//3, self.height//2.5))
        bottom_rect = pygame.Rect(0, self.height - (self.height//2), self.width, self.height)
        pygame.draw.line(self.loading_screen, color_dict['black'], (0, self.height - (self.height//2)),
                         (self.width, self.height - (self.height//2)), 3)
        pygame.draw.rect(self.loading_screen, color_dict['yellow'], bottom_rect)
        legend_text = {0: "- Left click: select cell",
                       1: "- 1-9: input a number",
                       2: "- ENTER: check if the input number is correct",
                       3: "- SPACE: end the game printing the solution"}
        legend_title = self.loading_font.render("Commands:", 1, color_dict['black'])
        legend = []
        for i in range(len(legend_text)):
            legend.append(self.loading_font.render(legend_text[i], 1, color_dict['black']))
        self.loading_screen.blit(legend_title, bottom_rect.topleft)
        for i in range(len(legend)):
            self.loading_screen.blit(legend[i], (0, self.height - (self.height//2.5) + (50 * i)))
        pygame.display.flip()

    def initialize_board(self):
        for i in range(len(self.board.board[0])):
            for j in range(len(self.board.board[1])):
                if self.board.board[i][j] != 0:
                    self.print_number(self.grid[i][j], str(self.board.board[i][j]))
        self.available_cells()

    def print_solved_board(self):
        for i in range(len(self.solved_board.board[0])):
            for j in range(len(self.solved_board.board[1])):
                self.print_number(self.grid[i][j], str(self.solved_board.board[i][j]))

    def grid_select(self, mouse_pos):
        """
        Selects the grid in which the mouse is located
        :param mouse_pos: (x, y)
        :return: rect
        """
        x, y = mouse_pos
        for i in range(len(self.grid[0])):
            for j in range(len(self.grid[1])):
                if self.grid[i][j].collidepoint(x, y):
                    return self.grid[i][j]

    def cell_coordinates(self, cell):
        """
        Returns the indexes of a cell corresponding to the indexes of the board
        :param cell: rect
        :return: (x, y)
        """
        for i in range(len(self.grid[0])):
            for j in range(len(self.grid[1])):
                if cell.colliderect(self.grid[i][j]):
                    return i, j

    def print_number(self, cell, text):
        """
        Print a number in a grid cell
        :param cell: rect
        :param text: str
        :return: None
        """
        number = self.font.render(text, 1, color_dict['black'])
        self.screen.fill(color_dict['grey'], cell.inflate(-5, -10))
        self.screen.blit(number, number.get_rect(center=cell.center))
        pygame.display.flip()

    def print_number_part(self, cell, text):
        """
        Print a number in a grid cell but the number is not the definitive one
        :param cell: rect
        :param text: str
        :return: None
        """
        number = self.part_font.render(text, 1, color_dict['black'])
        if cell.topleft[0] == 0:  # left border
            self.screen.fill(color_dict['grey'], cell.inflate(-6, -10))
        else:
            self.screen.fill(color_dict['grey'], cell.inflate(-5, -10))
        self.screen.blit(number, cell.topleft)
        self.board.update_board(self.cell_coordinates(cell), int(text))
        pygame.display.update(cell)

    def available_cells(self):
        """
        Makes a list of the cells that contain the correct results of the sudoku, therefore making them not overwritable
        :return: list of rect
        """
        for i in range(len(self.board.board[0])):
            for j in range(len(self.board.board[1])):
                if self.board.board[i][j] == 0:
                    self.available_cell_list.append(self.grid[i][j])
        return self.available_cell_list

    def remove_available_cell(self, cell):
        """
        Removes 1 element from the available cell list
        :param cell: rect
        :return: list of rect
        """
        for i in range(len(self.available_cell_list)):
            if cell.colliderect(self.available_cell_list[i]):
                del self.available_cell_list[i]
                break
        return self.available_cell_list

    def check_available_cell(self, cell):
        """
        Checks if a cell does not hold a valid result
        :param cell: rect
        :return: bool
        """
        for i in range(len(self.available_cell_list)):
            if cell.colliderect(self.available_cell_list[i]):
                return True
        return False

    def display_popup(self, status):
        """
        Displays a popup when the cell selected is already solved or when the game is over
        :param status: 0 : invalid cell, 1 : game over, 2: invalid number
        :return: None
        """
        pygame.image.save(self.screen, "Screenshot.png")
        popup_font = pygame.font.SysFont("Times New Roman", 40)
        if status == 0:
            popup_text = popup_font.render("Selected invalid cell!", 1, color_dict['black'], color_dict['yellow'])
        elif status == 1:
            popup_text = popup_font.render("Game over!", 1, color_dict['black'], color_dict['red'])
        elif status == 2:
            popup_text = popup_font.render("Number is invalid", 1, color_dict['black'], color_dict['yellow'])
        popup_rect = pygame.Rect(0, 0, self.width // 3, self.height // 3)
        popup_rect.center = (self.width // 2, self.height // 2)
        pygame.draw.rect(self.screen, color_dict['black'], popup_rect, 1)
        self.screen.blit(popup_text, popup_rect.topleft)
        pygame.display.update()
        time.sleep(1)
        image = pygame.image.load("Screenshot.png")
        self.screen.blit(image, (0, 0))
        pygame.display.flip()
        if status == 1:
            self.screen.lock()

    def confront_cells(self, pos):
        """
        Confronts the values of a partial cell and the solved board and returns if the value is the correct one
        :param pos: (x, y)
        :return: bool
        """
        if self.board.get_value(pos) == self.solved_board.get_value(pos):
            return True
        return False

    def check_game_over(self):
        """
        Checks if the board is complete
        :return: bool
        """
        for i in range(len(self.board.board[0])):
            for j in range(len(self.board.board[1])):
                if self.board.board[i][j] == 0 or self.board.board[i][j] != self.solved_board.board[i][j]:
                    return False
        return True
