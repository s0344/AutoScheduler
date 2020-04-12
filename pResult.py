from PyQt5 import QtGui
from PyQt5.QtCore import Qt
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

        # Spacer
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Button
        self.previous = QPushButton("Previous", self.widget)
        self.previous.setFont(self.font)
        self.buttonSort = QPushButton("Sort")
        self.buttonSort.setFont(self.font)

        """
        Layout
        """
        # Vertical layout 1
        self.vl1 = QVBoxLayout()
        self.vl1.addWidget(self.label)
        # Overall layout
        self.layout.addLayout(self.vl1)
        self.layout.addSpacerItem(self.spacer1)
        self.layout.addWidget(self.previous)
        self.layout.addWidget(self.buttonSort)


class Dialog_sort(QDialog):
    def __init__(self, gui):
        super(Dialog_sort, self).__init__()
        self.gui = gui
        self.setWindowTitle("Priority setting")
        self.setWindowIcon(QtGui.QIcon("pictures/prgmIcon.png"))
        self.setAttribute(Qt.WA_DeleteOnClose)

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
        self.listFont.setPointSize(10)
        self.listFont.setBold(True)
        self.listFont.setWeight(75)

        self.setFont(self.font)
        self.stl = QStackedLayout(self)

        self.lb1 = QLabel("Select preference that you interested in: ")
        self.lb1.setFont(self.fontB)
        self.lb2 = QLabel("Sort the priority of preference: ")
        self.lb2.setFont(self.fontB)
        self.chkbox1 = self.checkBox('School Day', Qt.Checked)
        self.chkbox2 = self.checkBox('Length of Class', Qt.Checked)
        self.chkbox3 = self.checkBox('Start Time', Qt.Checked)
        self.chkbox4 = self.checkBox('End Time', Qt.Checked)
        self.chkbox5 = self.checkBox('Instructor', Qt.Checked)
        self.buttonNext = QPushButton("Next")
        self.buttonChange = QPushButton("Change")

        self.widget1 = QWidget()
        self.vl1 = QVBoxLayout(self.widget1)
        self.vl1.addWidget(self.lb1)
        self.vl1.addWidget(self.chkbox1)
        self.vl1.addWidget(self.chkbox2)
        self.vl1.addWidget(self.chkbox3)
        self.vl1.addWidget(self.chkbox4)
        self.vl1.addWidget(self.chkbox5)
        self.vl1.addWidget(self.buttonNext)

        self.stl.addWidget(self.widget1)

        self.priority = []

        self.buttonNext.clicked.connect(lambda: self.click_next())

    def click_next(self):
        if self.chkbox1.checkState() == Qt.Checked:
            self.priority.append('School Day')
        if self.chkbox2.checkState() == Qt.Checked:
            self.priority.append('Length of Class')
        if self.chkbox3.checkState() == Qt.Checked:
            self.priority.append('Start Time')
        if self.chkbox4.checkState() == Qt.Checked:
            self.priority.append('End Time')
        if self.chkbox5.checkState() == Qt.Checked:
            self.priority.append('Instructor')

        self.priorityList = MainForm(self.priority)
        self.priorityList.setMaximumWidth(180)
        self.priorityList.view.setFont(self.listFont)

        self.widget2 = QWidget()
        self.vl2 = QVBoxLayout(self.widget2)
        self.vl2.addWidget(self.lb2)
        self.vl2.addWidget(self.priorityList)
        self.vl2.addWidget(self.buttonChange)
        self.stl.addWidget(self.widget2)
        self.stl.setCurrentIndex(1)

        self.buttonChange.clicked.connect(lambda: self.passPriority())

    def passPriority(self):
        self.gui.guiData.setPriority(self.priorityList.nodes)
        self.close()
        self.gui.result.rank(self.guiData)
        # self.reorderResult

    def checkBox(self, text, default):
        checkBox = QCheckBox()
        checkBox.setText(text)
        checkBox.setChecked(default)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setMaximumHeight(100)
        return checkBox
