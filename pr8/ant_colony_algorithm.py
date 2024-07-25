import numpy as np
from multiprocessing.pool import Pool
import time

def calculate_distance(distance_matrix, path):
    """
    Вычисление длины пути по матрице расстояний и пути
    :param distance_matrix: матрица расстояний
    :param path: путь
    :return: длина пути
    """
    return sum([distance_matrix[path[i], path[(i + 1)]] for i in range(len(distance_matrix) - 1)]) + distance_matrix[path[-1], path[0]]

def ant_colony_TSP(distance_matrix, ant_num, iter_num, alpha, beta, p, start_point=0):
    """
    Муравьиный алгоритм для решения задачи коммивояжёра
    :param distance_matrix: матрица расстояний
    :param ant_num: количество муравьёв
    :param iter_num: количество итераций
    :param alpha: коэффициент значимости феромонов(тау)
    :param beta: коэффициент значимости расстояния
    :param p: коэффициент испарения феромонов(тау)
    :param start_point: стартовая точка муршрута
    :return: лучший найденный маршрут и его длина
    """
    cities_num = len(distance_matrix)
    probability_matrix_distance = (1 / np.array(distance_matrix)) * (np.ones((cities_num, cities_num)) - np.eye(cities_num, cities_num))
    ant_paths = np.zeros((ant_num, cities_num)).astype(int)
    tau_matrix = np.ones((cities_num, cities_num))
    generation_best_paths, generation_best_distances = [], []

    for i in range(iter_num):
        print("iter:", i)
        start = time.time()
        probability_matrix = (tau_matrix ** alpha) * (probability_matrix_distance) ** beta
        for j in range(ant_num):
            ant_paths[j, 0] = start_point
            for k in range(cities_num - 1):
                passed_cities = ant_paths[j, :k + 1]
                available_cities = list(set(range(cities_num)) - set(passed_cities))
                probabilities = probability_matrix[ant_paths[j, k], available_cities]
                probabilities = probabilities / probabilities.sum()
                next_city = np.random.choice(available_cities, size=1, p=probabilities)[0]
                ant_paths[j, k + 1] = next_city

        distances = np.array([calculate_distance(distance_matrix, i) for i in ant_paths])

        best_index = distances.argmin()
        best_path, best_distance = ant_paths[best_index, :].copy(), distances[best_index]
        generation_best_paths.append(best_path)
        generation_best_distances.append(best_distance)
        tau_matrix_change = np.zeros((cities_num, cities_num))
        for j in range(ant_num):
            for k in range(cities_num - 1):
                city_a, city_b = ant_paths[j, k], ant_paths[j, k + 1]
                tau_matrix_change[city_a, city_b] += 1 / distances[j]
            tau_matrix_change[ant_paths[j, cities_num - 1], ant_paths[j, 0]] += 1 / distances[j]

        tau_matrix = (1 - p) * tau_matrix + tau_matrix_change
        print("time of iter:", time.time() - start)
        print("best distance on this iter:", best_distance)
    best_generation = np.array(generation_best_distances).argmin()
    best_path = generation_best_paths[best_generation]
    best_distance = generation_best_distances[best_generation]
    return best_path, best_distance

def ant_process(j, ant_path, probability_matrix, cities_num, start_point):
    """
    Процесс расчёта пути муравья для многопоточной версии
    :param j: номер муравья
    :param ant_path: список для пути муравья
    :param probability_matrix: матрица вероятностей переходов
    :param cities_num: количество городов
    :param start_point: стартовый город
    :return: номер муравья и путь муравья
    """
    ant_path[0] = start_point
    for k in range(cities_num - 1):
        passed_cities = ant_path[:k + 1]
        available_cities = list(set(range(cities_num)) - set(passed_cities))
        probabilities = probability_matrix[ant_path[k], available_cities]
        probabilities = probabilities / probabilities.sum()
        next_city = np.random.choice(available_cities, size=1, p=probabilities)[0]
        ant_path[k + 1] = next_city
    return (j, ant_path)

def ant_colony_TSP_multiproccesing(distance_matrix, ant_num, iter_num, alpha, beta, p, start_point=0, q = 1, elite_num = 0):
    """
    Муравьиный алгоритм для решения задачи коммивояжёра(многопоточная версия)
    :param distance_matrix: матрица расстояний
    :param ant_num: количество муравьёв
    :param iter_num: количество итераций
    :param alpha: коэффициент значимости феромонов(тау)
    :param beta: коэффициент значимости расстояния
    :param p: коэффициент испарения феромонов(тау)
    :param start_point: стартовая точка муршрута
    :param q: коэффициент увеличения феромона
    :param elite_num: количество элитных муравьёв
    :return: лучший найденный маршрут и его длина
    """
    cities_num = len(distance_matrix)
    probability_matrix_distance = (1 / np.array(distance_matrix)) * (np.ones((cities_num, cities_num)) - np.eye(cities_num, cities_num))
    tau_matrix = np.ones((cities_num, cities_num)) * 1
    ant_paths = np.zeros((ant_num, cities_num)).astype(int)
    generation_best_paths, generation_best_distances = [], []
    print(tau_matrix.max())
    print(probability_matrix_distance.max())
    for i in range(iter_num):
        print("iter:", i)
        start = time.time()
        probability_matrix = (tau_matrix ** alpha) * (probability_matrix_distance ** beta)
        with Pool(4) as pool:
            items = [(j, ant_paths[j], probability_matrix, cities_num, start_point) for j in range(ant_num)]
            for result in pool.starmap(ant_process, items):
                ant_paths[result[0]] = result[1]

        distances = np.array([calculate_distance(distance_matrix, i) for i in ant_paths])

        best_index = distances.argmin()
        best_path, best_distance = ant_paths[best_index, :].copy(), distances[best_index].copy()
        generation_best_paths.append(best_path)
        generation_best_distances.append(best_distance)
        tau_matrix_change = np.zeros((cities_num, cities_num))
        for j in range(ant_num):
            for k in range(cities_num - 1):
                city_a, city_b = ant_paths[j, k], ant_paths[j, k + 1]
                tau_matrix_change[city_a, city_b] += q / distances[j]
            tau_matrix_change[ant_paths[j, cities_num - 1], ant_paths[j, 0]] += q / distances[j]
        for k in range(cities_num - 1):
            city_a, city_b = best_path[k], best_path[k + 1]
            tau_matrix_change[city_a, city_b] += q / best_distance * elite_num
        tau_matrix_change[best_path[cities_num - 1], best_path[0]] += q / best_distance * elite_num
        tau_matrix = (1 - p) * tau_matrix + tau_matrix_change
        tau_matrix = np.clip(tau_matrix, 1, 100)
        print("time of iter:", time.time() - start)
        print("best distance on this iter:", best_distance)
    best_generation = np.array(generation_best_distances).argmin()
    best_path = generation_best_paths[best_generation]
    best_distance = generation_best_distances[best_generation]
    return best_path, best_distance
