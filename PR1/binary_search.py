import dynamic_array

def search(data: dynamic_array.Array, obj: object):
    """
    Бинарный поиск в массиве
    :param data: Массив для поиска
    :param obj: Искомый элемент
    :return: Индекс найденного элемента или None
    """
    if len(data) > 0:
        low = 0
        high = len(data) - 1
        while low <= high:
            middle = (low + high) // 2
            if data[middle] == obj:
                while middle > 0 and data[middle - 1] == obj:
                    middle = middle - 1
                return middle
            elif data[middle] > obj:
                high = middle - 1
            else:
                low = middle + 1
    return None

print(search([1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 5, 6], '2'))
