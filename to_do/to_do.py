# -*- coding: utf-8 -*-

import sys
import os
import json

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QStyle, QPushButton,
                             QPlainTextEdit, QLineEdit)

"""
This program allows you to create and track a to-do list. It is possible to create and 
delete tabs in an unlimited number. The data is stored in .json file
"""


class ToDo(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(500, 300)
        self.setWindowTitle("ToDo")
        icon = QtGui.QIcon(r"images/to_do.png")
        self.setWindowIcon(icon)
        self.move(self.width() * -2, 0)  # we will display the window outside the screen

        path = os.getcwd()  # getting the current working directory
        file_name = 'ToDo.json'
        self.file_path = os.path.join(path, file_name)
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as json_file:  # open file
                self.contents = json.load(json_file)  # downloading data from the file
                self.headings = list(self.contents.keys())
                self.contents = list(self.contents.values())
        else:
            with open(self.file_path, 'w', encoding='utf-8'):  # create file
                pass
            self.headings = ['tab 1']
            self.contents = ['']

        self.main_box = QVBoxLayout()
        # ---
        self.tab = QTabWidget()
        self.tab.setMovable(True)
        self.style = self.style()
        self.icon = self.style.standardIcon(QStyle.SP_DriveNetIcon)
        for content, heading in zip(self.contents, self.headings):
            self.tab.addTab(QPlainTextEdit(content), self.icon, heading)
        self.tab.setCurrentIndex(0)
        self.tab.setElideMode(QtCore.Qt.ElideNone)
        # ---
        self.buttons = QHBoxLayout()

        self.btn_add_tab = QPushButton('Add tab')
        self.btn_add_tab.clicked.connect(self.clc_btn_add_tab)
        self.btn_add_tab.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Space))
        self.btn_add_tab.setToolTip('CTRL + Space')

        self.btn_remove_tab = QPushButton('Delete tab')
        self.btn_remove_tab.clicked.connect(self.clc_btn_remove_tab)
        self.btn_remove_tab.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Delete))
        self.btn_remove_tab.setToolTip('CTRL + Delete')

        self.btn_save = QPushButton('Save')
        self.btn_save.setAutoDefault(True)
        self.btn_save.clicked.connect(self.clc_btn_save)
        self.btn_save.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
        self.btn_save.setToolTip('CTRL + S')

        self.buttons.addWidget(self.btn_add_tab)
        self.buttons.addWidget(self.btn_remove_tab)
        self.buttons.addWidget(self.btn_save)
        # ---
        self.rename_tab = QHBoxLayout()

        self.input_head_tab = QLineEdit('')
        self.input_head_tab.setAlignment(QtCore.Qt.AlignLeft)

        self.btn_rename_tab = QPushButton('Rename tab')
        self.btn_rename_tab.clicked.connect(self.clc_btn_rename_tab)
        self.btn_rename_tab.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Down))
        self.btn_rename_tab.setToolTip('CTRL + Down')

        self.rename_tab.addWidget(self.input_head_tab)
        self.rename_tab.addWidget(self.btn_rename_tab)
        # ---
        self.main_box.addWidget(self.tab)
        self.main_box.addLayout(self.buttons)
        self.main_box.addLayout(self.rename_tab)
        self.setLayout(self.main_box)  # Passing the link to the main container to the window

        # let's display a window in the center of the screen
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()) // 2
        self.move(x, y)
        self.show()

    @QtCore.pyqtSlot()
    def clc_btn_rename_tab(self):
        ind = self.tab.currentIndex()
        text = self.input_head_tab.text()
        self.tab.setTabText(ind, text)
        self.input_head_tab.setText('')

    @QtCore.pyqtSlot()
    def clc_btn_add_tab(self):
        cnt = self.tab.count()
        self.tab.addTab(QPlainTextEdit(''), self.icon, f'tab {cnt + 1}')

    @QtCore.pyqtSlot()
    def clc_btn_remove_tab(self):
        ind = self.tab.currentIndex()
        self.tab.removeTab(ind)

    @QtCore.pyqtSlot()
    def clc_btn_save(self):
        tmp_dct = {self.tab.tabText(ind): self.tab.widget(ind).toPlainText() for ind in range(self.tab.count())}
        with open(self.file_path, 'w', encoding='utf-8') as outfile:
            json.dump(tmp_dct, outfile)

    def closeEvent(self, event):
        self.clc_btn_save()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ToDo()
    sys.exit(app.exec_())
