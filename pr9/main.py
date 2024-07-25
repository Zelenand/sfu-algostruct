import argparse
import sys
import colorama
import search

def string_paint(string: str, occurences_indexes: list) -> str:
    """
    Раскраски подстрок в строке
    :param string: строка
    :param occurences_indexes: индексы подстрок
    :return: раскрашенная строка
    """
    colors = [
        colorama.Fore.RED,
        colorama.Fore.GREEN,
        colorama.Fore.BLUE,
        colorama.Fore.YELLOW,
        colorama.Fore.CYAN,
        colorama.Fore.MAGENTA
    ]
    colored_string = ""
    for i in range(len(string)):
        check = False
        index = 0
        for k in range(len(occurences_indexes)):
            for indexes in occurences_indexes[k]:
                if indexes[0] <= i <= indexes[1]:
                    check = True
                    index = k
                    break
            if check:
                break
        if check:
            colored_string += str(colors[index % len(colors)]) + string[i] + colorama.Fore.RESET
        else:
            colored_string += string[i]
    return colored_string


if __name__ == '__main__':
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', type=str)
    parser.add_argument('-f', '--file', default=None, type=str)
    parser.add_argument('-rf', '--result_file', default=None, type=str)
    parser.add_argument('-ss', '--sub_string', nargs='+', type=str)
    parser.add_argument('-n', '--n_gramms', nargs='?', default=3, type=int)
    parser.add_argument('-cs', '--case_sensitivity', nargs='?', default=False, const=True, type=bool)
    parser.add_argument('-si', '--strict_index', nargs='?', default=False, const=True, type=bool)
    parser.add_argument('-m', '--method', choices=['first', 'last'], default='first',
                        type=str)
    parser.add_argument('-k', '--count', nargs='?', default=1, type=int)
    args = parser.parse_args(sys.argv[1:])

    if args.file:
        with open(args.file, 'r') as f:
            args.string = f.read()
    results = search.search(args.string, args.sub_string, args.n_gramms, args.case_sensitivity,
                            args.method, args.count, args.strict_index)
    if results == -1:
        print("Подстроки не найдены")
    else:
        color_string = string_paint(args.string, results)

        for i in range(0, len(args.sub_string)):
            print(args.sub_string[i], len(results[i]), [(results[i][j], args.string[results[i][j][0]:results[i][j][1] + 1]) for
                                                        j in range(0, len(results[i]))])

        if args.result_file:
            with open(args.result_file, 'w') as f:
                for i in range(0, len(args.sub_string)):
                    f.write(args.sub_string[i])
                    for j in range(0, len(results[i])):
                        left_index = results[i][j][0]
                        right_index = results[i][j][1]
                        f.write(str(left_index) + "-" + str(right_index) + ": " + args.string[left_index:right_index + 1])

        if len(color_string) > 159 * 10:
            color_string = color_string[:159 * 10] + "..."
        print(color_string)