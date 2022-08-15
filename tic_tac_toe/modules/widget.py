import numpy as np

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QGridLayout, QMessageBox

from modules.cell import Cell


class Widget(QWidget):
    """implements the playing field"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.count = 0
        self.grid_values = np.zeros(9)
        self.game_over = False

        main_box = QVBoxLayout()

        frame = QFrame()
        frame.setStyleSheet("background-color:#9AA6A7;border:1px solid #9AA6A7;")

        grid = QGridLayout()
        grid.setSpacing(0)

        id_color = (1, 3, 5, 7)

        # array of application field cells
        self.cells = [Cell(i, Cell.color_grey if i in id_color else Cell.color_orange) for i in range(0, 9)]
        self.id_cell_in_focus = 0

        i = 0
        for j in range(0, 3):
            for k in range(0, 3):
                grid.addWidget(self.cells[i], j, k)
                i += 1

        for cell in self.cells:
            cell.changeCellFocus.connect(self.one_step_game)

        frame.setLayout(grid)
        main_box.addWidget(frame, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(main_box)

    def one_step_game(self, id):
        """when the cell is activated, one step of the game starts"""
        if not (id < 0 or id > 8) and not self.game_over:
            self.cells[self.id_cell_in_focus].clear_cell_focus()
            self.id_cell_in_focus = id
            self.cells[id].set_cell_focus()

            self.input_value(id)
            self.get_result_game()

    def input_value(self, id):
        """enter a value in a cell"""
        if self.cells[id].is_cell_change:
            if self.count % 2 == 0:
                self.cells[id].setText('X')
                self.grid_values[id] = 1
            else:
                self.cells[id].setText('O')
                self.grid_values[id] = -1
            self.cells[id].set_cell_block()
            self.count += 1

    def get_result_game(self):
        """checking the current state of the game"""
        for seq in ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                    (0, 3, 6), (1, 4, 7), (2, 5, 8),
                    (0, 4, 8), (2, 4, 6)):
            summa = self.grid_values[[seq]].sum()
            if summa in (3, -3):
                symbol = '̶X̶' if summa == 3 else '̶O̶'
                for i in seq:
                    self.cells[i].set_finish_symbol(symbol)
                self.game_over = True

        if not self.game_over:
            if not np.any(self.grid_values == 0):
                self.cells[self.id_cell_in_focus].clear_cell_focus()
                self.change_color_all_cells_red()
                self.game_over = True

    def keyPressEvent(self, evt):
        key = evt.key()
        if key == QtCore.Qt.Key_1:
            self.one_step_game(6)
        elif key == QtCore.Qt.Key_2:
            self.one_step_game(7)
        elif key == QtCore.Qt.Key_3:
            self.one_step_game(8)
        elif key == QtCore.Qt.Key_4:
            self.one_step_game(3)
        elif key == QtCore.Qt.Key_5:
            self.one_step_game(4)
        elif key == QtCore.Qt.Key_6:
            self.one_step_game(5)
        elif key == QtCore.Qt.Key_7:
            self.one_step_game(0)
        elif key == QtCore.Qt.Key_8:
            self.one_step_game(1)
        elif key == QtCore.Qt.Key_9:
            self.one_step_game(2)

        QWidget.keyPressEvent(self, evt)

    def clear_all_cells(self):
        for cell in self.cells:
            cell.setText("")
            cell.clear_cell_block()

    def clear_focus_all_cells(self):
        for cell in self.cells:
            cell.clear_cell_focus()

    def change_color_all_cells_red(self):
        for cell in self.cells:
            cell.set_cell_change_color_red()

    def change_color_all_cells_black(self):
        for cell in self.cells:
            cell.set_cell_change_color_black()

    def start_new_game(self):
        self.clear_all_cells()
        self.clear_focus_all_cells()
        self.change_color_all_cells_black()

        self.count = 0
        self.grid_values = np.zeros(9)
        self.game_over = False

