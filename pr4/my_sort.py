from typing import *


def quick_sort(arr, fst, lst, key, cmp) -> None:
    """
    Quicksort
    :param arr: список
    :param fst: левая граница
    :param lst: правая граница
    :param key: функция для нахождения значения элемента
    :param cmp: функция для сравнивания элементов
    """
    if fst >= lst: return

    i, j = fst, lst
    pivot = arr[(lst + fst) // 2]

    while i <= j:
        while cmp(key(arr[i]), key(pivot)):
            i += 1
        while cmp(key(pivot), key(arr[j])):
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i, j = i + 1, j - 1
    quick_sort(arr, fst, j, key, cmp)
    quick_sort(arr, i, lst, key, cmp)


def my_sort(array: list, reverse: bool = False, key: Optional[Callable] = None, cmp: Optional[Callable] = None) -> list:
    """
    получение отсортированного списка
    :param array: список
    :param reverse: флаг обратной сортировки
    :param key: функция для нахождения значения элемента
    :param cmp: функция для сравнивания элементов
    :return: отсортированный список
    """
    if key == None:
        key = lambda a: a
    if cmp == None:
        cmp = lambda a, b: a < b
    if reverse == True:
        cmp_2 = lambda a, b: cmp(b, a)
    else:
        cmp_2 = cmp
    quick_sort(array, 0, len(array) - 1, key, cmp_2)
    return array
