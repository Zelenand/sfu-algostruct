"""
Модуль плейлист
"""

import linked_list
import tinytag

class Composition:
    def __init__(self, path):
        """
        :param path: путь файла
        """
        self.__path = path
        metadata = tinytag.TinyTag.get(path)
        #self.image = metadata.get_image()
        self.name = metadata.title
        self.duration = metadata.duration

    @property
    def path(self):
        """
        Путь файла
        :return: Путь файла
        """
        return self.__path

class PlayList(linked_list.LinkedList):
    def __init__(self, name, composition: Composition = None):
        """
        :param name: название плейлиста
        :param composition: композиция
        """
        super().__init__(composition)
        self._name = name
        self._current_composition = None

    @property
    def name(self):
        """
        название плейлиста
        :return: название плейлиста
        """
        return self._name

    def play_all(self, index):
        """
        Установить текущую композицию
        :param index: индекс
        """
        self._current_composition = self[index]

    def next_track(self):
        """
        Сменить текущую композицию на следующую
        """
        self._current_composition = self.current_composition.next_item

    def previous_track(self):
        """
        Сменить текущую композицию на предыдущую
        """
        self._current_composition = self.current_composition.previous_item

    @property
    def current_composition(self):
        """
        Текущая композиция
        :return: Текущая композиция
        """
        return self._current_composition
