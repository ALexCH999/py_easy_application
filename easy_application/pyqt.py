from PyQt5 import QtWidgets, uic, QtGui
from matplotlib import pyplot as pl

app = QtWidgets.QApplication([])
win = uic.loadUi('ISP9-322AP_cher.ui')


class Main:
    def __init__(self):
        self.pushButton.clicked.connect(bar)  # сто
        self.pushButton_3.clicked.connect(skate)  # точ
        self.pushButton_4.clicked.connect(plot)  # лин
        self.pushButton_2.clicked.connect(pie)  # круго
        def bar(self):
            x = [int(i) for i in win.lineEdit.text().split(",")]
            y = [int(i) for i in win.lineEdit_2.text().split(",")]
            pl.bar(x,y)
            pl.show()

        def skate(self):
            x = [int(i) for i in win.lineEdit.text().split(",")]
            y = [int(i) for i in win.lineEdit_2.text().split(",")]
            pl.scatter(x,y)
            pl.show()

        def plot(self):
            x = [int(i) for i in win.lineEdit.text().split(",")]
            y = [int(i) for i in win.lineEdit_2.text().split(",")]
            pl.plot(x,y)
            pl.show()

        def pie(self):
            x = [int(i) for i in win.lineEdit.text().split(",")]
            pl.pie(x)
            pl.show()









win.pushButton.clicked.connect(bar)#сто
win.pushButton_3.clicked.connect(skate)#точ
win.pushButton_4.clicked.connect(plot)#лин
win.pushButton_2.clicked.connect(pie)#круго



win.show()
exit(app.exec())

