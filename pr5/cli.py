import argparse
import sys
from typing import *
import external_sort

def create_parser():
    """
    Создание парсера для CLI
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs='+', type=str)
    parser.add_argument('-sf', '--save_file', default=None, type=str)
    parser.add_argument('-r', '--reverse', nargs='?', default=False, const=True, type=bool)
    parser.add_argument('-k', '--key', nargs='?', default=None, type=Callable)
    parser.add_argument('-t', '--type',  default=None, type=str)
    parser.add_argument('-o', '--order', default=None, type=int)

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    if len(args.file) == 1:
        args.file = args.file[0]
    external_sort.fibonacci_sort(args.file, args.save_file, args.reverse, args.key, args.order, args.type)