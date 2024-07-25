import pathlib
from typing import *
import os
import csv

PathType = Union[str, pathlib.Path]


def a_next(prev_a):
    """
    Получение следующего уровня распределения
    :param prev_a: предыдущее распределение
    :return: следующий уровень распределения
    """
    a = [0] * len(prev_a)
    for i in range(len(prev_a) - 1):
        a[i] = prev_a[0] + prev_a[i + 1]
    a[len(a) - 1] = prev_a[0]
    return a


def first_raspr(src: PathType, order: int, file_names, cmp):
    """
    Первичное фибоначчиевое распределение
    :param src: исходный файл
    :param order: количество файлов
    :param file_names: имена файлов
    :param cmp: лямбда функция сравнения
    """

    flag = True
    a = [1] * order
    d = a.copy()
    last_lines = [0] * order
    with open(src, "r") as source:
        line = source.readline().replace("\n", "")
        if not line:
            return -1, -1
        for i in range(order):
            with open(file_names[i], "a") as file:
                file.write(line + "\n")
                last_lines[i] = line
                line = source.readline().replace("\n", "")
                if not line:
                    d[i] -= 1
                    return 1, d
                while(cmp(last_lines[i], line)):
                    file.write(line + "\n")
                    last_lines[i] = line
                    line = source.readline().replace("\n", "")
                    if not line:
                        d[i] -= 1
                        return 1, d
                d[i] -= 1
                level = 1
        if not line:
            flag = False
        while flag:
            d = a.copy()
            a = a_next(a)
            d = [(a[i] - d[i]) for i in range(order)]
            level += 1
            i = 0
            while max(d) > 0:
                with open(file_names[i], "a") as file:
                    if cmp(last_lines[i], line):
                        d[i] += 1
                    file.write(line + "\n")
                    last_lines[i] = line
                    line = source.readline().replace("\n", "")
                    if not line:
                        d[i] -= 1
                        flag = False
                        break
                    while cmp(last_lines[i], line):
                        file.write(line + "\n")
                        last_lines[i] = line
                        line = source.readline().replace("\n", "")
                        if not line:
                            d[i] -= 1
                            flag = False
                            break
                    if flag:
                        d[i] -= 1
                        if (i != order - 1) and d[i + 1] > d[i]:
                            i += 1
                        else:
                            i = d.index(d[i])
                    else: break
    return level, d


def first_raspr_csv(src: PathType, order: int, file_names, cmp, csv_column):
    """
    Первичное фибоначчиевое распределение csv
    :param src: исходный файл
    :param order: количество файлов
    :param file_names: имена файлов
    :param cmp: лямбда функция сравнения
    """

    flag = True
    a = [1] * order
    d = a.copy()
    last_lines = [0] * order
    with open(src, "r") as source:
        source_reader = csv.reader(source, delimiter=",")
        head = next(source_reader, False)
        if not head:
            return -1, -1, -1
        for i in range(0, len(head)):
            if head[i] == csv_column:
                csv_column_index = i
                break
        row = next(source_reader, False)
        if row:
            try:
                cmp(row[csv_column_index], row[csv_column_index])
            except ValueError:
                raise ValueError("Тип неккоректен относительно типа столбца сравнения")
        if not row:
            return -1, -1, -1
        line = row[csv_column_index]
        for i in range(order):
            with open(file_names[i], "a") as file:
                file_writer = csv.writer(file, delimiter = ",", lineterminator="\r")
                file_writer.writerow(head)
                file_writer.writerow(row)
                last_lines[i] = line
                row = next(source_reader, False)
                if not row:
                    d[i] -= 1
                    return 1, d, csv_column_index
                line = row[csv_column_index]
                while(cmp(last_lines[i], line)):
                    file_writer.writerow(row)
                    last_lines[i] = line
                    row = next(source_reader, False)
                    if not row:
                        d[i] -= 1
                        return 1, d, csv_column_index
                    line = row[csv_column_index]
                d[i] -= 1
                level = 1

        if not row:
            flag = False
        while flag:
            d = a.copy()
            a = a_next(a)
            d = [(a[i] - d[i]) for i in range(order)]
            level += 1
            i = 0
            while max(d) > 0:
                with open(file_names[i], "a") as file:
                    if cmp(last_lines[i], line):
                        d[i] += 1
                    file_writer = csv.writer(file, delimiter = ",", lineterminator="\r")
                    file_writer.writerow(row)
                    last_lines[i] = line
                    row = next(source_reader, False)
                    if not row:
                        d[i] -= 1
                        flag = False
                        break
                    line = row[csv_column_index]
                    while cmp(last_lines[i], line):
                        file_writer.writerow(row)
                        last_lines[i] = line
                        row = next(source_reader, False)
                        if not row:
                            d[i] -= 1
                            flag = False
                            break
                        line = row[csv_column_index]
                    if flag:
                        d[i] -= 1
                        if (i != order - 1) and d[i + 1] > d[i]:
                            i += 1
                        else:
                            i = d.index(d[i])
                    else: break
    return level, d, csv_column_index


