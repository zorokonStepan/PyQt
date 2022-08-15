from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel


class Cell(QLabel):
    """implements one cell of the playing field"""

    color_yellow = "#FFFF90"
    color_orange = "#F5D8C1"
    color_grey = "#E8E8E8"
    color_black = "#000000"
    color_red = "#D77A38"
    # it will transmit to the handler the number of the cell on which the user clicked the mouse.
    changeCellFocus = QtCore.pyqtSignal(int)

    def __init__(self, id, bg_color, parent=None):
        QLabel.__init__(self, parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(100, 100)
        self.setMargin(0)
        self.setText("")
        if id < 0 or id > 8:
            id = 0
        self.id = id  # sequence number of the cell
        self.is_cell_change = True  # a value of True will indicate that the cell is unlocked
        self.font_color_current = self.color_black  # current text color: black or red
        self.bg_color_default = bg_color  # the background color set when creating the cell: orange or light gray
        self.bg_color_current = bg_color  # current background color: yellow, orange or light gray
        self.show_color_current()

    def mousePressEvent(self, evt):
        """mousePressEvent — this method should be redefined to be able to handle mouse clicks."""
        self.changeCellFocus.emit(self.id)
        QLabel.mousePressEvent(self, evt)

    def show_color_current(self):
        """sets the text and background colors for the cell,
        taken from the font_сolor_сurrent and bg_сolor_сurrent attributes"""
        self.setStyleSheet(f"background-color: {self.bg_color_current} ;color: {self.font_color_current};")

    def set_cell_focus(self):
        """will move the cell from an inactive state to an active one."""
        self.bg_color_current = self.color_yellow
        self.show_color_current()

    def clear_cell_focus(self):
        """will move the cell from the active state to the inactive state"""
        self.bg_color_current = self.bg_color_default
        self.show_color_current()

    def set_cell_block(self):
        """will transfer the cell from the unlocked state to the locked one."""
        self.is_cell_change = False

    def clear_cell_block(self):
        """will transfer the cell from the locked state to the unlocked one"""
        self.is_cell_change = True

    def set_cell_change_color_red(self):
        """will change the color of the cell label to red"""
        self.font_color_current = self.color_red
        self.show_color_current()

    def set_cell_change_color_black(self):
        """will change the color of the cell label to black"""
        self.font_color_current = self.color_black
        self.show_color_current()

    def set_finish_symbol(self, symbol):
        """if a winning combination is collected, it will replace
        the symbol in the desired cell with the crossed one"""
        self.setText(symbol)
        self.set_cell_change_color_red()
        self.set_cell_focus()
