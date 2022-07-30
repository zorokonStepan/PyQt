# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from math import sqrt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QGridLayout, QLabel
from PyQt5 import QtCore
from functools import partial


class Button(QPushButton):
    def __init__(self, name):
        QPushButton.__init__(self, name)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(size.width() - 25)
        return size


class Calculator(QWidget):
    """A desktop calculator."""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)  # create window
        self.setWindowTitle('Calculator')
        self.setMaximumWidth(700)
        self.move(self.width() * -2, 0)  # we will display the window outside the screen

        self.expression = '0'
        self.history = ['']

        self.main_box = QVBoxLayout()
        self.buttons = QGridLayout()

        # create buttons
        self.btn_7 = Button("7")
        self.btn_8 = Button("8")
        self.btn_9 = Button("9")
        self.btn_back = Button("⟻")
        self.btn_clear = Button("C")
        self.btn_clear_history = Button("CA")

        self.btn_4 = Button("4")
        self.btn_5 = Button("5")
        self.btn_6 = Button("6")
        self.btn_sh = Button("÷")
        self.btn_mul = Button("x")
        self.btn_sub = Button("-")

        self.btn_1 = Button("1")
        self.btn_2 = Button("2")
        self.btn_3 = Button("3")
        self.btn_open_br = Button("(")
        self.btn_close_br = Button(")")
        self.btn_add = Button("+")

        self.btn_0 = Button("0")
        self.btn_point = Button(".")
        self.btn_div = Button("div")
        self.btn_mod = Button("mod")
        self.btn_round = Button("round")

        self.btn_result = Button("=")
        self.btn_sqrt_2 = Button("√")
        self.btn_pow_2 = Button("x²")
        self.btn_pow = Button("xⁿ")

        self.set_functionality_buttons()

        self.history_screen = QLabel()  # create window to display history of operation
        self.history_screen.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.history_screen.setMaximumWidth(700)
        self.history_screen.setToolTip('''<center>Display the history of the operation</center>''')

        self.error_screen = QLabel()  # create window to display errors
        self.error_screen.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.error_screen.setMaximumHeight(30)
        self.error_screen.setToolTip('''<center>Display errors of the operation</center>''')

        self.lcd = QLineEdit('0')  # create a window to display the input data
        self.lcd.setReadOnly(True)
        self.lcd.setAlignment(QtCore.Qt.AlignRight)
        self.lcd.setMinimumHeight(30)

        self.main_box.addWidget(self.history_screen)
        self.main_box.addWidget(self.error_screen)
        self.main_box.addWidget(self.lcd)
        self.main_box.addLayout(self.buttons)
        self.setLayout(self.main_box)

        self.show()

        # let's display a window in the center of the screen:
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()) // 2
        self.move(x, y)

    def set_functionality_buttons(self):
        # button layout
        self.buttons.addWidget(self.btn_7, 0, 0)
        self.buttons.addWidget(self.btn_8, 0, 1)
        self.buttons.addWidget(self.btn_9, 0, 2)
        self.buttons.addWidget(self.btn_back, 0, 3)
        self.buttons.addWidget(self.btn_clear, 0, 4)
        self.buttons.addWidget(self.btn_clear_history, 0, 5)

        self.buttons.addWidget(self.btn_4, 1, 0)
        self.buttons.addWidget(self.btn_5, 1, 1)
        self.buttons.addWidget(self.btn_6, 1, 2)
        self.buttons.addWidget(self.btn_sh, 1, 3)
        self.buttons.addWidget(self.btn_mul, 1, 4)
        self.buttons.addWidget(self.btn_sub, 1, 5)

        self.buttons.addWidget(self.btn_1, 2, 0)
        self.buttons.addWidget(self.btn_2, 2, 1)
        self.buttons.addWidget(self.btn_3, 2, 2)
        self.buttons.addWidget(self.btn_open_br, 2, 3)
        self.buttons.addWidget(self.btn_close_br, 2, 4)
        self.buttons.addWidget(self.btn_add, 2, 5)

        self.buttons.addWidget(self.btn_0, 3, 0, 1, 2)
        self.buttons.addWidget(self.btn_point, 3, 2)
        self.buttons.addWidget(self.btn_div, 3, 3)
        self.buttons.addWidget(self.btn_mod, 3, 4)
        self.buttons.addWidget(self.btn_round, 3, 5)

        self.buttons.addWidget(self.btn_result, 4, 0, 1, 3)
        self.buttons.addWidget(self.btn_sqrt_2, 4, 3)
        self.buttons.addWidget(self.btn_pow_2, 4, 4)
        self.buttons.addWidget(self.btn_pow, 4, 5)

        # assignment for handler buttons
        btn_number = (self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
                      self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9)
        btn_del = (self.btn_back, self.btn_clear, self.btn_clear_history)

        for btn in btn_number:
            btn.clicked.connect(partial(self.set_number, btn))

        for btn in btn_del:
            btn.clicked.connect(partial(self.del_value, btn))

        for btn in (self.btn_add, self.btn_sub):
            btn.clicked.connect(partial(self.clc_btn_add_sub, btn))

        for btn in (self.btn_mul, self.btn_sh, self.btn_div, self.btn_mod):
            btn.clicked.connect(partial(self.clc_btn_mul_sh_div_mod, btn))

        for btn in (self.btn_pow_2, self.btn_pow):
            btn.clicked.connect(partial(self.clc_btn_pow2_and_pow_any, btn))

        self.btn_sqrt_2.clicked.connect(partial(self.clc_btn_sqrt_2, self.btn_sqrt_2))
        self.btn_round.clicked.connect(self.clc_btn_round)
        self.btn_point.clicked.connect(self.clc_btn_point)
        self.btn_open_br.clicked.connect(self.clc_btn_open_br)
        self.btn_close_br.clicked.connect(self.clc_btn_close_br)
        self.btn_result.clicked.connect(self.clc_btn_result)

        # tooltips for any buttons
        self.btn_back.setToolTip('''<center>[Backspace].\n
                                          (it will work after pressing any button with the mouse)]</center>''')
        self.btn_clear.setToolTip('''<center>[Delete].\n
                                          (it will work after pressing any button with the mouse)]</center>''')
        self.btn_clear_history.setToolTip('''<center>[End.\n
                                          (it will work after pressing any button with the mouse)]</center>''')

        self.btn_sh.setToolTip('<center>[/]</center>')
        self.btn_mul.setToolTip('<center>[*]</center>')

        self.btn_div.setToolTip('<center>[shift !]</center>')
        self.btn_mod.setToolTip('<center>[shift @]</center>')
        self.btn_round.setToolTip('<center>[shift %]</center>')

        self.btn_result.setToolTip('<center>[= or Enter]</center>')
        self.btn_sqrt_2.setToolTip('<center>[shift $]</center>')
        self.btn_pow_2.setToolTip('<center>[shift #]</center>')
        self.btn_pow.setToolTip('<center>[shift ^]</center>')

    def event(self, e):
        # creating the ability to press all buttons using the keyboard
        if e.type() == QtCore.QEvent.KeyPress:
            if e.text() == '0':
                self.set_number(self.btn_0)
            elif e.text() == '1':
                self.set_number(self.btn_1)
            elif e.text() == '2':
                self.set_number(self.btn_2)
            elif e.text() == '3':
                self.set_number(self.btn_3)
            elif e.text() == '4':
                self.set_number(self.btn_4)
            elif e.text() == '5':
                self.set_number(self.btn_5)
            elif e.text() == '6':
                self.set_number(self.btn_6)
            elif e.text() == '7':
                self.set_number(self.btn_7)
            elif e.text() == '8':
                self.set_number(self.btn_8)
            elif e.text() == '9':
                self.set_number(self.btn_9)

            elif e.key() == 16777219:  # ⟻ == Button Backspace
                self.del_value(self.btn_back)
            elif e.key() == 16777223:  # C == Delete
                self.del_value(self.btn_clear)
            elif e.key() == 16777233:  # CA == End
                self.del_value(self.btn_clear_history)

            elif e.key() == 43 or e.text() == '+':  # +
                self.clc_btn_add_sub(self.btn_add)
            elif e.key() == 45 or e.text() == '-':  # -
                self.clc_btn_add_sub(self.btn_sub)

            elif e.key() == 42 or e.text() == '*':  # * or [shift 8and*]
                self.clc_btn_mul_sh_div_mod(self.btn_mul)
            elif e.key() == 47 or e.text() == '/':  # /
                self.clc_btn_mul_sh_div_mod(self.btn_sh)
            elif e.key() == 33 or e.text() == '!':  # div [shift 1and!]
                self.clc_btn_mul_sh_div_mod(self.btn_div)
            elif e.key() == 64 or e.text() == '@':  # mod [shift 2and@]
                self.clc_btn_mul_sh_div_mod(self.btn_mod)
            elif e.key() == 37 or e.text() == '%':  # % [shift 5and%]
                self.clc_btn_round()

            elif e.key() == 94 or e.text() == '^':  # ^ [shift 6and^]
                self.clc_btn_pow2_and_pow_any(self.btn_pow)
            elif e.key() == 35 or e.text() == '#':  # ² [shift 3and#]
                self.clc_btn_pow2_and_pow_any(self.btn_pow_2)
            elif e.key() == 36 or e.text() == '$':  # √ [shift 4and$]
                self.clc_btn_sqrt_2(self.btn_sqrt_2)

            elif e.key() == 46 or e.text() == '.':  # .
                self.clc_btn_point()
            elif e.key() == 40 or e.text() == '(':  # ( [shift 9and(]
                self.clc_btn_open_br()
            elif e.key() == 41 or e.text() == ')':  # ) [shift 0and)]
                self.clc_btn_close_br()

            elif e.key() in (61, 16777221, 16777220) or e.text() in ('=', r'\r'):  # =, Enter
                self.clc_btn_result()

        return QWidget.event(self, e)  # send farther

    def show_expression(self):
        self.lcd.setText(self.expression)
        self.history[-1] = self.expression
        self.history_screen.setText('\n'.join(self.history))
        self.error_screen.setText('')

    @QtCore.pyqtSlot()
    def set_number(self, btn):
        value = btn.text()

        if self.expression == '0':
            self.expression = value
        else:
            if self.expression[-1] not in ('²', ')'):
                self.expression += value

        self.show_expression()

    @QtCore.pyqtSlot()
    def del_value(self, btn):
        value = btn.text()

        if value == '⟻':
            if len(self.expression) == 1:
                self.expression = '0'
            elif self.expression.endswith('√('):
                if len(self.expression) == 2:
                    self.expression = '0'
                else:
                    self.expression = self.expression[:-2]
            elif self.expression.endswith('div') or self.expression.endswith('mod'):
                if len(self.expression) == 3:
                    self.expression = '0'
                else:
                    self.expression = self.expression[:-3]
            elif len(self.expression) > 1:
                self.expression = self.expression[:-1]

        elif value == 'C':
            self.expression = '0'

        elif value == 'CA':
            self.expression = '0'
            self.history = [self.expression]

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_add_sub(self, btn):
        value = btn.text()

        if self.expression == '0':
            self.expression = value
        else:
            if self.expression[-1].isdigit() or self.expression[-1] in ('x', '÷', '√', '²', '^', '(', ')', 'v', 'd'):
                self.expression += value
            elif self.expression[-1] == '.':
                self.expression += f'0{value}'
            elif self.expression[-1] in ('+', '-'):
                self.expression = self.expression[:-1] + value

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_point(self):
        list_of_digit = []
        for i in self.expression[::-1]:
            if i.isdigit() or i == '.':
                list_of_digit.append(i)
            else:
                break

        if not list_of_digit:
            self.expression += '0.'
        else:
            if '.' not in list_of_digit:
                self.expression += '.'

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_mul_sh_div_mod(self, btn):
        value = btn.text()

        if self.expression[-1] == '.':
            self.expression += f'0{value}'
        else:
            if self.expression[-1] not in ('^', 'x', '÷', '√', '(', '+', '-', 'v', 'd'):
                self.expression += value

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_round(self):
        expression = []
        for i in self.expression[::-1]:
            if i.isdigit() or i == '.':
                if i.isdigit():
                    expression.append(i)
                elif i == '.':
                    expression.append(i)
                    break
            else:
                break
        if expression and '.' in expression:
            ind = len(expression)
            self.expression = self.expression[:-ind]

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_sqrt_2(self, btn):
        value = f'{btn.text()}('

        if self.expression[-1] == '0':
            self.expression = value
        else:
            if not self.expression[-1].isdigit() and self.expression[-1] not in ('²', ')', '.'):
                self.expression += value

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_pow2_and_pow_any(self, btn):
        value = '²' if btn.text() == 'x²' else '^'

        if self.expression[-1].isdigit() or self.expression[-1] in (')', '²'):
            self.expression += value
        elif self.expression[-1] == '.':
            self.expression += f'0{value}'

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_open_br(self):
        if self.expression == '0':
            self.expression = '('
        else:
            if self.expression[-1] in ('+', '-', 'x', '÷', 'v', 'd', '√', '^', '('):
                self.expression += '('

        self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_close_br(self):
        parenthesis = [i for i in self.expression if i in ('(', ')')]
        if (parenthesis.count('(') - parenthesis.count(')')) > 0:
            if self.expression[-1] == '.':
                self.expression += '0)'
            elif self.expression[-1].isdigit() or self.expression[-1] in ('²', ')'):
                self.expression += ')'

            self.show_expression()

    @QtCore.pyqtSlot()
    def clc_btn_result(self):
        parenthesis = [i for i in self.expression if i in ('(', ')')]
        if (parenthesis.count('(') - parenthesis.count(')')) == 0:
            expression = self.expression
            expression = expression.replace('x', '*')
            expression = expression.replace('÷', '/')
            expression = expression.replace('div', '//')
            expression = expression.replace('mod', '%')
            expression = expression.replace('²', '**2')
            expression = expression.replace('^', '**')
            expression = expression.replace('√', 'sqrt')

            try:
                result = round(eval(expression), 5)
            except ZeroDivisionError:
                self.error_screen.setText("You can't divide by zero")
            except Exception:
                self.error_screen.setText("Error")
            else:
                result = str(result)
                self.lcd.setText(result)
                self.history[-1] = f'{self.expression} = {result}'
                self.history.append('')
                self.history_screen.setText('\n'.join(self.history))
                self.expression = result
        else:
            self.error_screen.setText('Incorrect number of parenthesis')


if __name__ == "__main__":
    app = QApplication([])
    calculator = Calculator()
    sys.exit(app.exec_())
