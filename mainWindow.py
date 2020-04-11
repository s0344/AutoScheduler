from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from pCourse import PanelCourse
from pInstructor import PanelInstructor
from pPreference import PanelPreference
from pResult import PanelResult
from UIdata import *
from core.coreDriver import coreDriver
import threading


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.guiData = None
        self.result = None
        """
        Draw the main window
        """
        self.setGeometry(200, 200, 1200, 750)
        self.setWindowTitle("Auto Course Scheduler")
        self.setWindowIcon(QtGui.QIcon('pictures/prgmIcon.png'))
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QHBoxLayout(self.centralWidget)   # Central Widget using horizontal layout
        self.statusBar = self.statusBar()

        '''
        Left column widgets
        '''
        self.leftWidget = QWidget(self.centralWidget)
        self.leftWidget.setMaximumWidth(150)

        # Font of leftWidget
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(10)
        self.leftWidget.setFont(self.font)
        # Size policy in left column
        self.leftSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.leftMinHeight = 50
        # Logo
        self.logo = QLabel(self.leftWidget)
        self.logo.setPixmap(QtGui.QPixmap("pictures/MClogo.png"))
        self.logo.setScaledContents(True)
        self.logo.setSizePolicy(self.leftSizePolicy)
        self.logo.setMaximumSize(150, 118)
        # Labels
        self.lb0 = QLabel("Course", self.leftWidget)
        self.lb0.setFrameShape(QFrame.Box)
        self.lb0.setAlignment(Qt.AlignCenter)
        self.lb0.setSizePolicy(self.leftSizePolicy)
        self.lb0.setMinimumHeight(self.leftMinHeight)

        self.lb1 = QLabel("Instructor", self.leftWidget)
        self.lb1.setAlignment(Qt.AlignCenter)
        self.lb1.setSizePolicy(self.leftSizePolicy)
        self.lb1.setMinimumHeight(self.leftMinHeight)

        self.lb2 = QLabel("Preference", self.leftWidget)
        self.lb2.setAlignment(Qt.AlignCenter)
        self.lb2.setSizePolicy(self.leftSizePolicy)
        self.lb2.setMinimumHeight(self.leftMinHeight)

        self.lb3 = QLabel("Result", self.leftWidget)
        self.lb3.setAlignment(Qt.AlignCenter)
        self.lb3.setSizePolicy(self.leftSizePolicy)
        self.lb3.setMinimumHeight(self.leftMinHeight)
        # Spacer
        self.vSpacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.vSpacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)


        '''
        Right column widget
        '''
        self.rightWidget = QWidget(self.centralWidget)
        # Panels
        self.pCourse = PanelCourse()
        self.pInstructor = PanelInstructor()
        self.pPreference = PanelPreference()
        self.pResult = PanelResult()


        """
        Layout
        """
        # Add widgets to left column
        self.leftLayout = QVBoxLayout(self.leftWidget)  # leftWidget using vertical layout
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setSpacing(0)
        self.leftLayout.addWidget(self.logo)
        self.leftLayout.addSpacerItem(self.vSpacer1)
        self.leftLayout.addWidget(self.lb0)
        self.leftLayout.addWidget(self.lb1)
        self.leftLayout.addWidget(self.lb2)
        self.leftLayout.addWidget(self.lb3)
        self.leftLayout.addSpacerItem(self.vSpacer2)
        # Add panels to the stacked layout
        self.rightLayout = QStackedLayout(self.rightWidget)  # Right column using stacked layout
        self.rightLayout.addWidget(self.pCourse)
        self.rightLayout.addWidget(self.pInstructor)
        self.rightLayout.addWidget(self.pPreference)
        self.rightLayout.addWidget(self.pResult)
        # Overall Layout
        self.centralLayout.addWidget(self.leftWidget)
        self.centralLayout.addWidget(self.rightWidget)

        """
        Events
        """
        # UI data
        self.guiData = UIdata(self)
        # Panel Indication
        self.rightLayout.currentChanged.connect(lambda: self.panelIndication())
        # Next/Previous Buttons
        # Panel Course
        self.pCourse.next.clicked.connect(lambda: self.click_next())
        # Panel Instructor
        self.pInstructor.next.clicked.connect(lambda: self.click_next())
        self.pInstructor.previous.clicked.connect(lambda: self.showPreviousPanel())
        # Panel Preference
        self.pPreference.fullSearch.clicked.connect(lambda: self.click_submit(1))
        self.pPreference.quickSearch.clicked.connect(lambda: self.click_submit(0))
        self.pPreference.previous.clicked.connect(lambda: self.showPreviousPanel())
        # Panel Result
        self.pResult.previous.clicked.connect(lambda: self.showPreviousPanel())
        self.pResult.buttonChange.clicked.connect(lambda: self.priorityChange())

    """
    Member functions
    """
    def panelIndication(self):
        currentIndex = self.rightLayout.currentIndex()
        dic = {0: self.lb0,
               1: self.lb1,
               2: self.lb2,
               3: self.lb3,
               }
        for i in range(4):
            dic[i].setFrameShape(QFrame.NoFrame)
            if i is currentIndex:
                dic[i].setFrameShape(QFrame.Box)

    def click_next(self):
        currentIndex = self.rightLayout.currentIndex()
        if currentIndex == 0:
            self.guiData.setCourseLimit()
            self.pInstructor.filterEvent(self.pCourse)
        elif currentIndex == 1:
            self.guiData.setCourses()
        self.showNextPanel()

    def showNextPanel(self):
        self.rightLayout.setCurrentIndex(self.rightLayout.currentIndex() + 1)

    def showPreviousPanel(self):
        self.rightLayout.setCurrentIndex(self.rightLayout.currentIndex() - 1)

    # flag 1: full search(brute force), flag 0: quick search(return 1 worked result)
    def click_submit(self, flag):
        self.guiData.setSchoolDay()
        self.guiData.setTime()
        self.guiData.setClassLen()
        self.guiData.setPriority()
        self.guiData.setErrmsg()
        if len(self.guiData.errmsg) == 0:
            self.guiData.setInfo()
            if len(self.guiData.info) != 0:
                self.dialog(self.guiData.info, 1)
            self.th1 = MyThread(coreDriver, (self.guiData, flag,))
            self.th1.finished.connect(lambda: self.progressFinish())
            self.th1.start()
            self.pPreference.previous.setDisabled(True)
            self.pPreference.fullSearch.setDisabled(True)
            self.pPreference.quickSearch.setDisabled(True)
            lbGif = QLabel()
            lbText = QLabel("Progressing")
            gif = QMovie("pictures/loading.gif")
            gif.start()
            lbGif.setScaledContents(True)
            lbGif.setMovie(gif)
            lbGif.setMaximumSize(20, 20)
            self.statusBar.addWidget(lbGif)
            self.statusBar.addWidget(lbText)

        else:
            self.dialog(self.guiData.errmsg, 0)

    def progressFinish(self):
        # self.pResult.drawResult()
        self.showNextPanel()
        self.statusBar.showMessage("Finished")

    # flag: 1 for info, 0 for errmsg
    def dialog(self, msg, flag):
        window = QDialog()
        window.setWindowTitle("AutoScheduler")
        window.setWindowIcon(QtGui.QIcon("pictures/prgmIcon.png"))
        window.setAttribute(Qt.WA_DeleteOnClose)
        window.setFont(self.font)
        window.setContentsMargins(15, 15, 15, 10)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)

        layout = QVBoxLayout(window)
        layout.setSpacing(15)
        if flag:
            lb1 = QLabel("Please notice:")
            button = QPushButton("OK")
        else:
            lb1 = QLabel("Error!")
            button = QPushButton("Close")
        button.clicked.connect(lambda: window.close())
        lb1.setFont(font)
        layout.addWidget(lb1)
        for i in range(len(msg)):
            if i == len(msg) - 1 and flag:
                lb = QLabel(msg[i])
                lb.setFont(font)
                layout.addWidget(lb)
                continue
            layout.addWidget(QLabel("\t" + str(i+1) + ". " + msg[i]))

        hl = QHBoxLayout(window)
        hl.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hl.addWidget(button)
        layout.addLayout(hl)

        window.exec()

    def priorityChange(self):
        self.guiData.setPriority()
        self.result.rank(self.guiData)


class MyThread(QtCore.QThread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None





