import copy
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QEvent
from functools import partial

"""
THE TOWER OF HANOI.
Move the tower of disks, one disk at a time, to another tower.
Larger disks cannot rest on top of a smaller disk.

The more disks, the more difficult the puzzle is.
Initially, all disks are on rod A
    
The game can be played by pressing the buttons, and the buttons back, up, forward.
"""


class Button(QPushButton):
    def __init__(self, text: str):
        QPushButton.__init__(self, text)
        self.setAutoDefault(True)  # you can press the Enter button


class HanoiTower(QWidget):

    """implementation of the Hanoi Tower game"""

    def __init__(self, total_disks: int = 5, parent=None):
        QWidget.__init__(self, parent)  # create window
        self.setWindowTitle("Hanoi Tower")
        self.resize(400, 300)

        self.number_of_moves = 0
        self.total_disks = total_disks  # the number of disks used in the puzzle
        self.solved_tower = list(range(self.total_disks, 0, -1))  # sample solution
        self.towers = {"A": copy.deepcopy(self.solved_tower), "B": [], "C": []}  # Initially, all disks are on rod A
        self.from_tower = ''
        self.to_tower = ''

        self.btn_a = Button('A')
        self.btn_b = Button('B')
        self.btn_c = Button('C')
        self.btn_a.clicked.connect(partial(self.push_btn_abc, self.btn_a, self.btn_b, self.btn_c, "A"))
        self.btn_b.clicked.connect(partial(self.push_btn_abc, self.btn_b, self.btn_a, self.btn_c, "B"))
        self.btn_c.clicked.connect(partial(self.push_btn_abc, self.btn_c, self.btn_a, self.btn_b, "C"))
        self.buttons_box = QHBoxLayout()
        self.buttons_box.addWidget(self.btn_a)
        self.buttons_box.addWidget(self.btn_b)
        self.buttons_box.addWidget(self.btn_c)

        self.main_box = QVBoxLayout()

        self.setToolTip('''<center>Move the tower of disks, one disk at a time, to another tower.</center>\n
        <center>Larger disks cannot rest on top of a smaller disk.</center>''')

        self.show_number_of_moves = QLabel('''<center>number of moves = 0</center>''')
        self.messages = QLabel('''<center>...</center>''')

        self.playing_field_a = QLabel("")
        self.playing_field_b = QLabel("")
        self.playing_field_c = QLabel("")
        self.playing_field_box = QHBoxLayout()
        self.playing_field_box.addWidget(self.playing_field_a)
        self.playing_field_box.addWidget(self.playing_field_b)
        self.playing_field_box.addWidget(self.playing_field_c)

        self.main_box.addWidget(self.show_number_of_moves)
        self.main_box.addLayout(self.playing_field_box)
        self.main_box.addWidget(self.messages)
        self.main_box.addLayout(self.buttons_box)

        self.setLayout(self.main_box)

        self.display_towers()
        self.show()

    def push_btn_abc(self, btn_1, btn_2, btn_3, letter):
        """processing the button click event"""
        btn_1.setEnabled(False)
        if btn_2.isEnabled() and btn_3.isEnabled():
            self.from_tower = letter
        elif btn_2.isEnabled() or btn_3.isEnabled():
            self.to_tower = letter
            btn_2.setEnabled(False)
            btn_3.setEnabled(False)
            self.is_valid_move()

    def set_enabled_true_abc(self):
        """make all buttons active"""
        self.btn_a.setEnabled(True)
        self.btn_b.setEnabled(True)
        self.btn_c.setEnabled(True)

    def set_enabled_false_abc(self):
        """make all buttons inactive"""
        self.btn_a.setEnabled(False)
        self.btn_b.setEnabled(False)
        self.btn_c.setEnabled(False)

    def event(self, e):
        """redefining the event method for pressing the A, B, C buttons on the keyboard back, up and forward"""
        if e.type() == QEvent.KeyPress:
            if e.key() == 16777234:
                self.push_btn_abc(self.btn_a, self.btn_b, self.btn_c, "A")
            elif e.key() == 16777235:
                self.push_btn_abc(self.btn_b, self.btn_a, self.btn_c, "B")
            elif e.key() == 16777236:
                self.push_btn_abc(self.btn_c, self.btn_a, self.btn_b, "C")
        return QWidget.event(self, e)  # send farther

    def is_valid_move(self):
        """valid combination check"""
        if len(self.towers[self.from_tower]) == 0:
            # The Tower from Tower cannot be empty:
            self.messages.setText("<center>You selected a tower with no disks.</center>")
            self.set_enabled_true_abc()  # Request a move again.
        elif len(self.towers[self.to_tower]) == 0:
            # Any disk can be moved to an empty tower:
            self.messages.setText("<center>...</center>")
            self.run()
        elif self.towers[self.to_tower][-1] < self.towers[self.from_tower][-1]:
            self.messages.setText("<center>Can't put larger disks on top of smaller ones.</center>")
            self.set_enabled_true_abc()  # Request a move again.
        else:
            self.messages.setText("<center>...</center>")
            self.run()

    def display_disk(self, width):
        """Outputs a disk of the specified width. Width 0 means no disk."""
        if width == 0:
            # Output a rod segment without a disk:
            return "<center>||</center>\n"
        else:
            # Output disk:
            disk = "@" * width
            width = str(width)
            return f"<center>{disk}{width}||{width}{disk}</center>"

    def display_tower(self, playing_field, letter):
        """Outputs one tower with disks."""
        image = """"""
        # Bring out three towers:
        for level in range(self.total_disks, -1, -1):
            if level >= len(self.towers[letter]):
                image += self.display_disk(0)  # Output an empty rod without a disk.
            else:
                image += self.display_disk(self.towers[letter][level])  # Output the disk.

        image += f"<center>{letter}</center>"
        playing_field.setText(image)

    def display_towers(self):
        """Outputs three tower with disks."""
        self.display_tower(self.playing_field_a, "A")
        self.display_tower(self.playing_field_b, "B")
        self.display_tower(self.playing_field_c, "C")

    def run(self):
        """Conducts one game.

        The towers dictionary contains the keys "A", "B" и "C", and values is lists,
        representing a stack of disks. The list contains integers representing
        the disks are of different sizes, and the beginning of the list represents
        the bottom of the tower. For playing with 5 discs list [5, 4, 3, 2, 1]
        represents a filled tower. Empty the list [] list represents a tower without disks.
        In the list [1, 3] a larger disk located on a smaller disk, this configuration is
        not allowed. The list [3, 1] is acceptable, since smaller disks can be placed on larger ones."""

        self.number_of_moves += 1

        disk = self.towers[self.from_tower].pop()  # Move the top disk from fromTower to toTower
        self.towers[self.to_tower].append(disk)
        self.display_towers()  # Bring out towers and disks
        self.show_number_of_moves.setText(f"<center>Number of moves = {self.number_of_moves}</center>")
        self.set_enabled_true_abc()

        # Check if the puzzle is solved:
        if self.solved_tower in (self.towers["B"], self.towers["C"]):
            self.messages.setText("<center>You have solved the puzzle! Well done!</center>")
            self.set_enabled_false_abc()


if __name__ == "__main__":
    app_hanoi_tower = QApplication([])
    hanoi_tower = HanoiTower()
    sys.exit(app_hanoi_tower.exec_())
