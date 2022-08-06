#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This program allows you to generate a password if you are too lazy to invent
it yourself and you don't want to take one that the browser can offer you
"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5 import QtCore
from string import ascii_letters, digits
from random import choice


class CreatePassword:

    """class CreatePassword generates a password"""

    symbols = ''.join((ascii_letters, digits, '@#$%^&*'))

    def __init__(self, _instance, length: int = 16, step: int = 4):
        self._instance = _instance
        self.length = length
        self.step = step

    def __call__(self):
        pwd_tmp = ''.join([choice(CreatePassword.symbols) for i in range(self.length)])
        pwd = '-'.join([pwd_tmp[i:i+self.step] for i in range(0, len(pwd_tmp), self.step)])
        self._instance.label.setText(f"<center>{pwd}</center>")


class WindowPasswordGenerator(QWidget):

    """class WindowPasswordGenerator implements the main application window"""

    def __new__(cls, *args, **kwargs):
        cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Password Generator')
        self.setMinimumSize(400, 150)
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.WindowStaysOnTopHint)

        self.label = QLabel("<center>Greetings!</center>")

        self.btn_generate_pwd = QPushButton('Generate a password')
        self.btn_generate_pwd.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.btn_generate_pwd.clicked.connect(CreatePassword(WindowPasswordGenerator.__instance))
        self.btn_generate_pwd.setAutoDefault(True)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label, QtCore.Qt.AlignCenter)
        self.vbox.addWidget(self.btn_generate_pwd, QtCore.Qt.AlignCenter)
        self.setLayout(self.vbox)

        self.show()

    def event(self, e):

        """creating the ability to press all buttons using the keyboard"""

        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() in (16777221, 16777220):  # =, Enter
                CreatePassword(WindowPasswordGenerator.__instance)

        return QWidget.event(self, e)  # send farther


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowPasswordGenerator()
    sys.exit(app.exec_())
