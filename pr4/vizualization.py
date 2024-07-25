import pygame
import random
from typing import *

width = 800
height = 600

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Сортировка')
clock = pygame.time.Clock()
elements = 100
FPS = 100

def random_array():
    """
    получение случайного списка
    :return: случайный список
    """
    array = []
    for i in range(elements):
        array.append(i)
    random.shuffle(array)
    return array


def draw(array, pivot, key):
    """
    Отрисовка столбиков списка
    :param array: список
    :param pivot: текущий элемент
    :param key:
    :return:
    """
    screen.fill((0, 0, 0))
    for i in range(0, len(array)):
        rect = pygame.Rect((width // elements) * i, height - key(array[i]) * (height // elements),
                           (width // elements),
                           key(array[i]) * (height // elements))
        if i == pivot:
            pygame.draw.rect(screen, 'white', rect)
            pygame.draw.line(screen, 'white', rect.topleft, rect.topright, 1)
            pygame.draw.line(screen, 'white', rect.topright, rect.bottomright, 1)
            pygame.draw.line(screen, 'white', rect.topleft, rect.bottomleft, 1)
            pygame.draw.line(screen, 'white', rect.bottomleft, rect.bottomright, 1)
        else:
            pygame.draw.rect(screen, 'red', rect)
            pygame.draw.line(screen, 'red', rect.topleft, rect.topright, 1)
            pygame.draw.line(screen, 'red', rect.topright, rect.bottomright, 1)
            pygame.draw.line(screen, 'red', rect.topleft, rect.bottomleft, 1)
            pygame.draw.line(screen, 'red', rect.bottomleft, rect.bottomright, 1)


def quick_sort_visualization(arr, fst, lst, key, cmp):
    """
    Quicksort с визализацией
    :param arr: список
    :param fst: левая граница
    :param lst: правая граница
    :param key: функция для нахождения значения элемента
    :param cmp: функция для сравнивания элементов
    :return:
    """
    pivot_index = (lst + fst) // 2
    draw(arr, pivot_index, key)
    clock.tick(FPS)
    pygame.display.flip()
    if fst >= lst: return

    i, j = fst, lst
    pivot = arr[pivot_index]

    while i <= j:
        while cmp(key(arr[i]), key(pivot)):
            i += 1
        while cmp(key(pivot), key(arr[j])):
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i, j = i + 1, j - 1
    quick_sort_visualization(arr, fst, j, key, cmp)
    quick_sort_visualization(arr, i, lst, key, cmp)

def my_sort_visualization(array: list, reverse: bool=False,key: Optional[Callable]=None, cmp: Optional[Callable]=None) -> list:
    """
    получение отсортированного списка с визуализацией
    :param array: список
    :param reverse: флаг обратной сортировки
    :param key: функция для нахождения значения элемента
    :param cmp: функция для сравнивания элементов
    :return: отсортированный список
    """
    global elements
    elements = len(array)
    if key == None:
        key = lambda a: a
    if cmp == None:
        cmp = lambda a, b: a < b
    if reverse == True:
        cmp_2 = lambda a, b: cmp(b, a)
    else:
        cmp_2 = cmp
    quick_sort_visualization(array, 0, len(array) - 1, key, cmp_2)
    return array

def execute(array: list=None, reverse: bool=False,key: Optional[Callable]=None, cmp: Optional[Callable]=None):
    """
    Запуск цикла pygame
    :param array: список
    :param reverse: флаг обратной сортировки
    :param key: функция для нахождения значения элемента
    :param cmp: функция для сравнивания элементов
    """
    global elements
    run = True
    start_draw = False
    if array == None:
        array = random_array()
    else:
        elements = len(array)
    if key == None:
        key = lambda a: a
    draw(array, 0, key)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if start_draw:
            start_draw = False
            my_sort_visualization(array, reverse, key, cmp)
        pykey = pygame.key.get_pressed()
        if pykey[pygame.K_SPACE]:
            start_draw = True
        if pykey[pygame.K_r]:
            start_draw = False
            array = random_array()
            draw(array, 0, key)
        if pykey[pygame.K_UP]:
            if elements < 500:
                elements += 1
            array = random_array()
            draw(array, 0, key)
        if pykey[pygame.K_DOWN]:
            if elements > 1:
                elements -= 1
            array = random_array()
            draw(array, 0, key)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    execute(reverse = True)