"""
Интерфейс
"""
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    """
    Интерфейс
    """
    def setupUi(self, Form):
        """
        Создание интерфейса
        """
        Form.setObjectName("Form")
        Form.resize(597, 496)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 350, 201, 31))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 370, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 320, 111, 41))
        self.pushButton_2.setAutoRepeat(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(325, 120, 261, 192))
        self.listWidget.setObjectName("listWidget")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(50, 320, 160, 22))
        self.horizontalSlider.setMouseTracking(False)
        self.horizontalSlider.setTabletTracking(False)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setTracking(True)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMaximum(1000)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(390, 420, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(70, 390, 111, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(360, 20, 181, 31))
        self.comboBox.setObjectName("comboBox")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(330, 60, 121, 41))
        self.pushButton_6.setAutoRepeat(False)
        self.pushButton_6.setFlat(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(460, 60, 121, 41))
        self.pushButton_7.setAutoRepeat(False)
        self.pushButton_7.setFlat(False)
        self.pushButton_7.setObjectName("pushButton_7")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 280, 51, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(200, 280, 51, 31))
        self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(510, 420, 81, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(300, 420, 81, 31))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(280, 150, 41, 51))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setGeometry(QtCore.QRect(280, 230, 41, 51))
        self.pushButton_10.setObjectName("pushButton_10")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(60, 100, 151, 151))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """
        Установка надписей на элементах интерфейса
        """
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название композиции"))
        self.pushButton.setText(_translate("Form", "Удалить песню"))
        self.pushButton_2.setText(_translate("Form", "Добавить песню"))
        self.pushButton_3.setText(_translate("Form", "Включить песню"))
        self.pushButton_5.setText(_translate("Form", "Пуск/Пауза"))
        self.pushButton_6.setText(_translate("Form", "Добавить плейлист"))
        self.pushButton_7.setText(_translate("Form", "Удалить плейлист"))
        self.label_2.setText(_translate("Form", "00:00"))
        self.label_3.setText(_translate("Form", "00:00"))
        self.pushButton_4.setText(_translate("Form", "Следующая"))
        self.pushButton_8.setText(_translate("Form", "Предыдущая"))
        self.pushButton_9.setText(_translate("Form", "▲"))
        self.pushButton_10.setText(_translate("Form", "▼"))
