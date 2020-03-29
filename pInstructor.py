from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from database.DB import *


class PanelInstructor(QMainWindow):
    """
    Draw "Instructor" panel
    """
    def __init__(self):
        super(PanelInstructor, self).__init__()
        self.widget = QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 850, 650))
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)  # Overall vertical layout
        self.layout.setSpacing(15)

        # Font
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(9)
        self.setFont(self.font)

        self.fontL = QtGui.QFont()
        self.fontL.setFamily("Arial")
        self.fontL.setPointSize(10)
        self.fontL.setBold(True)
        self.fontL.setWeight(75)

        """
        Widgets
        """
        # Label "Instructor Filter"
        self.title = QLabel("Instructor Filter", self.widget)
        self.title.setFont(self.fontL)
        # Instructor filter
        self.filter = QTreeWidget(self.widget)
        # Spacer
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Previous Button
        self.previous = QPushButton("Previous", self.widget)
        # Next Button
        self.next = QPushButton("Next", self.widget)

        """
        Layout
        """
        # Horizontal layout
        self.hl = QHBoxLayout(self.widget)
        self.hl.setContentsMargins(0, 0, 0, 0)
        self.hl.addItem(self.spacer)
        self.hl.addWidget(self.previous)
        self.hl.addWidget(self.next)
        # Overall layout
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.filter)
        self.layout.addLayout(self.hl)

    """
    Member functions
    """
    # update filter
    def filterEvent(self, panelCourse):

        self.filter.clear()

        self.filter.setHeaderLabel("Instructors by Course")
        self.db = DB()
        self.db.useDatabase()

        # Access the selectedList in Course Panel
        root = panelCourse.selectedList.invisibleRootItem()
        slCount = root.childCount()
        for i in range(slCount - 1, -1, -1):  # loop through each subject-level
            slItem = root.child(i)
            slName = slItem.text(0).split()
            subjName = slName[0]
            crseCount = slItem.childCount()
            for j in range(crseCount - 1, -1, -1):  # loop through each course in current subject-level
                crseSelected = slItem.child(j)
                crseText = crseSelected.text(0)
                crseNum = crseText.split()[0]

                # add corresponding course to filter
                crseItem = QTreeWidgetItem()
                crseItem.setText(0, "{} {}".format(subjName, crseText))
                self.filter.addTopLevelItem(crseItem)

                instructors = self.db.getInst(subjName, crseNum)   # Get all instructors teaching the course
                for instName in instructors:
                    instructor = QTreeWidgetItem(crseItem)
                    instructor.setText(0, instName)
                    instructor.setCheckState(0, Qt.Checked)

        self.db.close()
        self.filter.expandAll()
        self.filter.sortItems(0, Qt.AscendingOrder)