import argparse
import sys
import colorama
import search

def string_paint(string: str, sub_strings: list[str], indexes_dict: dict) -> str:
    """
    Красит подстроки в строке по индексам
    :param string: исходная строка
    :param sub_strings: подстроки
    :param sub_strings_entries: индексы начала подстрок
    :return: покрашенная строка
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
        for k in range(len(indexes_dict)):
            each_sub_string = sub_strings[k]
            if indexes_dict[each_sub_string] != None:
                for j in indexes_dict[each_sub_string]:
                    if j <= i < j + len(each_sub_string):
                        check = True
                        index = k
        if check:
            colored_string += str(colors[index % len(colors)]) + string[i] + colorama.Fore.RESET
        else:
            colored_string += string[i]
    return colored_string


def create_parser():
    """
    Создание парсера для CLI
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', default='', type=str)
    parser.add_argument('-f', '--file', default=None, type=str)
    parser.add_argument('-ss', '--sub_string', nargs='+', type=str)
    parser.add_argument('-cs', '--case_sensitivity', nargs='?', default=False, const=True, type=bool)
    parser.add_argument('-m', '--method', choices=['first', 'last'], default='first',
                        type=str)
    parser.add_argument('-k', '--count', nargs='?', default=1, type=int)

    return parser


if __name__ == '__main__':
    colorama.init()
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.file:
        with open(args.file, 'r') as f:
            args.string = f.read()
    results = search.search(args.string, args.sub_string, args.case_sensitivity,
                            args.method,args.count)
    if isinstance(results, tuple):
        results = {args.sub_string[0]: results}
    if results != None:
        color_string = string_paint(args.string, args.sub_string, results)
    else:
        color_string = args.string
    print(results)
    if len(color_string) > 120 * 10:
        color_string = color_string[:120 * 10] + "..."
    print(color_string)
