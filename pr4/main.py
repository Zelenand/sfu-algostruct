import argparse
import sys
from typing import *
import vizualization
import my_sort

def create_parser():
    """
    Создание парсера для CLI
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', nargs='+', type=str)
    parser.add_argument('-f', '--file', default=None, type=str)
    parser.add_argument('-sf', '--save_file', default=None, type=str)
    parser.add_argument('-r', '--reverse', nargs='?', default=False, const=True, type=bool)
    parser.add_argument('-k', '--key', nargs='?', default=None, type=Callable)
    parser.add_argument('-c', '--cmp', nargs='?', default=None, type=Callable)

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.file:
        with open(args.file, 'r') as f:
            args.list = f.read().split(" ")
    results = my_sort.my_sort(args.list, args.reverse, args.key, args.cmp)
    print(results)
    if args.save_file:
        with open(args.save_file, 'w') as f:
           f.write(" ".join(results))
