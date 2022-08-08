# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This program allows you to time the execution of some of your
work and save data in files with extensions .doc and .txt.
"""

import sys
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QRadioButton, QGroupBox,
                             QHBoxLayout, qApp, QLineEdit, QFileDialog, QMessageBox, QTextEdit)


class Button(QPushButton):
    """class Button to create identical buttons for the main window"""

    def __init__(self, name):
        QPushButton.__init__(self, name)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 30)
        size.setWidth(size.width())
        return size


class BaseWindow(QWidget):

    """In class BaseWindow general settings for most application windows are implemented in"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle("TimeManager")
        self.move(self.width() * -2, 0)  # we will display the window outside the screen
        self.resize(300, 150)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.main_box = QVBoxLayout()
        self.setLayout(self.main_box)  # Passing the link to the main container to the window

    def move_center_display(self):
        """let's display a window in the center of the screen"""
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()) // 2
        self.move(x, y)


class Question(BaseWindow):

    """In class Question user survey windows are implemented regarding the choice of a file to save data"""

    def __init__(self, label_rbtn_1: str, label_rbtn_2: str, label_group_box: str, parent=None):
        BaseWindow.__init__(self, parent)
        self.setMinimumSize(300, 150)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)

        self._check_value = None

        self.label = QLabel()

        self.rbtn_1 = QRadioButton(label_rbtn_1)
        self.rbtn_2 = QRadioButton(label_rbtn_2)
        self.rbtn_2.setChecked(True)  # default check

        self.btn_select = QPushButton('Select')
        self.btn_select.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.btn_select.clicked.connect(self.clc_btn_select)

        self.group_box = QGroupBox(label_group_box)  # Group object
        self.group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.vbox = QVBoxLayout()  # Container
        self.hbox = QHBoxLayout()  # Container

        self.hbox.addWidget(self.rbtn_1, alignment=QtCore.Qt.AlignCenter)  # Adding component
        self.hbox.addWidget(self.rbtn_2, alignment=QtCore.Qt.AlignCenter)  # Adding component

        self.vbox.addLayout(self.hbox)  # Adding component
        self.vbox.addWidget(self.btn_select, alignment=QtCore.Qt.AlignCenter)  # Adding component
        self.vbox.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        self.group_box.setLayout(self.vbox)  # Passing a link to the container
        self.main_box.addWidget(self.group_box)

        self.move_center_display()

    def event(self, e):
        # creating the ability to press all buttons using the keyboard
        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() in (16777221, 16777220):  # =, Enter
                self.clc_btn_select()

        return QWidget.event(self, e)  # send farther

    @property
    def check_value(self):
        return self._check_value

    @check_value.setter
    def check_value(self, value):
        self._check_value = value

    @QtCore.pyqtSlot()
    def clc_btn_select(self):
        if self.rbtn_1.isChecked():
            self.check_value = self.rbtn_1.text()
        elif self.rbtn_2.isChecked():
            self.check_value = self.rbtn_2.text()


class NamedFile(BaseWindow):

    """In class NamedFile implemented a window for specifying a file name for saving user data"""

    from string import ascii_letters, digits

    valid_symbols = f'{ascii_letters}{digits}_'

    def __init__(self, parent=None):
        BaseWindow.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)

        self.file_name = None
        self.valid_file_name = None

        self.message = QLabel('<center>Please change the file name using only letters, numbers and _.</center>\n'
                              '<center>The file will be created with the .doc extension.</center>')

        self.hbox = QHBoxLayout()
        self.enter_file_name = QLineEdit()
        self.enter_file_name.setAlignment(QtCore.Qt.AlignRight)
        self.enter_file_name.setMaxLength(20)
        self.btn_enter = QPushButton('Enter')
        self.btn_enter.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.btn_enter.setAutoDefault(True)
        self.btn_enter.clicked.connect(self.clc_btn_enter)
        self.hbox.addWidget(self.enter_file_name)
        self.hbox.addWidget(self.btn_enter)

        self.main_box.addWidget(self.message, alignment=QtCore.Qt.AlignCenter)
        self.main_box.addLayout(self.hbox)

        self.move_center_display()
        self.show()

    def event(self, e):
        # creating the ability to press all buttons using the keyboard
        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() in (16777221, 16777220):  # =, Enter
                self.clc_btn_enter()

        return QWidget.event(self, e)  # send farther

    @QtCore.pyqtSlot()
    def clc_btn_enter(self):
        self.file_name = self.enter_file_name.text()
        verification_result = self.is_valid_symbols(self.file_name)
        if verification_result is None:
            self.valid_file_name = self.file_name
            self.close()
        elif verification_result:
            self.message.setText(f'<center>The {verification_result} symbol cannot be used</center>')
        else:
            self.message.setText(f'<center>Please enter the file name using only letters, numbers and _.</center>')

    @staticmethod
    def is_valid_symbols(sequence):
        if sequence is None or sequence == '':
            return False
        for i in sequence:
            if i not in NamedFile.valid_symbols:
                return i
        return None