def fibonacci_sort(src: Union[PathType, list[PathType]], output: PathType = None, reverse: bool = False,
                   key_b: Optional[Callable] = lambda a: a, key_csv: str = "", order: int = 3, type_data: str = "i") -> None:
    """
    Многофазная фибоначчиевая сортировка
    :param src: исходные файлы
    :param output: выходные файлы
    :param reverse: обратная сортировка
    :param key_b: функция, вычисляющая значение, на основе которого будет производится сортировка.
    :param key_csv: столбец для csv по которому производится сортировка
    :param order: количество файлов многофазной сортировки
    :param type_data: тип сортируемых данных
    """
    if isinstance(src, list):
        if not output:
            for i in src:
                fibonacci_sort(i, i, reverse, key_b, key_csv, order, type_data)
            return
        else:
            if src[0][len(src[0]) - 3:] == "txt":
                open("new_source.txt", "w").close()
                with open("new_source.txt", "a") as new_src:
                    for i in src:
                        with open(i, "r") as file:
                            line = file.readline()
                            while line:
                                new_src.write(line)
                                line = file.readline()
                src = "new_source.txt"
            elif src[0][len(src) - 3:] == "csv":
                open("new_source.csv", "w").close()
                with open("new_source.csv", "a") as new_src:
                    file_writer = csv.writer(new_src)
                    for i in src:
                        with open(i, "r") as file:
                            file_reader = csv.reader(file, delimiter = ",")
                            for j in file_reader:
                                file_writer.writerow(j)
                src = "new_source.txt"
            else:
                raise ValueError("Некорректный формат файлов")
    if src[len(src) - 3:] == "csv":
        if output and output[len(output) - 3:] != "csv":
            raise ValueError("Некорректный формат файлов")
        fibonacci_sort_csv(src, output, reverse, key_b, key_csv, order, type_data)
        return
    if output and output[len(output) - 3:] != "txt":
        raise ValueError("Некорректный формат файлов")
    if not key_b:
        key_b = lambda a: a
    if order < 3:
        raise ValueError("количество лент должно быть не меньше 3")
    if type_data == "i":
        key = lambda a: key_b(int(a))
    elif type_data == "f":
        key = lambda a: key_b(float(a))
    elif type_data == "s":
        key = lambda a: key_b(a)
    else:
        raise ValueError("Некорректный тип")
    file_names = []
    for i in range(1, order + 1):
        file_name = "posl" + str(i) + ".txt"
        file_names.append(file_name)
        open(file_name, "w", encoding="utf-8").close()
    cmp = lambda a, b: key(a) <= key(b)
    if reverse:
        cmp = lambda a, b: key(a) >= key(b)
    level, d = first_raspr(src, order - 1, file_names[:len(file_names) - 1], cmp)
    if level != -1 and d != -1:
        first = lambda a: min(a)
        cmp = lambda a, b: a <= b
        if reverse:
            cmp = lambda a, b: a >= b
            first = lambda a: max(a)
        d.append(0)
        output_file_index = order
        while level != 0:
            output_file_index = (output_file_index - 1)
            if output_file_index < 0:
                output_file_index = order - 1
            input_files_indexes_1 = [i for i in range(0, order)]
            input_files_indexes_1.remove(output_file_index)
            flag_2 = True
            while flag_2:
                if min([d[i] for i in input_files_indexes_1]) != 0:
                    for i in input_files_indexes_1:
                        d[i] -= 1
                    d[output_file_index] += 1
                    continue
                input_files_indexes_2 = []
                for i in input_files_indexes_1:
                    if d[i] == 0:
                        input_files_indexes_2.append(i)
                    else:
                        d[i] -= 1
                while len(input_files_indexes_2) != 0:
                    elements = []
                    for i in input_files_indexes_2.copy():
                        with open(file_names[i], "r") as f:
                            line = f.readline()
                            if (line and line != "" and line != "\n"):
                                elements.append(key(line.replace("\n", "")))
                            else:
                                input_files_indexes_2.remove(i)
                    if len(elements) == 0:
                        break
                    elem = first(elements)
                    elem_file_index = input_files_indexes_2[elements.index(elem)]
                    with open(file_names[output_file_index], "a") as output_file:
                        output_file.write(str(elem) + "\n")
                    with open(file_names[elem_file_index], "r") as f:
                        f.readline()
                        with open('temp1.txt', "w") as tempf:
                            line = f.readline()
                            while line:
                                tempf.write(line)
                                line = f.readline()
                    os.replace('temp1.txt', file_names[elem_file_index])
                    with open(file_names[elem_file_index], "r") as f:
                        line = f.readline()
                        if not line:
                            input_files_indexes_2.remove(elem_file_index)
                        elif not cmp(elem, key(line.replace("\n", ""))):
                            input_files_indexes_2.remove(elem_file_index)
                with open(file_names[output_file_index - 1], "r") as f:
                    if d[output_file_index - 1] == 0 and not f.readline():
                        flag_2 = False
                        level -= 1
    else:
        delete_files(file_names, src)
        print("Sort complete")
        return
    if not output:
        output = src
    with open(output, "w") as result_file:
        with open(file_names[output_file_index], "r") as output_file:
            while True:
                line = output_file.readline()
                if line:
                    result_file.write(line)
                else:
                    break
    delete_files(file_names, src)
    print("Sort complete")


