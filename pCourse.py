from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from database.DB import *
import string

class PanelCourse(QMainWindow):
    """
    Draw "Course" panel
    """
    def __init__(self):
        super(PanelCourse, self).__init__()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)  # Overall vertical layout

        # Font
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(9)
        self.setFont(self.font)

        """
        Widgets
        """
        # Label
        self.label = QLabel("Number of course going to take: ", self.widget)
        fontB = QtGui.QFont()
        fontB.setFamily("Arial")
        fontB.setPointSize(10)
        fontB.setBold(True)
        self.label.setFont(fontB)
        # Combo Box
        self.limit = QComboBox(self.widget)
        self.limit.addItems([str(n + 1) for n in range(10)])
        self.limit.setCurrentIndex(4)
        # Spacer
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Course List
        self.courseList = QTreeWidget(self.widget)
        # Selected Course List
        self.selectedList = QTreeWidget(self.widget)
        # Add Button
        self.add = QPushButton("Add", self.widget)
        # Remove Button
        self.remove = QPushButton("Remove", self.widget)
        # Next Button
        self.next = QPushButton("Next", self.widget)

        """
        Layout
        """
        # Horizontal layout 1
        self.hl1 = QHBoxLayout(self.widget)
        self.hl1.setContentsMargins(0, 15, 0, 15)
        self.hl1.addItem(self.spacer1)
        self.hl1.addWidget(self.label)
        self.hl1.addWidget(self.limit)

        # Horizontal layout 2
        self.hl2 = QHBoxLayout(self.widget)
        self.hl2.addWidget(self.courseList)
        self.hl2.addWidget(self.selectedList)
        # Horizontal layout 3
        self.hl3 = QHBoxLayout(self.widget)
        self.hl3.addItem(self.spacer2)
        self.hl3.addWidget(self.add)
        self.hl3.addWidget(self.remove)
        self.hl3.addItem(self.spacer3)
        # Horizontal layout 4
        self.hl4 = QHBoxLayout(self.widget)
        self.hl4.addItem(self.spacer4)
        self.hl4.addWidget(self.next)
        # Overall layout
        self.layout.addLayout(self.hl1)
        self.layout.addLayout(self.hl2)
        self.layout.addLayout(self.hl3)
        self.layout.addLayout(self.hl4)

        """
        Events
        """
        self.initCourseList()
        self.initSelectedList()
        self.add.clicked.connect(lambda: self.addButtonEvent())
        self.remove.clicked.connect(lambda: self.removeButtonEvent())


    """
    Member functions
    """
    def initCourseList(self):
        self.courseList.setHeaderLabel("Course Available")
        self.courseList.expanded.connect(lambda: self.courseList.setColumnWidth(0, (self.courseList.width() + 200)))

        # connect to database
        self.db = DB()
        self.db.useDatabase()

        # fetch and display data
        subjects = self.db.getSubject()     # list of subject
        for x in subjects:  # x: subject name
            subjItem = QTreeWidgetItem(self.courseList)
            subjItem.setText(0, x)
            levels = self.db.getLevel(x)
            for y in levels:    # y: level in subject x
                lvItem = QTreeWidgetItem(subjItem)
                lvItem.setFlags(lvItem.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                lvItem.setText(0, "{} Level".format(y))
                lvItem.setCheckState(0, Qt.Unchecked)
                courses = self.db.getCourse(x, y)
                for z in courses:   # z: course name in "subject x - level y"
                    crseItem = QTreeWidgetItem(lvItem)
                    title = self.db.getTitle(x, z)
                    crseItem.setFlags(crseItem.flags() | Qt.ItemIsUserCheckable)
                    crseItem.setText(0, "{} - {}".format(z, title[0]))
                    crseItem.setCheckState(0, Qt.Unchecked)
                    # tooltips reminding prerequisites
                    prereqs = self.db.getPrereq(x, z)
                    tip = ""
                    for prereq in prereqs:
                        if prereq == "":
                            continue
                        plus = prereq.find("+")
                        if plus != -1:
                            prereq = prereq[:plus] + " or " + prereq[plus + 1:len(prereq)]
                        tip = tip + ", and " + prereq
                    tip = "Prereq: " + tip[6: len(tip)]
                    if tip == "Prereq: ":
                        tip = "No prerequisites"
                    crseItem.setToolTip(0, tip)

        self.courseList.sortItems(0, Qt.AscendingOrder)
        self.db.close()

    def initSelectedList(self):
        self.selectedList.setColumnCount(3)
        self.selectedList.setHeaderLabels(["Intended Course", "Mandatory", "# of Course"])
        self.selectedList.setColumnWidth(0, 300)
        self.selectedList.setColumnWidth(1, 90)
        self.selectedList.setColumnWidth(2, 80)
        header = self.selectedList.headerItem()
        header.setToolTip(2, "Number of Course needs to take for the level")

    def addButtonEvent(self):
        root = self.courseList.invisibleRootItem()
        subjCount = root.childCount()
        for i in range(subjCount):     # loop through each subject
            subjItem = root.child(i)
            lvCount = subjItem.childCount()
            for j in range(lvCount - 1, -1, -1):    # loop through each level in current subject
                lvItem = subjItem.child(j)
                lvState = lvItem.checkState(0)
                if lvState != Qt.Unchecked:   # if entire level is checked
                    self.__addToSelected(subjItem, lvItem)
        self.selectedList.sortItems(0, Qt.AscendingOrder)

    # used only by addButtonEvent()
    def __addToSelected(self, subjItem, lvItem):
        # find corresponding subject-level
        searchTerm = "{} {}".format(subjItem.text(0), lvItem.text(0))
        find = self.selectedList.findItems(searchTerm, Qt.MatchExactly)
        # check if the level exists in selected list
        if len(find):
            tarLv = find[0]
        else:
            # create level item in selectedList
            tarLv = QTreeWidgetItem()
            tarLv.setText(0, searchTerm)
            # combo box for each level item
            comboBox = QComboBox()
            num = [str(n+1) for n in range(5)]
            num.append("Ignore")
            comboBox.addItems(num)
            comboBox.setCurrentIndex(len(num) -1 )
            self.selectedList.addTopLevelItem(tarLv)
            self.selectedList.setItemWidget(tarLv, 2, comboBox)
            self.selectedList.expandItem(tarLv)

        # move checked crse
        crseCount = lvItem.childCount()  # loop through each course in current level
        for k in range(crseCount - 1, -1, -1):
            crseItem = lvItem.child(k)
            crseState = crseItem.checkState(0)
            if crseState == Qt.Checked:
                checkedItem = lvItem.takeChild(k)
                checkedItem.setText(0, "{}".format(crseItem.text(0)))
                checkedItem.setCheckState(0, Qt.Unchecked)
                tarLv.addChild(checkedItem)
                checkBox = QCheckBox()
                checkBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.selectedList.setItemWidget(checkedItem, 1, checkBox)

        # remove empty level in courseList
        if lvItem.childCount() == 0:
            subjItem.removeChild(lvItem)

    def removeButtonEvent(self):
        root = self.selectedList.invisibleRootItem()
        slCount = root.childCount()
        for i in range(slCount - 1, -1, -1):  # loop through each subject-level
            slItem = root.child(i)
            crseCount = slItem.childCount()
            for j in range(crseCount - 1, -1, -1):  # loop through each course in current subject-level
                crseItem = slItem.child(j)
                crseState = crseItem.checkState(0)
                if crseState == Qt.Checked:  # if crse is checked
                    self.__removeFromSelcted(i, j,slItem)

        self.courseList.sortItems(0, Qt.AscendingOrder)
        self.selectedList.sortItems(0, Qt.AscendingOrder)

    # used only by removeButtonEvent()
    def __removeFromSelcted(self, i, j, slItem):
        # find corresponding subject
        searchTerm = slItem.text(0).split()
        subjName = searchTerm[0]
        lvName = " ".join(searchTerm[1:len(searchTerm)])
        tarSubj = self.courseList.findItems(subjName, Qt.MatchExactly)[0]
        isFind = False
        # check if the level exists in corresponding subject
        for k in range(tarSubj.childCount()):
            lvItem = tarSubj.child(k)
            if lvItem.text(0) == lvName:
                tarLv = lvItem
                isFind = True
                break

        if isFind is False:     # create level in courseList
            tarLv = QTreeWidgetItem()
            tarLv.setText(0, lvName)
            tarLv.setFlags(tarLv.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            tarLv.setCheckState(0, Qt.Unchecked)
            tarSubj.addChild(tarLv)

        # move checked crse
        crseItem = slItem.takeChild(j)
        crseItem.setCheckState(0, Qt.Unchecked)
        tarLv.addChild(crseItem)

        if slItem.childCount() == 0:
            self.selectedList.removeItemWidget(slItem, 2)
            self.selectedList.removeItemWidget(slItem, 0)
            self.selectedList.takeTopLevelItem(i)



