"""
Лабиринты (Sidewinder / Best-first search)
Самарин Никита КИ21-17/2Б
"""
from PyQt5.QtWidgets import *

import gui
import sys
import maze_draw


class Main(QMainWindow, gui.Ui_Form):
    """
    Класс интерфейса
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start_labirinth)
        self.pushButton_3.clicked.connect(self.select_output_text_file)
        self.pushButton_2.clicked.connect(self.select_input_text_file)

        self.lineEdit.setText("10")
        self.lineEdit_2.setText("10")
        self.output_text_file = ""
        self.output_pic_file = ""
        self.input_text_file = ""
        self.input_pic_file = ""

    def start_labirinth(self):
        try:
            rows, columns = [int(self.lineEdit.text()), int(self.lineEdit_2.text())]
        except ValueError:
            self.label_6.setText("Неккоректный ввод")
            return
        if rows > 30 or columns > 30 or (min(rows, columns) <= 1):
            self.label_6.setText("Неккоректный ввод")
            return
        self.output_text_file = self.lineEdit_4.text()
        self.output_pic_file = self.lineEdit_5.text()
        self.input_text_file = self.lineEdit_3.text()
        self.input_pic_file = self.lineEdit_6.text()
        print(self.output_pic_file)
        print(self.output_text_file)
        print(self.input_text_file)
        print(self.input_pic_file)
        maze_draw.maze_draw(rows, columns, self.output_text_file, self.output_pic_file, self.input_text_file, self.input_pic_file)

    def select_output_text_file(self):
        self.output_text_file = QFileDialog.getSaveFileName(filter="Text files (*.txt)")[0]
        self.lineEdit_4.setText(self.output_text_file)

    def select_input_text_file(self):
        self.input_text_file = QFileDialog.getOpenFileName(filter="Text files (*.txt)")[0]
        self.lineEdit_3.setText(self.input_text_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec()