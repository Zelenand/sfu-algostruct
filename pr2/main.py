"""
Музыкальный плеер
"""

import playlist
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import gui
import sys
import pickle
from pygame import mixer

class composition_list_item(QListWidgetItem):
    """
    Класс элемента QListWidget
    """
    def __init__(self, linked_list_item):
        """
        :param linked_list_item: элемент связного списка
        """
        super().__init__(linked_list_item.data.name)
        self.__linked_list_item = linked_list_item

    @property
    def linked_list_item(self):
        """
        Получить элемент связного списка
        :return: элемент связного списка
        """
        return self.__linked_list_item


class Main(QMainWindow, gui.Ui_Form):
    """
    Класс интерфейса
    """
    def __init__(self):
        super().__init__()
        with open('data.pickle', 'rb') as f:
            self.data = pickle.load(f)
        self.index = 0
        mixer.init()
        self.current_playlist = None
        self.setupUi(self)
        self.timer = QTimer()
        self.update_comboBox()

        self.comboBox.currentIndexChanged.connect(self.update_listWidget)
        self.pushButton_6.clicked.connect(self.add_playlist)
        self.pushButton_7.clicked.connect(self.delete_playlist)
        self.pushButton_2.clicked.connect(self.add_composition)
        self.pushButton.clicked.connect(self.delete_composition)
        self.pushButton_9.clicked.connect(self.move_composition_up)
        self.pushButton_10.clicked.connect(self.move_composition_down)
        self.pushButton_3.clicked.connect(self.play_all)
        self.pushButton_5.clicked.connect(self.play_pause)
        self.pushButton_8.clicked.connect(self.previous_track)
        self.pushButton_4.clicked.connect(self.next_track)
        self.horizontalSlider.sliderPressed.connect(self.play_pause)
        self.horizontalSlider.sliderReleased.connect(self.slider_change)
        self.timer.timeout.connect(self.current_track_update)

    def update_comboBox(self):
        """
        Обновить список плейлистов
        """
        self.comboBox.clear()
        for i in range(len(self.data)):
            self.comboBox.addItem(self.data[i].name, self.data[i])
        self.comboBox.setCurrentIndex(0)
        self.update_listWidget()


    def update_listWidget(self):
        """
        Обновить список композицицй
        """
        self.listWidget.clear()
        new_linked_list = self.comboBox.currentData()
        for i in new_linked_list:
            item = composition_list_item(i)
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(self.index)

    def add_playlist(self):
        """
        Добавить плейлист
        """
        print(len(self.data))
        self.data.append(playlist.PlayList(str(int(self.data[len(self.data) - 1].name) + 1)))
        self.comboBox.addItem(self.data[len(self.data) - 1].name, self.data[len(self.data) - 1])
        self.save_data()

    def delete_playlist(self):
        """
        Удалить выбранный плейлист
        """
        if len(self.data) > 1:
            del_playlist = self.comboBox.currentData()
            self.data.remove(del_playlist)
            self.comboBox.removeItem(self.comboBox.currentIndex())
            self.update_listWidget()
            self.save_data()

    def add_composition(self):
        """
        Добавить композицию
        """
        path = QFileDialog.getOpenFileName(self, "Open file", "C:/Users/%USERNAME%/", "Sound files (*.mp3)")[0]
        if path != '' and path != " ":
            self.comboBox.currentData().append(playlist.Composition(path))
            self.update_listWidget()
            self.save_data()

    def delete_composition(self):
        """
        Удалить выбранную композицию
        """
        del_composition = self.listWidget.itemFromIndex(self.listWidget.currentIndex())
        if del_composition != None:
            index = self.listWidget.currentRow()
            self.comboBox.currentData().remove(del_composition.linked_list_item.data)
            if index <= self.index:
                self.index = self.index - 1
            self.update_listWidget()
            if mixer.music.get_busy() and self.index == index:
                self.next_track()
            self.save_data()

    def move_composition_down(self):
        """
        Сместить композицию вниз в списке
        """
        move_composition = self.listWidget.itemFromIndex(self.listWidget.currentIndex())
        index = self.listWidget.currentRow()
        if move_composition != None and index < len(self.comboBox.currentData()) - 1 and index > -1:
            data = move_composition.linked_list_item
            self.comboBox.currentData().insert(data.next_item, data.data)
            self.comboBox.currentData().remove(data)
            self.update_listWidget()
            self.listWidget.setCurrentRow(index + 1)
            self.save_data()

    def move_composition_up(self):
        """
        Сместить композицию вверх в списке
        """
        move_composition = self.listWidget.itemFromIndex(self.listWidget.currentIndex())
        index = self.listWidget.currentRow()
        if move_composition != None and index < len(self.comboBox.currentData()) and index > 0:
            data = move_composition.linked_list_item
            self.comboBox.currentData().remove(data.data)
            if index > 1:
                self.comboBox.currentData().insert(data.previous_item.previous_item, data.data)
            else:
                self.comboBox.currentData().append_left(data.data)
            self.update_listWidget()
            self.listWidget.setCurrentRow(index - 1)
            self.save_data()

    def save_data(self):
        """
        Сохранить данные
        """
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.data, f)

    def play_all(self):
        """
        Начать воспроизведение композиций
        """
        self.current_playlist = self.comboBox.currentData()
        if len(self.current_playlist) != 0:
            self.horizontalSlider.setValue(0)
            self.current_playlist.play_all(self.listWidget.currentRow())
            mixer.music.load(self.current_playlist.current_composition.data.path)
            self.preset_track()
            self.label.setText(self.current_playlist.current_composition.data.name)
            mixer.music.play()
            self.timer.start()

    def next_track(self):
        """
        Переключить на следующую композицию
        """
        if self.current_playlist != None and len(self.current_playlist) != 0:
            self.horizontalSlider.setValue(0)
            self.current_playlist = self.comboBox.currentData()
            self.current_playlist.play_all(self.listWidget.currentRow())
            self.current_playlist.next_track()
            self.index = self.listWidget.currentRow() + 1
            if self.index >= len(self.current_playlist):
                self.index = 0
            self.listWidget.setCurrentRow(self.index)
            mixer.music.load(self.current_playlist.current_composition.data.path)
            self.preset_track()
            self.label.setText(self.current_playlist.current_composition.data.name)
            mixer.music.play()
            self.timer.start()

    def previous_track(self):
        """
        Переключить на предыдущую композицию
        """
        if self.current_playlist != None and len(self.current_playlist) != 0:
            self.horizontalSlider.setValue(0)
            self.current_playlist = self.comboBox.currentData()
            self.current_playlist.play_all(self.listWidget.currentRow())
            self.current_playlist.previous_track()
            self.index = self.listWidget.currentRow() - 1
            if self.index < 0:
                self.index = len(self.current_playlist) - 1
            self.listWidget.setCurrentRow(self.index)
            mixer.music.load(self.current_playlist.current_composition.data.path)
            self.preset_track()
            self.label.setText(self.current_playlist.current_composition.data.name)
            mixer.music.play()
            self.timer.start()

    def play_pause(self):
        """
        Поставить паузуу/снять с паузы
        """
        if self.current_playlist != None:
            if mixer.music.get_busy():
                self.timer.stop()
                mixer.music.pause()
            else:
                self.timer.start()
                mixer.music.unpause()

    def current_track_update(self):
        """
        Обновление времени проигрывания
        """
        self.horizontalSlider.setValue(self.horizontalSlider.sliderPosition())
        duration = int(self.current_playlist.current_composition.data.duration)
        value = int(mixer.music.get_pos() /duration)
        if value > self.horizontalSlider.value():
            self.horizontalSlider.setValue(value)
        self.label_2.setText(str(int(value / 1000 * duration // 60)) + ":" +
                             str(int(value / 1000 * duration % 60)))
        if value >= 990:
            self.timer.stop()
            self.horizontalSlider.setValue(0)
            self.next_track()

    def preset_track(self):
        """
        Установка названия и длительности запущенной композиции
        """
        duration = int(self.current_playlist.current_composition.data.duration)
        self.label_3.setText(str(duration//60) + ":" + str(duration % 60))
        self.label.setText(self.current_playlist.current_composition.data.name)

    def slider_change(self):
        """
        Изменение позиции проигрывания в песне при смещении слайдера
        """
        value = self.horizontalSlider.sliderPosition()
        if value >= 990:
            self.next_track()
        else:
            self.horizontalSlider.setValue(0)
            duration = int(self.current_playlist.current_composition.data.duration)
            mixer.music.set_pos(value / 1000 * duration)
            self.horizontalSlider.setValue(value)
            self.play_pause()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec()