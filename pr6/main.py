"""
Астероиды
Самарин Никита КИ21-17/2Б
"""
from PyQt5.QtWidgets import *

import asteroid_field
import gui
import sys

class Main(QMainWindow, gui.Ui_Form):
    """
    Класс интерфейса
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start_field)

    def start_field(self):
        self.label_9.setText("")
        try:
            height, width, asteroid_num, asteroid_min_rad, asteroid_max_rad, asteroid_min_speed, asteroid_max_speed = \
                [int(self.lineEdit.text()), int(self.lineEdit_2.text()), int(self.lineEdit_7.text())
                      , int(self.lineEdit_4.text()), int(self.lineEdit_3.text()), float(self.lineEdit_6.text())
                      , float(self.lineEdit_5.text())]
        except ValueError:
            self.label_9.setText("Неккоректный ввод")
            return
        if asteroid_max_rad < asteroid_min_rad or asteroid_max_speed < asteroid_min_speed \
                or (min(height, width, asteroid_num, asteroid_min_rad, asteroid_max_rad, asteroid_min_speed,
                        asteroid_max_speed) <= 0):
            self.label_9.setText("Неккоректный ввод")
            return
        if height < 200 or height > 1080:
            self.label_9.setText("Неккоректный ввод")
            return
        if width < 200 or width > 1920:
            self.label_9.setText("Неккоректный ввод")
            return
        if asteroid_num > 300:
            self.label_9.setText("Неккоректный ввод")
            return
        if min(height, width) * min(height, width) <= asteroid_max_rad * asteroid_max_rad * asteroid_num:
            self.label_9.setText("Неккоректный ввод")
            return
        asteroid_field.asteroid_field_start(height, width, asteroid_num, asteroid_min_rad, asteroid_max_rad,
                                            asteroid_min_speed, asteroid_max_speed)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec()