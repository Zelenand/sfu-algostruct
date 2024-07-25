import pygame
from math import pi
from random import randint
from random import uniform
from random import choice

import asteroid
import quadtree


def asteroid_field_start(height: int, width: int, asteroid_num: int, asteroid_min_rad: int, asteroid_max_rad: int,
                         asteroid_min_speed: float, asteroid_max_speed: float):
    """
    Функция генерирующая астероиды, создающая поле и запускающая основной цикл pygame
    :param height: высота поля
    :param width: ширина поля
    :param asteroid_num: количество астероидав
    :param asteroid_min_rad: минимальный радиус астероидов
    :param asteroid_max_rad: максимальный радиус астероидов
    :param asteroid_min_speed: минимальная скорость астероидов
    :param asteroid_max_speed: максимальная скорость астероидов
    """
    print(height, width, asteroid_num, asteroid_min_rad, asteroid_max_rad, asteroid_min_speed, asteroid_max_speed)
    pygame.init()
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    a_params = []
    for i in range(0, asteroid_num):
        radius = randint(asteroid_min_rad, asteroid_max_rad)
        x = randint(radius + 1, width - radius - 1)
        y = randint(radius + 1, height - radius - 1)
        x_speed = choice([-1, 1]) * uniform(asteroid_min_speed, asteroid_max_speed)
        y_speed = choice([-1, 1]) * uniform(asteroid_min_speed, asteroid_max_speed)
        a_params.append([x, y, radius, x_speed, y_speed])
    asteroids = [asteroid.Asteroid(i[0], i[1], i[2], i[3], i[4]) for i in a_params]
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        asteroid_field = quadtree.QuadTree(0, pygame.Rect(0, 0, width, height))
        for i in asteroids:
            asteroid_field.insert(i)
        asteroids_indexes = [i for i in range(0, len(asteroids))]
        for i in asteroids_indexes:
            return_objects = []
            collided_asteroids = asteroid_field.retrieve(asteroids[i], return_objects)

            if asteroids[i] in collided_asteroids:
                collided_asteroids.remove(asteroids[i])
            for j in collided_asteroids:
                k = asteroids.index(j)
                if k in asteroids_indexes:
                    asteroids_indexes.remove(k)
                v_1 = pygame.math.Vector2(asteroids[i].x, asteroids[i].y)
                v_2 = pygame.math.Vector2(asteroids[k].x, asteroids[k].y)
                if v_1.distance_to(v_2) < (asteroids[i].radius + asteroids[k].radius + 1):

                    v_speed_1 = pygame.Vector2(asteroids[i].x_speed, asteroids[i].y_speed)
                    v_speed_2 = pygame.Vector2(asteroids[k].x_speed, asteroids[k].y_speed)
                    mass_1 = pi * (asteroids[i].radius ** 2)
                    mass_2 = pi * (asteroids[k].radius ** 2)
                    v_new_speed_1 = (v_speed_1 - (v_1 - v_2) * (2 * mass_2 * ((v_speed_1 - v_speed_2) * (v_1 - v_2)) /
                                                                (mass_1 + mass_2) / (v_1 - v_2).length_squared()))
                    v_new_speed_2 = (v_speed_2 - (v_2 - v_1) * (2 * mass_1 * ((v_speed_2 - v_speed_1) * (v_2 - v_1)) /
                                                                (mass_1 + mass_2) / (v_2 - v_1).length_squared()))
                    asteroids[i].x_speed, asteroids[i].y_speed = v_new_speed_1
                    asteroids[k].x_speed, asteroids[k].y_speed = v_new_speed_2

                    while v_1.distance_to(v_2) < asteroids[i].radius + asteroids[k].radius + 1:
                        asteroids[i].move(width, height)
                        asteroids[k].move(width, height)
                        v_1 = pygame.math.Vector2(asteroids[i].x, asteroids[i].y)
                        v_2 = pygame.math.Vector2(asteroids[k].x, asteroids[k].y)

        for i in range(0, len(asteroids)):
            asteroids[i].move(width, height)


        window.fill((127, 127, 127))
        rects = asteroid_field.get_rects([])
        for i in rects:
            pygame.draw.rect(window, (225, 225, 0), i, 1)
        for i in asteroids:
            pygame.draw.circle(window, (255, 0, 0), (round(i.x), round(i.y)), i.radius)
        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    asteroid_field_start(600, 800, 2, 100, 100, 2, 2)