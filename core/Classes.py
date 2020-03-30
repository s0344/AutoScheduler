# An object that store the course information that is targeted for the core algorithm

from database.DB import *
from core.Course import *
from datetime import datetime
import copy


class Classes():
    def __init__(self, crn):
        # connect to database
        self.db = DB()
        self.db.useDatabase()
        # defining object properties
        self.crn = crn
        self.subj = None
        self.crse = None
        self.rem = None
        self.inst = None
        self.days = None
        self.start = None
        self.end = None
        self.classTime = None
        self.location = None
        self.date = None
        self.prereq1 = None
        self.prereq2 = None
        self.prereq3 = None
        self.sec = None
        # use setup function to set up all the properties
        self.setup(crn)

    def setup(self, crn):
        data = self.db.getClassData(crn)
        count = 0
        for i in data:
            if count == 0:
                self.subj = i[1]
                self.crse = i[2]
                self.rem = i[3]
                self.inst = i[4]
                self.days = [i[5],]
                self.start = [datetime.strptime(i[6], '%H:%M'),]
                self.end = [datetime.strptime(i[7], '%H:%M'),]
                self.classTime = [self.calClassTime(i[6],i[7]),] # list is used in case there are more than one class
                self.location = [i[8],] # same as previous reason, eg: phy labs
                self.date = i[9]
                self.prereq1 = self.checkPrereq(i[10])
                self.prereq2 = self.checkPrereq(i[11])
                self.prereq3 = self.checkPrereq(i[12])
                self.sec = i[13]
                count += 1
            else:
                self.days.append(i[5])
                self.start.append(datetime.strptime(i[6], '%H:%M'))
                self.end.append(datetime.strptime(i[7], '%H:%M'))
                self.classTime.append(self.calClassTime(i[6],i[7]))
                if i[8] not in self.location:
                    self.location.append(i[8])

    # calculate the time diff of the start and end time of a lesson
    # takes string as input and return a datetime object
    def calClassTime(self,start,end):
        starttime = datetime.strptime(start, '%H:%M')
        endtime = datetime.strptime(end, '%H:%M')
        result = endtime - starttime
        return result

    def checkPrereq(self, prereq):
        data = prereq.split("+")
        result = ""
        count = 0
        for prereq in data:
            count += 1
            result += prereq if count<2 else " or "+prereq
        return result

    def printSimpleData(self):
        print("crn: ", self.crn)
        print("subj: ", self.subj)
        print("crse: ", self.crse)
        print("section: ", self.sec)
        print("=======================")


    def printDetailData(self):
        print("crn: ",self.crn)
        print("subj: ",self.subj)
        print("crse: ",self.crse)
        print("section: ",self.sec)
        print("rem: ",self.rem)
        print("inst: ",self.inst)
        print("days: ",self.days)
        print("start time: ", end="")
        for time in self.start:
            print(time.time(), end=", ")
        print()

        print("end time: ", end="")
        for time in self.end:
            print(time.time(), end=", ")
        print()

        print("class time: ",end="")
        for time in self.classTime:
            print(str(time),end=", ")
        print()
        print("location: ",self.location)
        print("date: ",self.date)
        print("prereq1: ",self.prereq1)
        print("prereq2: ",self.prereq2)
        print("prereq3: ",self.prereq3)
        print("=======================")

    # override original deepcopy to deepcopy this object, used in bruteforce/Schedule
    def __deepcopy__(self, memo):
        return Classes(copy.deepcopy(self.crn, memo))