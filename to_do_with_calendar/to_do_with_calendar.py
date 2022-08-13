# -*- coding: utf-8 -*-

"""
This program allows you to create and track a to-do list for the week.
The selection is made using the calendar window. When you start the program,
a directory is created in the folder with the program in which it will
be created and stored .json files for storing records.
"""

import sys
import os
import datetime
import json

from typing import Union
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QWidget, QCalendarWidget, QVBoxLayout, QLabel, QTabWidget, QStyle,
                             QPushButton, qApp, QPlainTextEdit)


class BaseWindow(QWidget):

    """In class BaseWindow general settings for most application windows are implemented in"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        ico = QtGui.QIcon("images/to_do.png")
        self.setWindowIcon(ico)

        self.setWindowTitle("To Do List")
        self.move(self.width() * -2, 0)  # we will display the window outside the screen

        self.main_box = QVBoxLayout()
        self.setLayout(self.main_box)  # Passing the link to the main container to the window

    def move_center_display(self):
        """let's display a window in the center of the screen"""
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()) // 2
        self.move(x, y)


class ToDoList(BaseWindow):

    """class ToDoListWithCalendar implements a window with entries for a week with a selected date"""

    def __init__(self, headings: Union[list, tuple], current_index: int, path: str, parent=None):
        BaseWindow.__init__(self, parent)  # create window
        self.setMinimumSize(500, 300)

        self.headings = headings  # tab headers
        self.current_index = current_index  # the tab that will be opened
        self.path = path  # the path to the folder for storing json files

        self.is_closed = False  # auxiliary flag

        file_name = f'{self.headings[0]}_{self.headings[6]}.json'
        self.file_path = os.path.join(self.path, file_name)
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as json_file:  # open file
                self.contents = json.load(json_file)  # downloading data from the file
                self.contents = list(self.contents.values())
        else:
            with open(self.file_path, 'w', encoding='utf-8'):  # create file
                pass
            self.contents = ['', '', '', '', '', '', '']

        self.tab = QTabWidget()
        style = self.style()
        icon = style.standardIcon(QStyle.SP_DriveNetIcon)

        for content, heading in zip(self.contents, self.headings):
            self.tab.addTab(QPlainTextEdit(content), icon, heading)

        self.tab.setCurrentIndex(self.current_index)
        self.tab.setElideMode(QtCore.Qt.ElideNone)

        self.btn_save = QPushButton('Save')
        self.btn_save.setAutoDefault(True)
        self.btn_save.clicked.connect(self.clc_btn_save)
        self.btn_save.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
        self.btn_save.setToolTip('CTRL + S')

        self.main_box.addWidget(self.tab)
        self.main_box.addWidget(self.btn_save, alignment=QtCore.Qt.AlignHCenter)

        self.move_center_display()
        self.show()

    @QtCore.pyqtSlot()
    def clc_btn_save(self):
        tmp_dct = {self.tab.tabText(ind): self.tab.widget(ind).toPlainText() for ind in range(7)}
        with open(self.file_path, 'w', encoding='utf-8') as outfile:
            json.dump(tmp_dct, outfile)

    def closeEvent(self, event):
        self.is_closed = True
        self.clc_btn_save()
        event.accept()


class MainWindow(BaseWindow):
    """class MainWindow implements the main application window"""

    def __init__(self, folder: str = 'ToDoListWithCalendar', parent=None):
        BaseWindow.__init__(self, parent)  # create window

        self.folder = folder  # the name of the folder for storing records in the application folder
        if not os.path.exists(folder):
            os.mkdir(folder)  # creating a folder to store records in the application folder
        os.chdir(folder)  # changing the directory
        self.path = os.getcwd()  # getting the current working directory

        self.choose_date = None
        self.open_dates = []

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QtCore.QDate].connect(self.show_date)
        self.calendar.activated[QtCore.QDate].connect(self.get_date)

        self.lbl = QLabel()
        self.date = self.calendar.selectedDate()
        self.lbl.setText(f'<center>{self.date.toString("dddd dd MMMM yyyy").title()}</center>')

        self.main_box.addWidget(self.calendar)
        self.main_box.addWidget(self.lbl)

        self.move_center_display()
        self.show()

    @QtCore.pyqtSlot()
    def show_date(self):
        self.date = self.calendar.selectedDate()
        self.lbl.setText(f'<center>{self.date.toString("dddd dd MMMM yyyy").title()}</center>')

    @QtCore.pyqtSlot()
    def get_date(self):
        self.choose_date = self.calendar.selectedDate().toPyDate()  # <class 'datetime.date'>
        if str(self.choose_date) not in self.open_dates:  # to exclude the repeated display of some dates
            selected_dates = {'1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': ''}

            weekday = self.choose_date.isocalendar()[2]
            selected_dates[str(weekday)] = str(self.choose_date)

            next_weekday, previous_weekday = weekday, weekday
            delta = datetime.timedelta(days=1)
            next_day, previous_day = self.choose_date, self.choose_date

            while next_weekday < 7:
                next_day += delta
                next_weekday = next_day.isocalendar()[2]
                selected_dates[str(next_weekday)] = str(next_day)

            while previous_weekday > 1:
                previous_day -= delta
                previous_weekday = previous_day.isocalendar()[2]
                selected_dates[str(previous_weekday)] = str(previous_day)

            selected_dates_values = list(selected_dates.values())
            self.open_dates.extend(selected_dates_values)

            to_do_list = ToDoList(headings=selected_dates_values,
                                  current_index=weekday - 1,
                                  path=self.path)

            while not to_do_list.is_closed:
                qApp.processEvents()  # Starting the cycle rotation

            for elem in selected_dates_values:
                self.open_dates.remove(elem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # icon = QtGui.QIcon(r"images/calendar.png")
    # app.setWindowIcon(icon)
    main_window = MainWindow()
    sys.exit(app.exec_())