class TimeManager(BaseWindow):

    """class TimeManager implements the main application window and program execution logic"""

    def __init__(self, parent=None):
        BaseWindow.__init__(self, parent)
        self.resize(500, 200)
        self.setMaximumWidth(700)
        self.setMaximumHeight(500)

        self.path_file = None
        self.history = []
        self.time_spent_task = []
        self.last_pressed_btn = None

        self.question = Question('Yes', 'No', 'Do you want to save the data to a file?')

        self.history_tasks = QTextEdit('')  # create window to display history of tasks
        self.history_tasks.setReadOnly(True)
        self.history_tasks.setLineWrapMode(QTextEdit.WidgetWidth)
        self.history_tasks.setToolTip('''<center>Display the history of the tasks</center>''')

        self.buttons = QHBoxLayout()
        self.btn_start = Button("Start")
        self.btn_start.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.btn_start.clicked.connect(self.clc_btn_start)
        # ---
        self.btn_pause = Button("Pause")
        self.btn_pause.setStyleSheet("background-color: rgb(255, 255, 0)")
        self.btn_pause.setEnabled(False)
        self.btn_pause.clicked.connect(self.clc_btn_pause)
        # ---
        self.btn_stop = Button("Stop")
        self.btn_stop.setStyleSheet("background-color: rgb(255, 0, 0)")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.clc_btn_stop)
        # ---
        self.buttons.addWidget(self.btn_start)
        self.buttons.addWidget(self.btn_pause)
        self.buttons.addWidget(self.btn_stop)

        self.task = QHBoxLayout()
        self.label_task = QLabel('Enter the name of the task: ')
        self.text_task = QLineEdit()
        self.task.addWidget(self.label_task)
        self.task.addWidget(self.text_task)

        self.main_box.addWidget(self.history_tasks, QtCore.Qt.AlignBottom)
        self.main_box.addLayout(self.buttons, QtCore.Qt.AlignBottom)
        self.main_box.addLayout(self.task, QtCore.Qt.AlignBottom)

        self.move_center_display()

        self.run_questions()

    def make_a_time_stamp(self):
        mark_time = time.time()
        struct = time.localtime(mark_time)
        output_mark_time = time.strftime('%d.%m.%Y %H:%M', struct)
        self.time_spent_task.append(mark_time)
        return output_mark_time

    @QtCore.pyqtSlot()
    def clc_btn_start(self):
        self.last_pressed_btn = 'Start'

        start_task = self.make_a_time_stamp()

        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)

        task = self.text_task.text()
        self.text_task.setReadOnly(True)

        name_task = f'\nTask: {task}\n\n' if task else f'Task: # ---\n\n'
        self.history.append(name_task)

        start_text = f'Start: {start_task}\n'
        self.history.append(start_text)
        self.history_tasks.setText(''.join(self.history))

        if self.path_file:
            with open(self.path_file, 'a+') as file:
                file.write(name_task)
                file.write(start_text)

    @QtCore.pyqtSlot()
    def clc_btn_pause(self):
        self.last_pressed_btn = 'Pause'

        pause_task = self.make_a_time_stamp()

        head = 'Pause/Stop' if len(self.history) % 2 == 0 else 'Pause/Start'
        pause_text = f'{head}: {pause_task}\n'
        self.history.append(pause_text)
        self.history_tasks.setText(''.join(self.history))

        if self.path_file:
            with open(self.path_file, 'a+') as file:
                file.write(pause_text)

    @QtCore.pyqtSlot()
    def clc_btn_stop(self):
        self.last_pressed_btn = 'Stop'

        stop_task = self.make_a_time_stamp()

        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)

        self.text_task.setReadOnly(False)
        self.text_task.clear()
        stop_text = f'Stop: {stop_task}\n\n'
        self.history.append(stop_text)

        if len(self.time_spent_task) % 2 != 0:
            self.time_spent_task = self.time_spent_task[:-1]

        all_time_task_seconds = sum([i - j for i, j in zip(self.time_spent_task[-1::-2], self.time_spent_task[-2::-2])])
        hours = round(all_time_task_seconds // 3600)
        minutes = round((all_time_task_seconds - hours * 3600) // 60)
        seconds = round(all_time_task_seconds - hours * 3600 - minutes * 60, 2)
        all_time_text = f'The task took: {hours=} {minutes=} {seconds=}\n\n'
        self.history.append(all_time_text)
        self.history_tasks.setText(''.join(self.history))

        if self.path_file:
            with open(self.path_file, 'a+') as file:
                file.write(stop_text)
                file.write(all_time_text)

        self.time_spent_task = []

    def event(self, e):

        """creating the ability to press all buttons using the keyboard"""

        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() in (16777221, 16777220):  # =, Enter
                self.clc_btn_start()

        elif e.type() == QtCore.QEvent.Close:
            if self.last_pressed_btn != 'Stop':
                self.clc_btn_stop()

            self.setVisible(False)
            message = '<center>Goodbye!</center>\n'
            if self.path_file:
                message += f'<center>The data is saved at: {self.path_file}</center>'
            last_window = QMessageBox(QMessageBox.NoIcon, f'{" " * 10}TimeManager{" " * 10}',
                                      message, buttons=QMessageBox.NoButton, parent=self)
            last_window.exec_()
        return QWidget.event(self, e)  # send farther

    def run_questions(self):
        self.question.show()
        # answers_to_questions
        while True:
            if self.question.check_value is not None:
                self.answers_to_questions()
                break

            qApp.processEvents()  # Starting the cycle rotation

    def answers_to_questions(self):
        while True:
            if self.question.check_value == 'Yes':
                self.question.rbtn_1.setText('Create file')
                self.question.rbtn_2.setText('Select file')
                self.question.group_box.setTitle('Do you want to create or select a file?')
                self.question.label.setText('<center>The file extension must be .txt or .doc</center>')

            elif self.question.check_value in ('No', 'Create file', 'Select file'):

                self.question.close()

                if self.question.check_value == 'Create file':
                    self.path_file = QFileDialog.getSaveFileName(filter="*.doc *.txt")[0]
                    if not (self.path_file.endswith('.doc') or self.path_file.endswith('.txt')):
                        separator = '/'

                        path = self.path_file.split(separator)[:-1]
                        path = separator.join(path)

                        name_file = NamedFile()
                        # a loop is created to get the name of the created file
                        while True:
                            if name_file.valid_file_name:
                                self.path_file = f'{path}{separator}{name_file.valid_file_name}.doc'
                                break

                            qApp.processEvents()  # Starting the cycle rotation

                elif self.question.check_value == 'Select file':
                    self.path_file = QFileDialog.getOpenFileName(filter="Files (*.doc *.txt)")[0]

                self.show()  # display time manager window
                break

            qApp.processEvents()  # Starting the cycle rotation


if __name__ == "__main__":
    app = QApplication([])
    time_manager = TimeManager()
    sys.exit(app.exec_())
