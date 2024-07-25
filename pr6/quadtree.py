from pygame import Rect
import asteroid

class QuadTree:
    """
    Класс квадродерева/элемента квадродерева
    """
    def __init__(self, p_level:int, p_bounds: Rect):
        """
        :param p_level: порядок элемента дерева в общем дереве
        :param p_bounds: границы элемента
        """
        self.MAX_LEVEL = 6
        self.level = p_level
        self.objects = []
        self.bounds = p_bounds
        self.nodes = [None, None, None, None]

    def split(self):
        """
        Создание элементов дерева(поддеревьев)
        """
        subWidth = int(self.bounds.width / 2)
        subHeight = int(self.bounds.height / 2)
        x = self.bounds.x
        y = self.bounds.y

        self.nodes[0] = QuadTree(self.level + 1, Rect(x, y, subWidth, subHeight))
        self.nodes[1] = QuadTree(self.level + 1, Rect(x + subWidth, y, subWidth, subHeight))
        self.nodes[2] = QuadTree(self.level + 1, Rect(x, y + subHeight, subWidth, subHeight))
        self.nodes[3] = QuadTree(self.level + 1, Rect(x + subWidth, y + subHeight, subWidth, subHeight))

    def get_index(self, p_object: asteroid.Asteroid):
        """
        Возвращает индекс поддерева в которое попадает астероид при разделении текущего дерева
        :param p_object: астероид
        :return: индекс поддерева
        """
        index = -1
        verticalMidpoint = self.bounds.x + int(self.bounds.width / 2)
        horizontalMidpoint = self.bounds.y + int(self.bounds.height / 2)
        topQuadrant = (p_object.y < horizontalMidpoint and p_object.y + p_object.radius < horizontalMidpoint)
        bottomQuadrant = (p_object.y > horizontalMidpoint)

        if (p_object.x < verticalMidpoint and p_object.x + p_object.radius < verticalMidpoint):
            if topQuadrant:
                index = 0
            elif bottomQuadrant:
                index = 2
        elif p_object.x > verticalMidpoint:
            if topQuadrant:
                index = 1
            elif bottomQuadrant:
                index = 3

        return index

    def get_indexes(self, p_object):
        """
        Получить индексы поддеревьев куда попадает астероид
        :param p_object: астероид
        :return: индексы поддеревьев
        """
        indexes = []
        horizontalMidpoint = self.bounds.x + int(self.bounds.width / 2)
        verticalMidpoint = self.bounds.y + int(self.bounds.height / 2)
        topQuadrant = (p_object.y - p_object.radius < verticalMidpoint and p_object.y + p_object.radius > self.bounds.y)
        bottomQuadrant = (p_object.y + p_object.radius > verticalMidpoint and p_object.y - p_object.radius < self.bounds.y + self.bounds.height)

        if (p_object.x - p_object.radius < horizontalMidpoint and p_object.x + p_object.radius > self.bounds.x):
            if topQuadrant:
                indexes.append(0)
            if bottomQuadrant:
                indexes.append(2)
        if (p_object.x + p_object.radius > horizontalMidpoint and p_object.x - p_object.radius < self.bounds.x + self.bounds.width):
            if topQuadrant:
                indexes.append(1)
            if bottomQuadrant:
                indexes.append(3)
        return indexes

    def insert(self, p_object: asteroid.Asteroid):
        """
        "Положить" астероид в дерево
        :param p_object: астероид
        """
        if self.nodes[0] != None:
            indexes = self.get_indexes(p_object)
            for i in indexes:
                self.nodes[i].insert(p_object)
            return

        self.objects.append(p_object)

        if (len(self.objects) > 1 and self.level < self.MAX_LEVEL):
            self.split()
            while len(self.objects) != 0:
                indexes = self.get_indexes(self.objects[0])
                obj = self.objects.pop(0)
                for i in indexes:
                    self.nodes[i].insert(obj)


    def retrieve(self, p_object: asteroid.Asteroid, return_objects):
        """
        Получение списка астероидов находящихся в том же поддереве что и целевой астероид
        :param p_object: целевой астероид
        :param return_objects: список астероидов для возврата
        :return: список астероидов
        """
        indexes = self.get_indexes(p_object)
        if (indexes != [] and self.nodes[0] != None):
            for i in indexes:
                self.nodes[i].retrieve(p_object, return_objects)
        for i in self.objects:
            if i not in return_objects:
                return_objects.append(i)

        return return_objects

    def get_rects(self, rects_list):
        """
        Функция возвращяющая список rect-ов для отображения границ элементов квадродерева
        :param rects_list: список rect-ов
        :return: список rect-ов
        """
        rects_list.append(self.bounds)
        if self.nodes[0] != None:
            for i in range(0, 4):
                self.nodes[i].get_rects(rects_list)
        return rects_list

    def remove(self, p_object: asteroid.Asteroid):
        if p_object in self.objects:
            self.objects.remove(p_object)
        if self.nodes[0] != None:
            indexes = self.get_indexes(p_object)
            for i in indexes:
                self.nodes[i].remove(p_object)
            return