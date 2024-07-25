from typing import *
from multiprocessing.pool import Pool


def get_n_gramms(strings, n):
    """
    Получить н-граммы символов из строк
    :param strings: список строк
    :param n: количество символов n в n-грамме
    :return: список н-грамм
    """
    n_gramms = []
    for i in range(0, len(strings)):
        if n >= len(strings[i]):
            n_gramms.append((strings[i], i))
        else:
            for j in range(0, len(strings[i]) - n + 1):
                n_gramms.append((strings[i][j: j + n], i))
    return n_gramms

def n_gramm_process(n_gramm_num, string, n_gramm, sub_string_num, count):
    """
    Процесс поиска н-граммы в строке
    :param n_gramm_num: номер н-граммы
    :param string: строка
    :param n_gramm: н-грамма
    :param sub_string_num: номер подстроки н-граммы
    :param count: количество совпадений, которые нужно найти
    :return: номер н-граммы, кортеж индексов совпадений, номер подстроки
    """
    n_gramm_len = len(n_gramm)
    occurances = []
    for i in range(0, len(string) - n_gramm_len + 1):
        if string[i: i + n_gramm_len] == n_gramm:
            occurances.append(i)
            count -= 1
            if count == 0:
                break
    return n_gramm_num, tuple(occurances), sub_string_num

def n_gramm_process_strict_index(n_gramm_num, string, n_gramm, sub_string_num, sub_string, count):
    """
    Процесс поиска н-граммы в строке
    :param n_gramm_num: номер н-граммы
    :param string: строка
    :param n_gramm: н-грамма
    :param sub_string_num: номер подстроки н-граммы
    :param count: количество совпадений, которые нужно найти
    :return: номер н-граммы, кортеж индексов совпадений, номер подстроки
    """
    n_gramm_len = len(n_gramm)
    occurances = []
    n_gramm_indent = sub_string.find(n_gramm)
    for i in range(0, len(string) - n_gramm_len + 1):
        if string[i: i + n_gramm_len] == n_gramm:
            word_index, _ = find_word_indexes(i, string)
            if word_index + n_gramm_indent == i:
                occurances.append(i)
                count -= 1
                if count == 0:
                    break
    return n_gramm_num, tuple(occurances), sub_string_num

def find_word_indexes(index, string):
    """
    Найти индексы первой и последней буквы слова расположенного на индексе символа в строке
    :param index: индекс символа слова
    :param string: строка
    :return: индексы первой и последней буквы слова расположенного на индексе символа в строке
    """
    left_word_index = 0 if string[:index].count(' ') == 0 else string[:index].rindex(' ') + 1
    right_word_index = len(string) if string[index:].count(' ') == 0 else index + string[index:].index(' ') - 1
    return (left_word_index, right_word_index)

def search(string: str, sub_strings: Union[str, list[str], tuple[str]], n: int = 3,
           case_sensitivity: bool = False, method: str = 'first', count: Optional[int] = 1, strict_index: bool = False) \
        -> Union[list[list[tuple[int, ...], ...], ...], int]:
    """
    Неточный поиск подстрок в строке методом N-грамм
    :param string: исходная строка
    :param sub_strings: одна или несколько подстрок, которые необходимо найти
    :param n: количество символов в n-граммах
    :param case_sensitivity: флаг чувствительности к регистру
    :param method: метод поиска
    :param count: количество совпадений, которые нужно найти
    :return: индексы найденных подстрок или -1 если подстроки не найдены
    """
    if count < 1:
        raise ValueError("количество совпадений, не может быть меньше 1")
    if method != 'first' and method != 'last':
        raise ValueError("Некорректный метод поиска")
    if count == None:
        count = 1
    if isinstance(sub_strings, str):
        sub_strings = [sub_strings]
    else:
        sub_strings = list(sub_strings)
    if len(sub_strings) == 0:
        return -1
    if not case_sensitivity:
        string = string.lower()
        for i in range(len(sub_strings)):
            sub_strings[i] = sub_strings[i].lower()
    if method != 'first':
        for i in range(len(sub_strings)):
            sub_strings[i] = sub_strings[i][::-1]
        string = string[::-1]
    occurrences = {}
    n_gramms = get_n_gramms(sub_strings, n)

    if strict_index:
        with Pool(5) as pool:
            items = [(j, string, n_gramms[j][0], n_gramms[j][1], sub_strings[n_gramms[j][1]], count) for j in range(len(n_gramms))]
            for result in pool.starmap(n_gramm_process_strict_index, items):
                occurrences[result[0]] = (result[1], result[2])
    else:
        with Pool(5) as pool:
            items = [(j, string, n_gramms[j][0], n_gramms[j][1], count) for j in range(len(n_gramms))]
            for result in pool.starmap(n_gramm_process, items):
                occurrences[result[0]] = (result[1], result[2])

    if len(occurrences) == 0:
        return -1
    if method != "first":
        string = string[::-1]

    fine_occurences = []
    for i in range(0, len(sub_strings)):
        fine_occurences.append([])
    for j in occurrences.values():
        fine_occurences[j[1]] += list(j[0])

    for i in range(0, len(sub_strings)):
        for j in range(0, len(fine_occurences[i])):
            if method == "first":
                fine_occurences[i][j] = find_word_indexes(fine_occurences[i][j], string)
            else:
                fine_occurences[i][j] = len(string) - fine_occurences[i][j] - 1
                fine_occurences[i][j] = find_word_indexes(fine_occurences[i][j], string)
        fine_occurences = [list(set(i)) for i in fine_occurences]
        fine_occurences[i].sort(key=lambda x: x[0], reverse=(method == "last"))
        fine_occurences[i] = fine_occurences[i][0: count]

    return fine_occurences