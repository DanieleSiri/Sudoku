import pygame
import sys
import sudoku_class
import time

pygame.init()
size = width, height = 756, 756
grey = 240, 240, 240
black = 0, 0, 0
yellow = 255, 255, 0
red = 255, 0, 0
screen = pygame.display.set_mode(size)
Board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
grid = []
font = pygame.font.SysFont("Times New Roman", 80)
part_font = pygame.font.SysFont("Times New Roman", 30)
solver = sudoku_class.SudokuSolver(Board)
current_rect = None


def initialize():
    pygame.display.init()
    screen.fill(grey)
    # initialize grid
    for i in range(1, 4):
        for j in range(1, 4):
            pygame.draw.rect(screen, (0, 0, 0, 0), (0, 0, width // 3 * i, height // 3 * j), 5)
    # rectangle matrix
    for i in range(len(Board[0])):
        grid_y = []
        for j in range(len(Board[1])):
            grid_y.append(pygame.Rect(width // 9 * j, height // 9 * i, width // 9, height // 9))
        grid.append(grid_y)

    for i in range(len(grid[0])):
        for j in range(len(grid[1])):
            pygame.draw.rect(screen, black, grid[i][j], 2)


def initialize_board(board):
    for i in range(len(board[0])):
        for j in range(len(board[1])):
            if board[i][j] != 0:
                print_number(grid[i][j], str(board[i][j]))


def grid_select(mouse_pos):
    """
    Selects the grid in which the mouse is located
    :param mouse_pos: (x, y)
    :return: rect
    """
    x, y = mouse_pos
    for i in range(len(grid[0])):
        for j in range(len(grid[1])):
            if grid[i][j].collidepoint(x, y):
                return grid[i][j]


def cell_coordinates(cell):
    """
    Returns the indexes of a cell corresponding to the indexes of the board
    :param cell: rect
    :return: (x, y)
    """
    for i in range(len(grid[0])):
        for j in range(len(grid[1])):
            if cell.colliderect(grid[i][j]):
                return i, j


def print_number(cell, text):
    """
    Print a number in a grid cell
    :param cell: rect
    :param text: str
    :return: None
    """
    number = font.render(text, 1, black)
    screen.fill(grey, cell.inflate(-5, -10))
    screen.blit(number, number.get_rect(center=cell.center))
    pygame.display.update(cell)


def print_number_part(cell, text):
    """
    Print a number in a grid cell but the number is not the definitive one
    :param cell: rect
    :param text: str
    :return: None
    """
    number = part_font.render(text, 1, black)
    if cell.topleft[0] == 0:  # left border
        screen.fill(grey, cell.inflate(-6, -10))
    else:
        screen.fill(grey, cell.inflate(-5, -10))
    screen.blit(number, cell.topleft)
    solver2.update_board(cell_coordinates(cell), int(text))
    pygame.display.update(cell)


def available_cells(board, grid_list):
    """
    Makes a list of the cells that contain the correct results of the sudoku, therefore making them not overwritable
    :param board: 2d list of int
    :param grid_list: 2d list of rect
    :return: list of rect
    """
    available_cell_list = []
    for i in range(len(board[0])):
        for j in range(len(board[1])):
            if board[i][j] == 0:
                available_cell_list.append(grid_list[i][j])
    return available_cell_list


def remove_available_cell(grid_list, cell):
    """
    Removes 1 element from the available cell list
    :param grid_list: list of rect
    :param cell: rect
    :return: list of rect
    """
    for i in range(len(grid_list)):
        if cell.colliderect(grid_list[i]):
            del grid_list[i]
            break
    return grid_list


def check_available_cell(grid_list, cell):
    """
    Checks if a cell does not hold a valid result
    :param grid_list: 2d list of rect
    :param cell: rect
    :return: bool
    """
    for i in range(len(cell_list)):
        if cell.colliderect(grid_list[i]):
            return True
    return False


def display_popup(status):
    """
    Displays a popup when the cell selected is already solved or when the game is over
    :param status: 0 : invalid, 1 : game over
    :return:
    """
    pygame.image.save(screen, "Screenshot.png")
    popup_font = pygame.font.SysFont("Times New Roman", 40)
    if status == 0:
        popup_text = popup_font.render("Selected invalid cell!", 1, black, yellow)
    elif status == 1:
        popup_text = popup_font.render("Game over!", 1, black, red)
    elif status == 2:
        popup_text = popup_font.render("Number is invalid", 1, black, yellow)
    popup_rect = pygame.Rect(0, 0, width // 3, height // 3)
    popup_rect.center = (width // 2, height // 2)
    pygame.draw.rect(screen, black, popup_rect, 1)
    screen.blit(popup_text, popup_rect.topleft)
    pygame.display.update()
    time.sleep(1)
    image = pygame.image.load("Screenshot.png")
    screen.blit(image, (0, 0))
    pygame.display.flip()
    if status == 1:
        screen.lock()


def confront_cells(board_solved, pos):
    """
    Confronts the values of a partial cell and the solved board and returns if the value is the correct one
    :param board_solved: 2d int
    :param pos: (x, y)
    :return: bool
    """
    if solver2.get_value(pos) == board_solved[pos[0]][pos[1]]:
        return True
    return False


initialize()
initialize_board(Board)
cell_list = available_cells(Board, grid)
solver.solve()
solved_board = solver.copy_board()
solver2 = sudoku_class.SudokuSolver(Board)
while 1:
    for event in pygame.event.get():
        if not screen.get_locked():
            current_mouse_pos = pygame.mouse.get_pos()
            check = pygame.mouse.get_pressed()[0]  # left click
            if check:
                current_rect = grid_select(current_mouse_pos)
            if event.type == pygame.KEYDOWN and current_rect is not None and (pygame.K_9 >= event.key >= pygame.K_1) \
                    and check_available_cell(cell_list, current_rect):
                print_number_part(current_rect, event.unicode)
            if event.type == pygame.KEYDOWN and current_rect is not None and (pygame.K_9 >= event.key >= pygame.K_1) \
                    and not check_available_cell(cell_list, current_rect):
                display_popup(0)
            if event.type == pygame.KEYDOWN and current_rect is not None and event.key == pygame.K_RETURN \
                    and check_available_cell(cell_list, current_rect):
                if confront_cells(solved_board, cell_coordinates(current_rect)):
                    print_number(current_rect, str(solver2.get_value(cell_coordinates(current_rect))))
                    cell_list = remove_available_cell(cell_list, current_rect)
                else:
                    display_popup(2)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                initialize_board(solved_board)
                display_popup(1)
        # quit game
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()
