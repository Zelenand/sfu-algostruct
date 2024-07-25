"""
Модуль поиска подстроки/подстрок в строке алгоритмом Рабина-Карпа
"""
from typing import *
import json
import time

def new_hash(string: str, b: int):
    """
    Получение нового полиноминального хэша
    :param string: строка для которой ищем хэш
    :param b: основание системы символов(количество символов в алфавите исходной строки)
    :return: хэш
    """
    new_hash = 0
    length = len(string)
    for i in range(length):
        new_hash += ord(string[i]) * (b ** (length - i - 1))
    return new_hash

def next_hash(old_hash: int, b: int, length: int,  new_chr: chr, prev_chr: chr):
    """
    Получение следующего полиноминального хэша (скользящий хэш)
    :param old_hash: предыдущий хэш
    :param b: основание системы символов(количество символов в алфавите исходной строки)
    :param length: длина строки
    :param new_chr: новый символ
    :param prev_chr: предыдущий символ (из начала подстроки)
    :return: хэш
    """
    return ((old_hash - ord(prev_chr) * (b ** (length - 1))) * b + ord(new_chr))

def timer(function):
    """
    Декоратор для логирования времени выполнения функции
    :param function: функция
    :return: декорированная функция
    """
    def function_decorator(string: str, sub_string: Union[str, list[str], tuple[str]],
                           case_sensitivity: bool = False, method: str = 'first',
                           count: Optional[int] = None):
        start = time.perf_counter()
        result = function(string, sub_string, case_sensitivity,
                          method, count)
        final = time.perf_counter()
        with open("time.json", "w") as file:
            json.dump(final - start, file)
        return result
    return function_decorator

@timer
def search(string: str, sub_string: Union[str, list[str], tuple[str]],
           case_sensitivity: bool = False, method: str = 'first',
           count: Optional[int] = None) \
        -> Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Нахождение подстроки/подстрок в строке алгоритмом Рабина-Карпа
    :param string: исходная строка
    :param sub_string: одна или несколько подстрок, которые необходимо найти
    :param case_sensitivity: флаг чувствительности к регистру
    :param method: метод поиска
    :param count: количество совпадений, которые нужно найти
    :return: индексы найденных подстрок
    """
    if count < 1:
        raise ValueError("количество совпадений, не может быть меньше 1")
    if method != 'first' and method != 'last':
        raise ValueError("Некорректный метод поиска")

    # b - основание системы символов(количество символов в алфавите исходной строки)
    b = len(set([ord(i) for i in string]))

    if count == None:
        count = 1
    if isinstance(sub_string, str):
        sub_string = [sub_string]
    else:
        sub_string = list(sub_string)
    string_len = len(string)
    if len(sub_string) == 0:
        return None
    if not case_sensitivity:
        string = string.lower()
        for i in range(len(sub_string)):
            sub_string[i] = sub_string[i].lower()
    dict_indexes = dict()
    for i in sub_string:
        dict_indexes[i] = []
    if method != 'first':
        for i in range(len(sub_string)):
            sub_string[i] = sub_string[i][::-1]
        string = string[::-1]
    sub_string_len = [len(string) for string in sub_string]
    sub_string_hash = [new_hash(string, b) for string in sub_string]
    string_part_hash = [0] * len(sub_string)
    for i in range(string_len):
        if count == 0:
            break
        for j in range(len(sub_string)):
            if i + sub_string_len[j] > string_len:
                continue
            string_part = string[i: i + sub_string_len[j]]
            if i == 0:
                string_part_hash[j] = new_hash(string_part, b)
            else:
                string_part_hash[j] = next_hash(string_part_hash[j], b, sub_string_len[j], string_part[-1], string[i - 1])
            if string_part_hash[j] == sub_string_hash[j]:
                check = True
                for k in range(sub_string_len[j]):
                    if string_part[k] != sub_string[j][k]:
                        check = False
                        break
                if check:
                    if method == 'first':
                        dict_indexes[sub_string[j]].append(i)
                    else:
                        dict_indexes[sub_string[j][::-1]].append(string_len - i - len(sub_string[j]))
                    count -= 1
                    if count == 0:
                        break

    tuple_dict_indexes = dict()
    for i in dict_indexes:
        if len(dict_indexes[i]) == 0:
            tuple_dict_indexes[i] = None
        else:
            tuple_dict_indexes[i] = tuple(dict_indexes[i])
    if list(tuple_dict_indexes.values()).count(None) == len(tuple_dict_indexes):
        return None
    if len(tuple_dict_indexes) == 1:
        if method == 'first':
            return tuple_dict_indexes[sub_string[0]]
        return tuple_dict_indexes[sub_string[0][::-1]]
    return tuple_dict_indexes