from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from reorderableList import MainForm
import math
import sip

class PanelResult(QMainWindow):
    def __init__(self):
        super(PanelResult, self).__init__()
        self.pgNum = 5

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)  # Overall vertical layout

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
        # Spacer
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Button
        self.previous = QPushButton("Previous", self.widget)
        self.previous.setFont(self.font)
        self.buttonSort = QPushButton("Sort")
        self.buttonSort.setFont(self.font)
        # label
        self.label = QLabel("Page: ")
        self.label.setFont(self.fontB)
        # Combo Box
        self.page = QComboBox()
        self.page.setCurrentIndex(0)
        self.page.currentIndexChanged.connect(lambda: self.stl.setCurrentIndex(self.page.currentIndex()))
        """
        Layout
        """
        self.stl = QStackedLayout()

        self.hl = QHBoxLayout()
        self.hl.addSpacerItem(self.spacer1)
        self.hl.addWidget(self.label)
        self.hl.addWidget(self.page)
        self.hl.addSpacerItem(self.spacer2)
        self.hl.addSpacerItem(self.spacer1)
        self.hl.addWidget(self.previous)
        self.hl.addWidget(self.buttonSort)

        # Overall layout
        self.layout.addLayout(self.stl)
        self.layout.addLayout(self.hl)

    def drawResult(self, results):
        if self.page.count() != 0:
            self.page.clear()

        while self.stl.count() != 0:
            page0 = self.stl.currentWidget()
            self.stl.removeWidget(page0)
            sip.delete(page0)

        c = 25
        if len(results) < 25:
            c = len(results)
        self.pgNum = math.ceil(c/5)  # Number of page for displaying result
        items = [str(n+1) for n in range(self.pgNum)]
        self.page.addItems(items)

        for i in items:
            self.stl.addWidget(self.__drawResultPage(i, c, results))

        self.stl.setCurrentIndex(0)

    def __drawResultPage(self, pg, c, results):
        pageWidget = QScrollArea()
        pageWidget.ensureVisible(960, 640)
        pageWidget.setWidgetResizable(True)
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vl = QVBoxLayout(widget)
        pg = int(pg)
        index = list(range((pg * 5 - 5), pg*5))
        if int(self.pgNum) != 5 and int(pg) == int(self.pgNum):
            index = list(range((pg * -5), c))
            if c == 1:
                index = [0]
        for i in index:
                vl.addWidget(self.__graphicSchedule(results, i))
                line = QFrame()     # separate line
                line.setFrameShadow(QFrame.Sunken)
                line.setFrameShape(QFrame.HLine)
                vl.addWidget(line)
        pageWidget.setWidget(widget)
        return pageWidget

    def __graphicSchedule(self, results, i):
        scheduleWidget = QWidget()
        scheduleWidget.setMinimumWidth(960)
        scheduleWidget.setMinimumHeight(600)
        scheduleWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vl = QVBoxLayout(scheduleWidget)
        label = QLabel("Result # " + str(i + 1))
        label.setFont(self.fontB)
        label.setMinimumHeight(50)

        list1 = QListWidget()       # time table

        '''
        Class information table
        '''
        classInfo = QTableWidget()
        classInfo.setColumnCount(10)
        classInfo.setRowCount(len(results[i].classList))
        classInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        classInfo.resizeColumnsToContents()
        classInfo.resizeRowsToContents()
        hHeader = classInfo.horizontalHeader()
        hHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
        hHeader.setFont(self.fontB)
        vHeader = classInfo.verticalHeader()
        vHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
        vHeader.setFont(self.fontB)
        colName = ['CRN', 'Crse', 'Sec', 'Days', 'Start', 'End', 'Instructor', 'Location', 'Date', 'Prereq']
        for c in range(10):
            classInfo.setHorizontalHeaderItem(c, QTableWidgetItem(colName[c]))

        count = 0
        for crse in results[i].classList:
            crn = QTableWidgetItem(str(crse.crn))
            crseNum = QTableWidgetItem(str(crse.subj) + " " + str(crse.crse))
            sec = QTableWidgetItem(str("{:02d}".format(int(crse.sec))))
            if len(crse.days) > 1:
                days = QTableWidgetItem('\n'.join(crse.days))
            else:
                days = QTableWidgetItem(crse.days[0])

            for x in range(len(crse.start)):
                if type(crse.start[x]) is str:
                    break
                st = crse.start[x].strftime('%H:%M')
                et = crse.end[x].strftime('%H:%M')
                crse.start[x] = st
                crse.end[x] = et

            if len(crse.start) > 1:
                start = QTableWidgetItem('\n'.join(crse.start))
                end = QTableWidgetItem('\n'.join(crse.end))
            else:
                start = QTableWidgetItem(crse.start[0])
                end = QTableWidgetItem(crse.end[0])

            inst = QTableWidgetItem(crse.inst)

            if len(crse.location) > 1:
                location = QTableWidgetItem('\n'.join(crse.location))
            else:
                location = QTableWidgetItem(crse.location[0])
            date = QTableWidgetItem(str(crse.date))
            if crse.prereq1 != '':
                text = crse.prereq1
                if crse.prereq2 != '':
                    text = text + ', ' + crse.prereq2
                    if crse.prereq3 != '':
                        text = text + ', ' + crse.prereq3
            else:
                text = 'None'
            prereq = QTableWidgetItem(text)

            classInfo.setItem(count, 0, crn)
            classInfo.setItem(count, 1, crseNum)
            classInfo.setItem(count, 2, sec)
            classInfo.setItem(count, 3, days)
            classInfo.setItem(count, 4, start)
            classInfo.setItem(count, 5, end)
            classInfo.setItem(count, 6, inst)
            classInfo.setItem(count, 7, location)
            classInfo.setItem(count, 8, date)
            classInfo.setItem(count, 9, prereq)
            count += 1


        '''
        Schedule quality information
        '''
        scheInfo = QTableWidget()
        scheInfo.setColumnCount(1)
        scheInfo.setRowCount(6)
        scheInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        scheInfo.resizeColumnsToContents()
        scheInfo.resizeRowsToContents()
        hHeader = scheInfo.horizontalHeader()
        hHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
        hHeader.setFont(self.fontB)
        vHeader = scheInfo.verticalHeader()
        vHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
        vHeader.setFont(self.fontB)
        scheInfo.horizontalHeader().hide()
        rowName = ["School Day: ", "Start Time: ", "End Time: ",
                   "Class Length: ", "Unexpected\nInstructor: ", "Distance: "]
        for k in range(6):
            scheInfo.setVerticalHeaderItem(k, QTableWidgetItem(rowName[k]))

        if results[i].schoolDayCheck == 3:
            r1 = "Extra Day Off"
        elif results[i].schoolDayCheck == 2:
            r1 = "Match Preferences"
        elif results[i].schoolDayCheck == 1:
            r1 = "Does not match, but day off exists"
        elif results[i].schoolDayCheck == 0:
            r1 = "Does not match, no day off"

        r2 = str(results[i].startCheck) + " Day matched"
        r3 = str(results[i].endCheck) + " Day matched"

        if results[i].classLenCheck == 1:
            r4 = "Match Preference"
        else:
            r4 = "Does not match"

        r5 = str(results[i].instCheck)
        r6 = str(results[i].routeScore)

        scheInfo.setItem(0, 0, QTableWidgetItem(r1))
        scheInfo.setItem(1, 0, QTableWidgetItem(r2))
        scheInfo.setItem(2, 0, QTableWidgetItem(r3))
        scheInfo.setItem(3, 0, QTableWidgetItem(r4))
        scheInfo.setItem(4, 0, QTableWidgetItem(r5))
        scheInfo.setItem(5, 0, QTableWidgetItem(r6))

        btnExprot = QPushButton("Exprot")   # button exprot

        vl1 = QVBoxLayout()
        vl1.addWidget(scheInfo)
        vl1.addWidget(btnExprot)

        hl = QHBoxLayout()
        spLeft = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spLeft.setHorizontalStretch(2)
        classInfo.setSizePolicy(spLeft)
        spRight = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        spRight.setHorizontalStretch(1)
        scheInfo.setSizePolicy(spRight)
        btnExprot.setSizePolicy(spRight)
        hl.addWidget(classInfo)
        hl.addLayout(vl1)

        vl.addWidget(label)
        vl.addWidget(list1)
        vl.addLayout(hl)

        return scheduleWidget


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
        if len(self.priorityList.nodes) == 0:
            self.gui.guiData.setPriority()
        self.gui.results.rank(self.gui.guiData)
        self.gui.pResult.drawResult(self.gui.results.scheduleList)
        self.close()
        self.gui.statusBar.showMessage("Sorted")



    def checkBox(self, text, default):
        checkBox = QCheckBox()
        checkBox.setText(text)
        checkBox.setChecked(default)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setMaximumHeight(100)
        return checkBox
