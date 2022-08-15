from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QToolBar, QMainWindow, qApp

from modules.widget import Widget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Крестики-Нолики")
        icon = QtGui.QIcon(r"images/tic_tac_toe.png")
        self.setWindowIcon(icon)

        self.setStyleSheet(
            "QFrame QPushButton {font-size:10pt;font-family:Verdana;"
            "color:black;font-weight:bold;}"
            "Cell {font-size:14pt;font-family:Verdana;"
            "border:1px solid #9AA6A7;}")

        self.tic_tac = Widget()
        self.setCentralWidget(self.tic_tac)

        menuBar = self.menuBar()
        toolBar = QToolBar()

        myMenuFile = menuBar.addMenu("&Файл")

        action_new = myMenuFile.addAction(QtGui.QIcon(r"images/new.png"),
                                          "&Новый", self.tic_tac.start_new_game,
                                           QtCore.Qt.CTRL + QtCore.Qt.Key_N)

        action_quit = myMenuFile.addAction(QtGui.QIcon(r"images/close.png"),
                                           "&Выход", qApp.quit,
                                            QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        toolBar.addAction(action_new)
        action_new.setStatusTip("Начать сначала")
        myMenuFile.addSeparator()
        toolBar.addSeparator()
        toolBar.addAction(action_quit)
        action_quit.setStatusTip("Завершение работы приложения")

        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)

        statusBar = self.statusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.showMessage("\"Крестики-Нолики\" приветствует вас", 20000)
