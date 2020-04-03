from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from reorderableList import MainForm

class PanelResult(QMainWindow):
    def __init__(self):
        super(PanelResult, self).__init__()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QHBoxLayout(self.widget)  # Overall horizontal layout

        # Font
        self.fontB = QtGui.QFont()
        self.fontB.setFamily("Arial")
        self.fontB.setPointSize(9)
        self.fontB.setBold(True)
        self.fontB.setWeight(75)

        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(9)
        self.font.setBold(False)

        self.listFont = QtGui.QFont()
        self.listFont.setFamily("Arial")
        self.listFont.setPointSize(12)
        self.listFont.setBold(True)
        self.listFont.setWeight(75)

        """
        Widgets
        """
        # Label
        self.label = QLabel("Explanation: ....")
        self.label.setFont(self.listFont)
        # Priority List
        defaultPriority = ['School Day', 'Length of Class', 'Start Time', 'End Time', 'Instructor']
        self.priorityList = MainForm(defaultPriority)
        self.priorityList.setMaximumWidth(180)
        self.priorityList.show()
        self.priorityList.view.setFont(self.listFont)
        # Spacer
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Change Button
        self.change = QPushButton("Change Priority", self.widget)
        self.change.setFont(self.fontB)
        # Previous Button
        self.previous = QPushButton("Previous", self.widget)
        self.previous.setFont(self.font)

        """
        Layout
        """
        # Vertical layout 1
        self.vl1 = QVBoxLayout()
        self.vl1.addWidget(self.label)
        self.vl1.addWidget(self.priorityList)
        self.vl1.addWidget(self.change)
        # Overall layout
        self.layout.addLayout(self.vl1)
        self.layout.addSpacerItem(self.spacer1)
        self.layout.addWidget(self.previous)