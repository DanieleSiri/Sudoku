import pygame
import sys
import sudoku


pygame.init()
loading = True
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
current_rect = None

Sudoku = sudoku.SudokuGUI(Board)
Sudoku.initialize_loading()
while loading:
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            loading = False
Sudoku.initialize()
Sudoku.initialize_board()
while 1:
    for event in pygame.event.get():
        if not Sudoku.screen.get_locked():
            if Sudoku.check_game_over():
                Sudoku.display_popup(1)
            current_mouse_pos = pygame.mouse.get_pos()
            check = pygame.mouse.get_pressed()[0]  # left click
            if check:
                current_rect = Sudoku.grid_select(current_mouse_pos)
            if event.type == pygame.KEYDOWN and current_rect is not None and (pygame.K_9 >= event.key >= pygame.K_1) \
                    and Sudoku.check_available_cell(current_rect):
                Sudoku.print_number_part(current_rect, event.unicode)
            if event.type == pygame.KEYDOWN and current_rect is not None and (pygame.K_9 >= event.key >= pygame.K_1) \
                    and not Sudoku.check_available_cell(current_rect):
                Sudoku.display_popup(0)
            if event.type == pygame.KEYDOWN and current_rect is not None and event.key == pygame.K_RETURN \
                    and Sudoku.check_available_cell(current_rect):
                if Sudoku.confront_cells(Sudoku.cell_coordinates(current_rect)):
                    Sudoku.print_number(current_rect, str(Sudoku.board.get_value(Sudoku.cell_coordinates(current_rect))))
                    Sudoku.remove_available_cell(current_rect)
                else:
                    Sudoku.display_popup(2)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                Sudoku.print_solved_board()
                Sudoku.display_popup(1)
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
