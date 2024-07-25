# cython: language_level=3
# distutils: language = c
"""Модуль динамического массива на cython
Самарин Никита КИ21-17/2Б"""
import re

from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from cpython.float cimport PyFloat_FromDouble, PyFloat_AsDouble
from cpython.long cimport PyLong_FromLong, PyLong_AsLong
import array

cdef class Array:
    """Класс динамического массива"""
    cdef int length
    cdef char* data
    cdef int typecode
    cdef int elem_size
    cdef int capacity

    def __cinit__(self, str typecode_init, object list_init = None):
        """Инициализация динамического массива
        :param typecode_init: тип элементов
        :param list_init: инициализационный список
        """
        if not (isinstance(list_init, list)):
            raise ValueError("Неккоректный инициализационный список")
        if list_init == None:
            list_init = []
        self.length = len(list_init)
        if typecode_init == 'd':
            self.typecode = 1
            self.elem_size = sizeof(double)
        elif typecode_init == 'i':
            self.typecode = 2
            self.elem_size = sizeof(long)
        else:
            raise ValueError("Неккоректный тип")
        self.capacity = self.elem_size * 2 + self.length * self.elem_size * 2
        self.data = <char*> PyMem_Malloc(self.capacity)
        cdef int i = 0
        for i in range(0, self.length):
            self.__setitem__(i, list_init[i])

    def __dealloc__(self):
        """Очистка памяти"""
        PyMem_Free(self.data)

    def size_up(self):
        """Увеличение размера массива"""
        self.length = self.length + 1
        if self.length * self.elem_size > self.capacity:
            self.capacity = self.capacity * 2
            self.data = <char*> PyMem_Realloc(self.data, self.capacity)

    def size_down(self):
        """Уменьшение размера массива"""
        self.length = self.length - 1
        if self.length * self.elem_size < 0.25 * self.capacity:
            self.capacity = self.capacity // 2
            self.data = <char*> PyMem_Realloc(self.data, self.capacity)

    def absolute_index(self, int index):
        """Получение абсолютного значения индекса
        :param index: индекс элемента
        :return: полученный индекс
        """
        cdef int now_length = self.length
        if now_length == 0:
            now_length = 1
        if index < 0:
           if abs(index) > now_length:
               index = - (abs(index) % now_length)
           if index != 0:
               index = now_length - abs(index)
        elif index > now_length:
            index = index % now_length
        return index

    def __getitem__(self, int index):
        """Получение элемента по индексу
        :param index: индекс элемента
        :return: полученный элемент
        """
        if 0 <= index < self.length:
            if self.typecode == 1:
                return (<double *> self.data)[index]
            return (<long *> self.data)[index]
        raise IndexError("Неккоректный индекс")

    def __setitem__(self, int index, object obj):
        """Запись элемента по индексу
        :param index: индекс
        :param obj: объект записи"""
        cdef double value_d
        cdef int value
        if obj == None:
            raise ValueError("Неккоректный obj")
        if index < self.length and index >= 0:
            if self.typecode == 1:
                if (isinstance(obj, int) or isinstance(obj, float)):
                    value_d = PyFloat_AsDouble(float(obj))
                else:
                    self.size_down()
                    raise TypeError()
                (<double *> self.data)[index] = value_d
            else:
                if (isinstance(obj, int)):
                    value = PyLong_AsLong(int(obj))
                else:
                    self.size_down()
                    raise TypeError()
                (<long *> self.data)[index] = value
        else:
            raise IndexError("Неккоректный индекс")


    def append(self, object obj = None):
        """Добавление элемента в конец массива
        :param obj: объект добавления"""
        cdef double value_d
        cdef int value
        if obj == None:
            raise ValueError
        if self.typecode == 1:
            if (isinstance(obj, int) or isinstance(obj, float)):
                self.size_up()
                value_d = PyFloat_AsDouble(float(obj))
                (<double *> self.data)[self.length - 1] = value_d
            else:
                raise TypeError()
        else:
            if isinstance(obj, int):
                self.size_up()
                value = PyLong_AsLong(obj)
                (<long *> self.data)[self.length - 1] = value
            else:
                raise TypeError()

    def insert(self, int index, object obj = None):
        """Вставка элемента по индексу
        :param index: индекс вставки
        :param obj: объект вставки"""
        cdef int i
        cdef object temp_elem
        cdef object prev_elem
        if obj == None:
            raise ValueError("Неккоректный obj")
        if index > 0:
            index = self.absolute_index(index)
            if index == 0:
                index = self.length
        else:
            index = self.absolute_index(index)
        self.size_up()
        if self.length > 1:
            value = self.__getitem__(index)
            prev_elem = self.__getitem__(index)
        self.__setitem__(index, obj)
        for i in range(index + 1, self.length):
            temp_elem = self.__getitem__(i)
            self.__setitem__(i, prev_elem)
            prev_elem = temp_elem


    def remove(self, object obj = None):
        """Удаление элемента по значению
        :param obj: удаляемый элемент"""
        cdef int i
        cdef int j
        if obj != None:
            for i in range(0, self.length):
                if obj == self.__getitem__(i):
                    for j in range(i, self.length - 1):
                        self.__setitem__(j, self.__getitem__(j + 1))
                    self.size_down()
                    return
        raise ValueError("Объект отсутствует")

    def pop(self, int index = -1):
        """Удаление элемента по индексу с возвратом
        :param index: индекс элемента
        :return: убранный элемент"""
        if index == -1:
            index = self.length - 1
        cdef int i
        if index < 0:
           index = self.length - abs(index)
        if index < self.length:
            value = self.__getitem__(index)
            for i in range(index, self.length - 1):
                self.__setitem__(i, self.__getitem__(i + 1))
            self.size_down()
            return value
        else:
            raise IndexError("Неккоректный индекс")

    def __len__(self):
        """Длина массива
        :return: Длина массива"""
        return self.length

    def __sizeof__(self):
        """Размер массива в памяти
        :return: Размер массива в памяти"""
        return sizeof(self.data)

    def __reversed__(self):
        """Получение инвертированного массива
        :return: инвертированный массив"""
        cdef int i
        for i in range(self.length):
            yield self.__getitem__(self.length - 1 - i)

    def __eq__(self, object other):
        """Метод для сравнения массива
        :param other: объект для сравнения
        :return: результат (true/false)"""
        cdef int i
        if not isinstance(other, (array.array, Array)):
            return False
        if self.length == len(other):
            for i in range(0, self.length):
                if other[i] != self.__getitem__(i):
                    return False
            return True
        return False

    def __repr__(self):
        if self.typecode == 1:
            return (f"Array(double, "
                f"{[self.__getitem__(i) for i in range(self.length)]})")
        if self.typecode == 2:
            return (f"Array(long, "
                f"{[self.__getitem__(i) for i in range(self.length)]})")