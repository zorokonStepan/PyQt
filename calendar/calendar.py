# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel, QApplication, QVBoxLayout
from PyQt5.QtCore import QDate
from PyQt5 import QtGui


class Calendar(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)  # create window
        self.setWindowTitle('Календарь')
        icon = QtGui.QIcon(r"images/calendar.png")
        self.setWindowIcon(icon)
        self.resize(400, 200)
        self.move(self.width() * -2, 0)  # we will display the window outside the screen

        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.show_date)

        self.lbl = QLabel()
        self.date = self.cal.selectedDate()
        self.lbl.setText(f'<center>{self.date.toString("dddd dd MMMM yyyy").title()}</center>')

        self.main_box = QVBoxLayout(self)
        self.main_box.addWidget(self.cal)
        self.main_box.addWidget(self.lbl)

        self.show()

        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()) // 2
        self.move(x, y)  # let's display a window in the center of the screen

    def show_date(self):
        self.date = self.cal.selectedDate()
        self.lbl.setText(f'<center>{self.date.toString("dddd dd MMMM yyyy").title()}</center>')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calendar = Calendar()
    sys.exit(app.exec_())
