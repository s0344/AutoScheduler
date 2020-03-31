from PyQt5.QtCore import Qt
from datetime import datetime

# a class getting data from the gui
class UIdata():
    def __init__(self, gui):
        self.__gui = gui

        # int: Total number of course going to take
        self.__courseLimit = None

        # list of string: priority
        self.__priority = None

        # list of boolean: value for school days
        # index 0 - 4: Monday - Friday
        self.__schoolDay = None

        # list of boolean: value for length of class
        # index 0 - 2: 50Min, 1Hr15Min, 2Hr45Min
        self.__classLen = None

        # list of string: Start Time
        # possible value: from "08:00" to "21:30", every 30 minutes
        # index 0 - 4: Monday - Friday
        self.__st = None

        # list of string: End Time for everyday
        # possible value: from "08:00" to "21:30", every 30 minutes
        # index 0 - 4: Monday - Friday
        self.__et = None

        """
        Data from Selected List (sl)
        list of slTuple:
             [(str subj, str lv, str #crse, list crse)]
        eg. ("CMPT", "100", "Ignore", crse)
            cres is a list of clTuple:
            [(str crseNum, bool mandatory, list instructors)]
            eg. ("101", True, instructors)
                    inst is a list of tuple (str instName, bool chk)
                    chk is the whether the instructor is checked in the filter 
        """
        self.__courses = None

    def setCourseLimit(self):
        self.__courseLimit = int(self.__gui.pCourse.limit.currentText())

    def setPriority(self):
        self.__priority = self.__gui.pPriority.priorityList.defaultPriority

    def setSchoolDay(self):
        self.__schoolDay = [self.__gui.pPreference.check1.checkState(),
                            self.__gui.pPreference.check2.checkState(),
                            self.__gui.pPreference.check3.checkState(),
                            self.__gui.pPreference.check4.checkState(),
                            self.__gui.pPreference.check5.checkState()]
        # convert to binary check state value
        for i in range(len(self.__schoolDay)):
            self.__schoolDay[i] = self.__biCheckState(self.__schoolDay[i])

    def setClassLen(self):
        self.__classLen = [self.__gui.pPreference.check50.checkState(),
                           self.__gui.pPreference.check75.checkState(),
                           self.__gui.pPreference.check180.checkState()]
        # convert to binary check state value
        for i in range(len(self.__classLen)):
            self.__classLen[i] = self.__biCheckState(self.__classLen[i])

    def setTime(self):
        self.__st = [self.__gui.pPreference.st1.currentText(),
                     self.__gui.pPreference.st2.currentText(),
                     self.__gui.pPreference.st3.currentText(),
                     self.__gui.pPreference.st4.currentText(),
                     self.__gui.pPreference.st5.currentText()]

        self.__et = [self.__gui.pPreference.et1.currentText(),
                     self.__gui.pPreference.et2.currentText(),
                     self.__gui.pPreference.et3.currentText(),
                     self.__gui.pPreference.et4.currentText(),
                     self.__gui.pPreference.et5.currentText()]

        for i in range(5):
            self.__st[i] = datetime.strptime(self.__st[i], "%H:%M")
            self.__et[i] = datetime.strptime(self.__et[i], "%H:%M")


    def setCourses(self):
        self.__courses = self.__selectedData()

    def __selectedData(self):
        data = []

        # Access the selected list in gui
        sl = self.__gui.pCourse.selectedList
        slRoot = sl.invisibleRootItem()

        slCount = slRoot.childCount()
        for i in range(slCount):  # loop through each subject-level
            slItem = slRoot.child(i)

            # get subject name and level
            slText = slItem.text(0).split()
            subj = slText[0]
            lv = slText[1]
            # get combo box value
            lvLimit = sl.itemWidget(slItem, 2).currentText()
            # data of courses in current subj-level
            crseList = self.__courseData(subj, slItem)

            tup = slTuple(subj, lv, lvLimit, crseList)
            data.append(tup)

        return data

    def __courseData(self, subj, slItem):
        data = []
        # Access the selected list in gui
        sl = self.__gui.pCourse.selectedList

        crseCount = slItem.childCount()
        for i in range(crseCount):
            crseItem = slItem.child(i)
            crseItemText = crseItem.text(0)
            # course number
            crseNum = crseItemText.split()
            crseNum = crseNum[0]
            # value of check box for mandatory
            checkBox = sl.itemWidget(crseItem, 1)
            mandatory = checkBox.checkState()
            mandatory = self.__biCheckState(mandatory)
            # instructor data of the course
            instructors = self.__instData(subj, crseItemText)
            tup = clTuple(crseNum, mandatory, instructors)
            data.append(tup)
        return data

    def __instData(self, subj, crseItemText):
        data = []
        filter = self.__gui.pInstructor.filter
        searchTerm = "{} {}".format(subj, crseItemText)
        crse = filter.findItems(searchTerm, Qt.MatchExactly)
        crse = crse[0]
        crseCount = crse.childCount()
        for i in range(crseCount):
            instName = crse.child(i).text(0)
            instCheck = crse.child(i).checkState(0)
            instCheck = self.__biCheckState(instCheck)
            tup = (instName, instCheck)
            data.append(tup)
        return data

    def __biCheckState(self, val):
        if val == 2:
            return 1
        return val

    def getPriority(self):
        return self.__priority

    def getSchoolDay(self):
        return self.__schoolDay

    def getClassLen(self):
        return self.__classLen

    def getStartTime(self):
        return self.__st

    def getEndTime(self):
        return self.__et

    def getCourses(self):
        return self.__courses

    def getNotSelectedInst(self):
        data = []
        for sl in self.__courses:
            for crse in sl.crseList:
                for instructors in crse.instructors:
                    if instructors[1] == 0:
                        tup = (crse.crseNum, instructors[0])
                        data.append(tup)
        return data

    def getCourseLimit(self):
        return self.__courseLimit

    def dataValidation(self):
        message = []

        # start time and end time
        for i in range(5):
            if self.__st[i] > self.__et[i]:
                message.append("Start Time later than End Time")
                break

        # length of class
        if all(v == 0 for v in self.__classLen):
            message.append("No Length of Class Selected")

        # school day
        if all(v == 0 for v in self.__schoolDay):
            message.append("No School Day Selected")

        # course = self.__courses
        # sum_Man = 0     # sum of user-selected mandatory
        # for subjLv in course:
        #     sum_LvMan = 0   # sum of user-selected mandatory in the subj-level
        #     crseList = subjLv.crseList
        #     for crse in crseList:
        #         sum_LvMan += crse.mandatory
        #         sum_Man += crse.mandatory
        #
        #         for instructor in crse.instructors:
        #             if crse.mandatory == 1 and len(crse.instructors) == 1 and instructor[1] == 0:
        #                 msg = "For your mandatory course " + str(subjLv.subj) + str(crse.crseNum) + \
        #                       ", choose at least one instructor"
        #                 message.append(msg)
        #
        #     if sum_LvMan > int(subjLv.lvLimit) and subjLv.lvLimit is not "Ignore":
        #         msg = "For " + str(subjLv.subj) + str(subjLv.lv) + " Level : # of Mandatory Course > # of Course"
        #         message.append(msg)
        #
        # if sum_Man > self.__courseLimit:
        #     message.append("# of Mandatory Course > # of Course going to take")

        return message


# container for data of selected list
class slTuple():
    def __init__(self, subj, lv, lvLimit, crseList):
        self.subj = subj            # Name of the subject
        self.lv = lv                # level
        self.lvLimit = lvLimit      # value of the combo box
        self.crseList = crseList    # list of selected course (clTuple)

# data container of selected course
class clTuple():
    def __init__(self, crseNum, mandatory, instructors):
        self.crseNum = crseNum
        self.mandatory = mandatory
        self.instructors = instructors
