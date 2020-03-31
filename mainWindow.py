from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from pCourse import PanelCourse
from pInstructor import PanelInstructor
from pPreference import PanelPreference
from pPriority import PanelPriority
from pResult import PanelResult
from UIdata import *
from core.coreDriver import coreDriver


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.guiData = None
        """
        Draw the main window
        """
        self.setGeometry(200, 200, 1000, 650)
        self.setWindowTitle("Auto Course Scheduler")
        self.setWindowIcon(QtGui.QIcon('pictures/prgmIcon.png'))
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QHBoxLayout(self.centralWidget)   # Central Widget using horizontal layout

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

        self.lb3 = QLabel("Priority", self.leftWidget)
        self.lb3.setAlignment(Qt.AlignCenter)
        self.lb3.setSizePolicy(self.leftSizePolicy)
        self.lb3.setMinimumHeight(self.leftMinHeight)

        self.lb4 = QLabel("Result", self.leftWidget)
        self.lb4.setAlignment(Qt.AlignCenter)
        self.lb4.setSizePolicy(self.leftSizePolicy)
        self.lb4.setMinimumHeight(self.leftMinHeight)
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
        self.pPriority = PanelPriority()
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
        self.leftLayout.addWidget(self.lb4)
        self.leftLayout.addSpacerItem(self.vSpacer2)
        # Add panels to the stacked layout
        self.rightLayout = QStackedLayout(self.rightWidget)  # Right column using stacked layout
        self.rightLayout.addWidget(self.pCourse)
        self.rightLayout.addWidget(self.pInstructor)
        self.rightLayout.addWidget(self.pPreference)
        self.rightLayout.addWidget(self.pPriority)
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
        self.pPreference.next.clicked.connect(lambda: self.click_next())
        self.pPreference.previous.clicked.connect(lambda: self.showPreviousPanel())
        # Panel Priority
        self.pPriority.submit.clicked.connect(lambda: self.click_submit())
        self.pPriority.previous.clicked.connect(lambda: self.showPreviousPanel())


    """
    Member functions
    """
    def panelIndication(self):
        currentIndex = self.rightLayout.currentIndex()
        dic = {0: self.lb0,
               1: self.lb1,
               2: self.lb2,
               3: self.lb3,
               4: self.lb4}
        for i in range(5):
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
        elif currentIndex == 2:
            self.guiData.setSchoolDay()
            self.guiData.setTime()
            self.guiData.setClassLen()

        self.showNextPanel()

    def showNextPanel(self):
        self.rightLayout.setCurrentIndex(self.rightLayout.currentIndex() + 1)

    def showPreviousPanel(self):
        self.rightLayout.setCurrentIndex(self.rightLayout.currentIndex() - 1)

    def click_submit(self):
        self.guiData.setPriority()
        coreDriver(self.guiData)
        self.showNextPanel()
