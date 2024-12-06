import subprocess
from idlelib.pyshell import capture_warnings
from PyQt6 import QtWidgets, uic
from db import *
import sys
import random
import importlib
import os
import index
from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication([])
winreg = uic.loadUi('registration.ui')
winlog = uic.loadUi('login.ui')
winwelcome = uic.loadUi('HELLO.ui')
winQ = uic.loadUi("test.ui")
win1 = uic.loadUi("untitled.ui")
winQTDIAG = uic.loadUi("ISP9.ui")


con = sqlite3.connect('users.db')
create_db(con)


def openlogin():
    winreg.close()
    winlog.show()


winreg.pushlogButton.clicked.connect(openlogin)


def register():
    lname = winreg.lineEdit.text()
    fname = winreg.lineEdit_2.text()
    email = winreg.lineEdit_3.text()
    password = winreg.lineEdit_4.text()
    confirm_password = winreg.lineEdit_5.text()
    if not lname or not fname or not email or not password:
        QtWidgets.QMessageBox.warning(winreg, 'Ошибка', 'Заполните все поля')
        return
    if password == confirm_password and password != '':
        try:
            if find_user_email(con, email):
                QtWidgets.QMessageBox.warning(winreg, "Ошибка", "Пользователь с таким email уже существует")
                return
            insert(con, lname, fname, email, password)
            QtWidgets.QMessageBox.information(winreg, 'Успех', 'Вы успешно зарегистрированы')
            winreg.close()
            winlog.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(winreg, "Ошибка", f"Не удалось зарегистрироваться: {e}")
    else:
        QtWidgets.QMessageBox.warning(winreg, 'Ошибка', 'Пароли не совпадают')


def login():
    try:
        email = winlog.lineEdit.text()
        password = winlog.lineEdit_2.text()

        if not email or not password:
            QtWidgets.QMessageBox.warning(winlog, 'Ошибка', 'Заполните все поля')
            return
        user = select(con, email, password)
        if user:
            QtWidgets.QMessageBox.information(winlog, 'Успех', 'Вы успешно вошли в систему')
            winlog.close()
            winwelcome.show()
        else:
            QtWidgets.QMessageBox.warning(winlog, 'Ошибка', 'Неверный email или пароль')
    except Exception as e:
        QtWidgets.QMessageBox.critical(winlog, 'Ошибка', f'Произошла ошибка при входе: {e}')


def openQuestions():
    winwelcome.close()
    loadQuestion(quesions[0])
    winQ.show()


winwelcome.pushButton.clicked.connect(openQuestions)
winreg.pushregButton.clicked.connect(register)
winlog.pushlogButton.clicked.connect(login)


class Question:
    def __init__(self, text, ans, otherAns):
        self.text = text
        self.ans = ans
        self.otherAns = otherAns


quesions = [
    Question("цвет неба", "голубой", ["красный", "оранжевый", "?"]),
    Question("цвет машины ?", "черная", ["красная", "желтая", "синяя"]),
    Question("дней в неделе", "7", ["5", "6", "8"])
]

questionIndex = 0
rightAns = 0
Ans = ""
lbl = winQ.label
rBtn1 = winQ.radioButton
rBtn2 = winQ.radioButton_2
rBtn3 = winQ.radioButton_3
rBtn4 = winQ.radioButton_4
layout = winQ.verticalLayout


def loadQuestion(quest):
    global rightAns, questionIndex, Ans
    l = quest.otherAns
    l.append(quest.ans)
    Ans = quest.ans
    random.shuffle(l)
    rBtn1.setText(l[0])
    rBtn2.setText(l[1])
    rBtn3.setText(l[2])
    rBtn4.setText(l[3])
    lbl.setText(quest.text)


def res(self):
    global rightAns, questionIndex
    for i in range(layout.count()):
        rbt = layout.itemAt(i).widget()
        if rbt.isChecked():
            if Ans == rbt.text():
                rightAns += 1
            break
    questionIndex += 1
    if questionIndex >= len(quesions):
        result()
        return
    loadQuestion(quesions[questionIndex])


def result():
    layout.setParent(None)
    winQ.pushButton.setParent(None)
    rBtn1.setParent(None)
    rBtn2.setParent(None)
    rBtn3.setParent(None)
    rBtn4.setParent(None)
    lbl.setText(f"Правильных: {rightAns}, Всего:{len(quesions)}")


def goBackToMenu():
    winQ.close()
    winwelcome.show()


winQ.pushBackButton.clicked.connect(goBackToMenu)


def openDIAG():
    winwelcome.close()
    winQTDIAG.show()


winwelcome.pushButton_2.clicked.connect(openDIAG)


def open_game_page():

    game_module = importlib.import_module('index')
    game_module.main()


winwelcome.pushButton_3.clicked.connect(open_game_page)


def GoBackToMenu():
    win1.close()
    winwelcome.show()


win1.pushButton.clicked.connect(GoBackToMenu)



winQ.radioButton.clicked.connect(res)
winQ.radioButton_2.clicked.connect(res)
winQ.radioButton_3.clicked.connect(res)
winQ.radioButton_4.clicked.connect(res)


winreg.show()
sys.exit(app.exec())

con.close()