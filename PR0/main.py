"""
Вариант 2 - Треугольник Серпинского
Выполнил: Самарин Никита КИ21-17/2Б
"""

# turtle - нужен для отображения фрактала
# random - нужен для генерации случайных цветов
import turtle
import random


def new_gen(gen_1, chr_1, chr_2, rule_1, rule_2):
    """
    Получение строки следующего поколения
    :param gen: строка поколения
    :param chr_1: конфигурация L-системы
    :param chr_2: конфигурация L-системы
    :param rule_1: конфигурация L-системы
    :param rule_2: конфигурация L-системы
    :return:
    """
    return ''.join([rule_1 if chr == chr_1 else
                    rule_2 if chr == chr_2 else chr for chr in gen_1])

def get_final(gen_1, gen_num_1, chr_1, chr_2, rule_1, rule_2):
    """
    Получение строки финального поколения
    :param gen: строка поколения
    :param gen_num: количество поколений
    :param chr_1: конфигурация L-системы
    :param chr_2: конфигурация L-системы
    :param rule_1: конфигурация L-системы
    :param rule_2: конфигурация L-системы
    :return: строка финального поколения
    """
    i = 0
    while i < gen_num_1:
        gen_1 = new_gen(gen_1, chr_1, chr_2, rule_1, rule_2)
        i+=1
    return gen_1


if __name__ == '__main__':
    gen_num = 0
    while gen_num == 0:
        try:
            gen_num = int(
                input("Введите количество поколений"
                      "(больше 7 не рекомендовано):\n"))
        except ValueError:
            print("Некорректный ввод")

    # Конфигурация L-системы
    config = {"CHR1": 'A',
        "CHR2": 'B',
        "RULE1": 'A-B+A+B-A',
        "RULE2": 'BB',
        "STEP": 8,
        "ANGLE": 120
    }
    gen = 'A-B-B'

    # Получение строки финального поколения
    gen = get_final(gen, gen_num, config["CHR1"], config["CHR2"], config["RULE1"], config["RULE2"])
    # Настройки окна черепашки
    WIDTH, HEIGHT = 1280, 900
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.screensize(3 * WIDTH, 3 * HEIGHT)
    screen.bgcolor("white")
    screen.delay(0)

    # Настройки черепашки
    myturtle = turtle.Turtle()
    myturtle.hideturtle()
    myturtle.pensize(2)
    myturtle.speed(0)
    turtle.tracer(False)
    myturtle.color("white")
    myturtle.setpos(-WIDTH // 3, - HEIGHT // 2)
    turtle.colormode(255)
    base_color = (34, 139, 34)
    myturtle.color(base_color)

    # Цикл рисования черепашки
    for char in gen:
        if char in (config["CHR1"], config["CHR2"]):
            color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            myturtle.color(color)
            myturtle.forward(config["STEP"])
        elif char == '+':
            myturtle.right(config["ANGLE"])
        elif char == '-':
            myturtle.left(config["ANGLE"])

    # Выход из программы
    screen.exitonclick()
