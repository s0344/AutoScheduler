from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow


class PanelResult(QMainWindow):
    def __init__(self):
        super(PanelResult, self).__init__()
        self.setGeometry(0, 0, 850, 650)