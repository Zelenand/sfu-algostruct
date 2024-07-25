"""
Модуль реализующий двусвязный кольцевой список
"""
class LinkedListItem:
    """Узел связного списка"""
    def __init__(self, data=None):
        self.data = data
        self.__next = None
        self.__previous = None

    @property
    def next_item(self):
        """Следующий элемент"""
        return self.__next

    @next_item.setter
    def next_item(self, value):
        self.__next = value
        value.__previous = self

    @property
    def previous_item(self):
        """Предыдущий элемент"""
        return self.__previous

    @previous_item.setter
    def previous_item(self, value):
        self.__previous = value
        value.__next = self

    #def __repr__(self):
        #return f"data: {self.data}"


class LinkedList:
    """Связный список"""
    def __init__(self, first_item = None):
        """
        :param first_item: первый элемент
        """
        if first_item == None:
            self.first_item = first_item
        elif not (isinstance(first_item, LinkedListItem)):
            self.first_item = LinkedListItem(first_item)
        else:
            self.first_item = first_item
            if self.first_item.next_item == None:
                self.first_item.next_item = self.first_item
            if self.first_item.previous_item == None:
                self.first_item.previous_item = self.first_item

    @property
    def last(self):
        """
        Последний элемент
        :return: последний элемент
        """
        if self.first_item == None:
            return None
        return self.first_item.previous_item

    def append_left(self, item):
        """
        Добавление слева
        :param item: элемент для добавления
        """
        if not (isinstance(item, LinkedListItem)):
            linked_list_item = LinkedListItem(item)
        else:
            linked_list_item = item
        if self.first_item == None:
            self.first_item = linked_list_item
            self.first_item.next_item = self.first_item
        else:
            last_item = self.last
            linked_list_item.next_item = self.first_item
            last_item.next_item = linked_list_item
            self.first_item = linked_list_item

    def append_right(self, item):
        """
        Добавление справа
        :param item: элемент для добавления
        """
        if not (isinstance(item, LinkedListItem)):
            linked_list_item = LinkedListItem(item)
        else:
            linked_list_item = item
        if self.first_item == None:
            self.first_item = linked_list_item
            self.first_item.next_item = self.first_item
        else:
            last_item = self.last
            last_item.next_item = linked_list_item
            linked_list_item.next_item = self.first_item


    def append(self, item):
        """
        Добавление справа
        :param item: элемент для добавления
        """
        self.append_right(item)

    def remove(self, item):
        """
        Удаление
        :param item: элемент для удаления
        """
        len = self.__len__()
        if self.first_item != None:
            if isinstance(item, LinkedListItem):
                now_item = self.first_item
                for _ in range(len):
                    if now_item is item:
                        if len == 1:
                            self.first_item = None
                        else:
                            now_item.previous_item.next_item = now_item.next_item
                            if now_item is self.first_item:
                                self.first_item = now_item.next_item
                        return
                    now_item = now_item.next_item
            else:
                now_item = self.first_item
                for _ in range(len):
                    if now_item.data == item:
                        if len == 1:
                            self.first_item = None
                        else:
                            now_item.previous_item.next_item = now_item.next_item
                            if now_item is self.first_item:
                                self.first_item = now_item.next_item
                        return
                    now_item = now_item.next_item
        raise ValueError

    def insert(self, previous, item):
        """
        Вставка после элемента
        :param previous: элемент после которого добавить
        :param item: элемент для добавления
        """
        if not (isinstance(item, LinkedListItem)):
            new_item = LinkedListItem(item)
        else:
            new_item = item
        if not (isinstance(previous, LinkedListItem)):
            previous = LinkedListItem(previous)
        else:
            previous = previous
        if previous in self:
            if previous is self.first_item:
                new_item.next_item = self.first_item.next_item
                self.first_item.next_item = new_item
                return
            new_item.next_item = previous.next_item
            previous.next_item = new_item
            return
        raise ValueError


    def __len__(self):
        """
        Длина списка
        :return: Длина списка
        """
        len = 0
        if self.first_item:
            len = 1
            if not (self.first_item.next_item is self.first_item):
                len = 2
                item = self.first_item.next_item
                last_item = self.last
                while not(item is last_item):
                    len += 1
                    item = item.next_item
        return len


    def __iter__(self):
        """
        Итерация по списку
        :return: элементы списка по порядку
        """
        now_item = self.first_item
        for _ in range(self.__len__()):
            yield now_item
            now_item = now_item.next_item


    def __getitem__(self, index):
        """
        Получить элемент по индексу
        :param index: индекс
        :return: элемент по индексу
        """
        len = self.__len__()
        if index >= len or index < -len:
            raise IndexError
        item = self.first_item
        for _ in range(index):
            item = item.next_item
        return item

    def __contains__(self, item):
        """
        Содержится ли элемент
        :param item: элемент
        :return: Содержится ли элемент
        """
        len = self.__len__()
        if self.first_item != None:
            if not isinstance(item, LinkedListItem):
                now_item = self.first_item
                for _ in range(len):
                    if now_item.data == item:
                        return True
                    now_item = now_item.next_item
            else:
                now_item = self.first_item
                for _ in range(len):
                    if now_item is item:
                        return True
                    now_item = now_item.next_item
        return False

    def __reversed__(self):
        len = self.__len__()
        for index in range(len):
            yield self.__getitem__(len - index - 1)