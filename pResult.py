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

        self.dialog = None

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

        '''
        Widget in dialog 
        '''
        defaultPriority = ['School Day', 'Length of Class', 'Start Time', 'End Time', 'Instructor']
        self.priorityList = MainForm(defaultPriority)
        self.priorityList.setMaximumWidth(180)
        self.priorityList.view.setFont(self.listFont)
        self.buttonChange = QPushButton("Change")
        self.buttonChange.setFont(self.font)
        self.buttonNext = QPushButton("Next")
        self.chkbox1 = self.checkBox('School Day', Qt.Checked)
        self.chkbox2 = self.checkBox('Length of Class', Qt.Checked)
        self.chkbox3 = self.checkBox('Start Time', Qt.Checked)
        self.chkbox4 = self.checkBox('End Time', Qt.Checked)
        self.chkbox5 = self.checkBox('Instructor', Qt.Checked)


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

        '''
        Event
        '''
        self.buttonSort.clicked.connect(lambda: self.sort())
        self.buttonNext.clicked.connect(lambda: self.dialog.stl.setCurrentIndex(self.dialog.stl.currentIndex() + 1))

    def sort(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("AutoScheduler - Priority setting")
        self.dialog.setWindowIcon(QtGui.QIcon("pictures/prgmIcon.png"))
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.setFont(self.font)
        self.dialog.setContentsMargins(15, 15, 15, 10)
        stl = QStackedLayout(self.dialog)
        widget1 = QWidget(self.dialog)
        widget2 = QWidget(self.dialog)

        vl1 = QVBoxLayout(widget1)
        hl1 = QHBoxLayout()
        vl1.addWidget(self.chkbox1)
        vl1.addWidget(self.chkbox2)
        vl1.addWidget(self.chkbox3)
        vl1.addWidget(self.chkbox4)
        vl1.addWidget(self.chkbox5)
        hl1.addWidget(self.buttonNext)
        vl1.addLayout(hl1)

        vl2 = QVBoxLayout(widget2)
        hl2 = QHBoxLayout()
        vl2.addWidget(self.priorityList)
        hl2.addWidget(self.buttonChange)
        vl2.addLayout(hl2)

        stl.addWidget(widget1)
        stl.addWidget(widget2)

        self.dialog.exec()

    def click_next(self):
        priority = []
        if self.chkbox1 == Qt.Checked:
            priority.append('School Day')
        if self.chkbox2 == Qt.Checked:
            priority.append('Length of Class')
        if self.chkbox3 == Qt.Checked:
            priority.append('Start Time')
        if self.chkbox4 == Qt.Checked:
            priority.append('End Time')
        if self.chkbox5 == Qt.Checked:
            priority.append('Instructor')
        # self.priorityList.nodes = priority

        self.priorityList.show()


    def checkBox(self, text, default):
        checkBox = QCheckBox()
        checkBox.setText(text)
        checkBox.setChecked(default)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setMaximumHeight(100)
        return checkBox