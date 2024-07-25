from random import choice
from queue import PriorityQueue


def create_grid(rows, columns):
    """
    Функция создания первоначальной сетки лабиринта
    :param rows: количество строк
    :param columns: количество столбцов
    :return: сетка лабиринта
    """
    grid = []
    for i in range(0, rows):
        grid.append([])
        for j in range(0, columns):
            grid[i].append([True, True])

    return grid

def sidewinder(grid):
    """
    Функция генерации лабиринта алгоритмом sidewinder
    :param grid: сетка лабиринта
    :return: лабиринт
    """
    rows = len(grid)
    columns = len(grid[0])
    cur_x = 0
    for i in range(0, rows):
        for j in range(0, columns):
            if i == 0:
                if j != columns - 1:
                    grid[i][j][1] = False
            else:
                if choice([0, 1]) == 0 and j != columns - 1:
                    grid[i][j][1] = False
                else:
                    b = choice(range(cur_x, j + 1))
                    grid[i - 1][b][0] = False
                    if j != columns - 1:
                        cur_x = j + 1
                    else:
                        cur_x = 0
    return grid

def create_maze(rows, columns):
    """
    Создание лабиринта
    :param rows: количество строк
    :param columns: количество столбцов
    :return: лабиринт
    """
    return sidewinder(create_grid(rows, columns))

def build_graph(maze, target):
    """
    Создание списка связей между клетками
    :param maze: лабиринт
    :param target: целевая клетка
    :return: список связей между клетками
    """
    rows = len(maze)
    columns = len(maze[0])
    n = rows * columns
    graph = [[] for i in range(n)]
    for i in range(0, rows):
        for j in range(0, columns):
            cur_weight = abs(target[0] - j) + abs(target[1] - i)
            if (not maze[i][j][0]) and i != (rows - 1):
                weight = abs(target[0] - j) + abs(target[1] - (i + 1))
                graph[i * columns + j].append(((i + 1) * columns + j, weight))
                graph[(i + 1) * columns + j].append((i * columns + j, cur_weight))
            if (not maze[i][j][1]) and j != (columns - 1):
                weight = abs(target[0] - (j + 1)) + abs(target[1] - i)
                graph[i * columns + j].append((i * columns + j + 1, weight))
                graph[i * columns + j + 1].append((i * columns + j, cur_weight))
    return graph

def best_first_search(maze, src, target):
    """
    Решение лабиринта алгоритмом Best-first search
    :param maze: лабиринт
    :param src: координаты исходной клетки
    :param target: координаты целевой клетки
    :return: путь решения лабиринта и область "открытая" алгоритмом Best-first search
    """
    rows = len(maze)
    columns = len(maze[0])
    n = rows * columns
    graph = build_graph(maze, target)
    src = src[1] * columns + src[0]
    target = target[1] * columns + target[0]
    visited = [False] * n
    pq = PriorityQueue()
    pq.put((0, src))
    visited[src] = True
    area = []
    while pq.empty() == False:
        u = pq.get()[1]
        area.append(u)
        if u == target:
            break

        for v, c in graph[u]:
            if visited[v] == False:
                visited[v] = True
                pq.put((c, v))

    path = [target]
    cur_node = target
    while cur_node != src:
        for i in graph[cur_node]:
            if (i[0] in area) and area.index(i[0]) < area.index(cur_node):
                path.append(i[0])
                cur_node = i[0]
                break
    path.reverse()
    return path, area