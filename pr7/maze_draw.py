import pygame

import maze_work


WALL_COLOR = (255, 255, 255)
FLOOR_COLOR = (0, 0, 0)
PATH_COLOR = (255, 165, 0)
AREA_COLOR = (127, 127, 127)

def maze_to_text_file(maze, file):
    """
    Экспорт лабирина в текстовый файл
    :param maze: лабиринт
    :param file: текстовый файл
    """
    rows = len(maze)
    columns = len(maze[0])
    file.writelines([str(rows) + ' ' + str(columns) + '\n'])
    for i in range(0, rows):
        for j in range(0, columns):
            file.writelines([str(int(maze[i][j][0])) + ' ' + str(int(maze[i][j][1])) + '\n'])

def text_file_to_maze(file):
    """
    Импорт лабиринта из текстового файла
    :param file: текстовый файл
    :return: лабиринт
    """
    rows, columns = map(int, file.readline().split())
    maze = []
    for i in range(0, rows):
        maze.append([])
        for j in range(0, columns):
            maze[i].append(list(map(bool, list(map(int,  file.readline().split())))))
    return maze

def pic_to_maze(surf: pygame.surface, cell_side):
    """
    Создание лабиринта по pygame поверхности
    :param surf: pygame поверхность
    :param cell_side: размер стороны клетки
    :return: лабиринт
    """
    columns = 0
    rows = 0
    print(1)
    print(99999)
    while surf.get_at((columns * cell_side, 0)) == WALL_COLOR:
        columns += 1
    columns -= 1
    print(columns)
    while surf.get_at((0, rows * cell_side)) == WALL_COLOR:
        rows += 1
    rows -= 1
    print(rows)
    if columns < 2 or rows < 2:
        return None

    maze = []
    for i in range(0, rows):
        maze.append([])
        for j in range(0, columns):
            bottom = (surf.get_at((int(j * cell_side + cell_side / 2), ((i + 1) * cell_side))) == WALL_COLOR)
            right = (surf.get_at((int((j + 1) * cell_side), int(i * cell_side + cell_side / 2))) == WALL_COLOR)
            maze[i].append([bottom, right])

    return maze

def cell_choose(choosed_cells, rows, columns, cell_side):
    """
    Функция добавления клетки в список выбранных клеток по положению курсора
    :param choosed_cells: выбранные клетки
    :param rows: количество строк
    :param columns: количество столбцов
    :param cell_side: размер стороны клетки
    :return: изменённый список выбранных клеток
    """
    x, y = pygame.mouse.get_pos()
    cell_x, cell_y = x // cell_side, y // cell_side
    if cell_y < rows and cell_x < columns:
        choosed_cells.append((cell_x, cell_y))
    return choosed_cells

def maze_draw(rows, columns, output_text_file = '', output_pic_file = '', input_text_file = '', input_pic_file = ''):
    """
    Функция отображения генерации лабиринта и его решения
    :param rows: количество строк
    :param columns: количество столбцов
    :param output_text_file: путь текстового файла для экспорта
    :param output_pic_file: название файла изображение для экспорта
    :param input_text_file: путь текстового файла для импорта
    :param input_pic_file: название файла изображение для импорта
    """
    cell_side = 20
    if input_text_file != '':
        try:
            with open(input_text_file, 'r') as input_text_f:
                maze = text_file_to_maze(input_text_f)
                rows = len(maze)
                columns = len(maze[0])
        except FileNotFoundError:
            maze = maze_work.create_maze(rows, columns)
    elif input_pic_file != '':
        try:
            surf = pygame.image.load(input_pic_file)
            print(99999)
            maze = pic_to_maze(surf, cell_side)
            if maze is None:
                maze = maze_work.create_maze(rows, columns)
            else:
                rows = len(maze)
                columns = len(maze[0])
        except FileNotFoundError:
            maze = maze_work.create_maze(rows, columns)
    else:
        maze = maze_work.create_maze(rows, columns)
    if output_text_file != '':
        try:
            with open(output_text_file, 'w') as output_text_f:
                maze_to_text_file(maze, output_text_f)
        except FileNotFoundError:
            pass
    if output_pic_file != '':
        save_pic = True
    else:
        save_pic= False

    width = (columns * cell_side + cell_side) * 2
    height = (rows * cell_side + cell_side) * 2
    pygame.init()
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    run = True
    choosed_cells = []
    path, area = None, None
    shift = columns * cell_side + cell_side

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                choosed_cells = cell_choose(choosed_cells, rows, columns, cell_side)
        window.fill(FLOOR_COLOR)
        pygame.draw.line(window, WALL_COLOR, [0, 0], [columns * cell_side, 0])
        pygame.draw.line(window, WALL_COLOR, [0, 0], [0, rows * cell_side])
        for i in range(0, rows):
            for j in range(0, columns):
                if maze[i][j][0]:
                    pygame.draw.line(window, WALL_COLOR, [j * cell_side, (i + 1) * cell_side], [(j + 1) * cell_side, (i + 1) * cell_side])
                if maze[i][j][1]:
                    pygame.draw.line(window, WALL_COLOR, [(j + 1) * cell_side, i * cell_side], [(j + 1) * cell_side, (i + 1) * cell_side])

        if save_pic:
            try:
                pygame.image.save(window, output_pic_file)
                save_pic = False
            except :
                save_pic = False

        if len(choosed_cells) == 2:
            if choosed_cells[0] != choosed_cells[1]:
                print(choosed_cells)
                path, area = maze_work.best_first_search(maze, choosed_cells[0], choosed_cells[1])
                pass
            choosed_cells = []
        if not(path is None):
            pygame.draw.line(window, WALL_COLOR, [shift, 0], [shift + columns * cell_side, 0])
            pygame.draw.line(window, WALL_COLOR, [shift, 0], [shift, rows * cell_side])
            for i in range(0, rows):
                for j in range(0, columns):
                    if maze[i][j][0]:
                        pygame.draw.line(window, WALL_COLOR, [shift + j * cell_side, (i + 1) * cell_side],
                                         [shift + (j + 1) * cell_side, (i + 1) * cell_side])
                    if maze[i][j][1]:
                        pygame.draw.line(window, WALL_COLOR, [shift + (j + 1) * cell_side, i * cell_side],
                                         [shift + (j + 1) * cell_side, (i + 1) * cell_side])
                    if (i * columns + j) in path:
                        pygame.draw.rect(window, PATH_COLOR, (shift + j * cell_side + 1, i * cell_side + 1, cell_side - 1, cell_side - 1))
                    elif (i * columns + j) in area:
                        pygame.draw.rect(window, AREA_COLOR, (shift + j * cell_side + 1, i * cell_side + 1, cell_side - 1, cell_side - 1))

        pygame.display.flip()

    pygame.quit()
    exit()

if __name__ == "__main__":
    maze_draw(10, 10)