from PyQt5.QtWidgets import *

# Source: https://github.com/d1vanov/PyQt5-reorderable-list-model/blob/master/reorderable_list_model.py
from reorderableList import *


class PanelPriority(QMainWindow):
    def __init__(self):
        super(PanelPriority, self).__init__()
        self.widget = QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 850, 650))
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)  # Overall vertical layout
        self.layout.setSpacing(15)

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
        nodes = ['Instructor', 'School Day', 'Start Time', 'End Time', 'Length of Class']
        self.priorityList = MainForm(nodes)
        self.priorityList.show()
        self.priorityList.view.setFont(self.listFont)
        # Spacer
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Previous Button
        self.previous = QPushButton("Previous", self.widget)
        self.previous.setFont(self.font)
        # Submit Button
        self.submit = QPushButton("Submit", self.widget)
        self.submit.setFont(self.fontB)

        """
        Layout
        """
        # Horizontal layout 1
        self.hl1 = QHBoxLayout(self.widget)
        self.hl1.addItem(self.spacer1)
        self.hl1.addWidget(self.priorityList)
        self.hl1.addItem(self.spacer2)
        # Horizontal layout 2
        self.hl2 = QHBoxLayout(self.widget)
        self.hl2.addItem(self.spacer3)
        self.hl2.addWidget(self.previous)
        self.hl2.addWidget(self.submit)
        # Overall layout
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.hl1)
        self.layout.addLayout(self.hl2)

