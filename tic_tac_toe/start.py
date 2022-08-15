from PyQt5 import QtGui, QtWidgets
import sys
from modules.main_window import MainWindow

app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(r"images/svd.png"))
window = MainWindow()
window.show()
sys.exit(app.exec_())