def fibonacci_sort_csv(src: Union[PathType, list[PathType]], output: PathType = None, reverse: bool = False,
                   key_b: Optional[Callable] = lambda a: a, key_csv: str = "",  order: int = 3, type_data: str = "i") -> None:
    """
    Многофазная фибоначчиевая сортировка csv-файлов
    :param src: исходные файлы
    :param output: выходные файлы
    :param reverse: обратная сортировка
    :param key_b: функция, вычисляющая значение, на основе которого будет производится сортировка.
    :param key_csv: столбец для csv по которому производится сортировка
    :param order: количество файлов многофазной сортировки
    :param type_data: тип сортируемых данных
    """
    if not key_b:
        key_b = lambda a: a
    if order < 3:
        raise ValueError("количество лент должно быть не меньше 3")
    if type_data == "i":
        key = lambda a: key_b(int(a))
    elif type_data == "f":
        key = lambda a: key_b(float(a))
    elif type_data == "s":
        key = lambda a: key_b(a)
    else:
        raise ValueError("Некорректный тип")
    file_names = []
    for i in range(1, order + 1):
        file_name = "posl" + str(i) + ".csv"
        file_names.append(file_name)
        open(file_name, "w", encoding="utf-8").close()
    cmp = lambda a, b: key(a) <= key(b)
    if reverse:
        cmp = lambda a, b: key(a) >= key(b)
    if not key_csv:
        raise ValueError("Не указан key_csv")
    csv_column = key_csv
    level, d, csv_column_index = first_raspr_csv(src, order - 1, file_names[:len(file_names) - 1], cmp, csv_column)
    if level != -1 and d != -1:
        with open(file_names[-1], "w") as f:
            f_writer = csv.writer(f, delimiter = ",", lineterminator="\r")
            with open(file_names[0], "r") as file:
                file_reader = csv.reader(file, delimiter = ",")
                row = next(file_reader)
                f_writer.writerow(row)
        cmp = lambda a, b: a <= b
        if reverse:
            cmp = lambda a, b: a >= b
        d.append(0)
        first = lambda a: min(a)
        if reverse:
            first = lambda a: max(a)
        output_file_index = order
        while level != 0:
            output_file_index = (output_file_index - 1)
            if output_file_index < 0:
                output_file_index = order - 1
            input_files_indexes_1 = [i for i in range(0, order)]
            input_files_indexes_1.remove(output_file_index)
            flag_2 = True
            while flag_2:
                if min([d[i] for i in input_files_indexes_1]) != 0:
                    for i in input_files_indexes_1:
                        d[i] -= 1
                    d[output_file_index] += 1
                    continue
                input_files_indexes_2 = []
                for i in input_files_indexes_1:
                    if d[i] == 0:
                        input_files_indexes_2.append(i)
                    else:
                        d[i] -= 1
                while len(input_files_indexes_2) != 0:
                    elements = []
                    for i in input_files_indexes_2:
                        with open(file_names[i], "r") as f:
                            f_reader = csv.reader(f, delimiter = ",")
                            next(f_reader, False)
                            row = next(f_reader, False)
                            if row:
                                line = row[csv_column_index]
                            if (row and line != ""):
                                elements.append(key(line))
                            else:
                                input_files_indexes_2.remove(i)
                    if len(elements) == 0:
                        break
                    elem = first(elements)
                    elem_file_index = input_files_indexes_2[elements.index(elem)]
                    with open(file_names[output_file_index], "a") as output_file:
                        output_file_writer = csv.writer(output_file, delimiter = ",", lineterminator="\r")
                        with open(file_names[elem_file_index], "r") as f:
                            f_reader = csv.reader(f, delimiter = ",")
                            next(f_reader)
                            row = next(f_reader)
                            output_file_writer.writerow(row)
                    with open(file_names[elem_file_index], "r") as f:
                        f_reader = csv.reader(f, delimiter = ",")
                        with open('temp1.csv', "w") as tempf:
                            tempf_writer = csv.writer(tempf, delimiter = ",", lineterminator="\r")
                            row = next(f_reader, False)
                            tempf_writer.writerow(row)
                            next(f_reader)
                            row = next(f_reader, False)
                            while row:
                                tempf_writer.writerow(row)
                                row = next(f_reader, False)
                    with open('temp1.csv', "r") as f:
                        f_reader = csv.reader(f, delimiter = ",")
                        row = next(f_reader, False)
                        while row:
                            row = next(f_reader, False)
                    os.replace('temp1.csv', file_names[elem_file_index])
                    with open(file_names[elem_file_index], "r") as f:
                        f_reader = csv.reader(f, delimiter = ",")
                        row = next(f_reader, False)
                        while row:
                            row = next(f_reader, False)
                    with open(file_names[elem_file_index], "r") as f:
                        f_reader = csv.reader(f, delimiter = ",")
                        next(f_reader, False)
                        row = next(f_reader, False)
                        if row:
                            line = row[csv_column_index]
                        if not row:
                            input_files_indexes_2.remove(elem_file_index)
                        elif not cmp(elem, key(line)):
                            input_files_indexes_2.remove(elem_file_index)
                with open(file_names[output_file_index - 1], "r") as f:
                    f_reader = csv.reader(f, delimiter = ",")
                    next(f_reader, False)
                    if d[output_file_index - 1] == 0 and not next(f_reader, False):
                        flag_2 = False
                        level -= 1
    else:
        delete_files(file_names, src)
        print("Sort complete")
        return

    if not output:
        output = src
    with open(output, "w") as result_file:
        result_file_writer = csv.writer(result_file, delimiter = ",", lineterminator="\r")
        with open(file_names[output_file_index], "r") as output_file:
            output_file_reader = csv.reader(output_file, delimiter = ",")
            while True:
                row = next(output_file_reader, False)
                if row:
                    result_file_writer.writerow(row)
                else:
                    break
    delete_files(file_names, src)
    print("Sort complete")


def delete_files(file_list, src):
    for i in file_list:
        open(i, "r").close()
        os.unlink(i)
    if src.count("new_source") == 1:
        open(src, "r").close()
        os.unlink(src)

if __name__ == "__main__":
    fibonacci_sort("test.csv", "sorted.csv", key_csv="sort")