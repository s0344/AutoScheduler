import copy
from database.DB import *
from datetime import datetime

class Schedule():
    def __init__(self, classList):
        self.classList = copy.deepcopy(classList)
        self.weekList = [[], [], [], [], []]
        self.schoolDayCheck = None
        self.startCheck = None
        self.endCheck = None
        self.classLenCheck = True
        self.instCheck = None
        self.routeScore = None
        self.setupCheck()


    '''
    Priority type:
    School Day(if user choose a  dayooff): match and extra day off(3), match(2), no match but have day off(1), no dayoff(0)
    School Day(if user didn't choose):  match and extra day off(3), match(2)
    Length of Class(indicating value): match(1), not match(0)
    Start Time: base on how many days match (0-5)
    End Time: base on how many days match(0-5)
    Instructor: base on how many instructor that the user doesn't want is in the scheduler(0-5) lower better
    route: value lower the better
    '''

    # check if the schedule match the default priority
    def setupCheck(self):
        self.db = DB()
        self.db.useDatabase()
        # PART 1 - find all the data that is needed
        instList = []
        classLenList = []
        # week day list to match the class days
        weekDay = ['M', 'T', 'W', 'R', 'F']

        # create default preference for the priorities
        schoolDayPref = [1,1,1,1,1]
        instPref = []
        startPref = []
        for i in range(5):
            startPref.append(datetime.strptime("8:00","%H:%M"))
        endPref = []
        for i in range(5):
            endPref.append(datetime.strptime("21:30","%H:%M"))
        classLenPref = [1, 1, 1]

        # loop through each class to get data
        for classes in self.classList:
            # get class length of each classes
            for classLen in classes.classTime:
                if classLen not in classLenList:
                    classLenList.append(classLen)

            # get instructor
            if classes.inst not in instList:
                instList.append(classes.inst)

            index = 0  # a index used to access list data
            # add all the days in to a nested list
            for day in classes.days:  # days contains a list of lesson days
                # start checking each day(mon-fri)
                for i in range(5):
                    if weekDay[i] in day:
                        self.weekList[i].append((classes.start[index],classes.end[index]))
                index += 1  # increment to the index for next lesson

        for day in self.weekList:
            day.sort(key=lambda x:x[0])


        # PART 2 - check the priority state
        # calculate day off check, start check, end check, and classLength check.
        self.timeCheck(schoolDayPref, startPref, endPref, classLenList, classLenPref)
        # calculate route score
        self.routeCal()
        # calculate instructor check
        self.instructorCheck(instList, instPref)

        self.db.close()

    # check if the schedule match the user priority
    def updateCheck(self, data):
        self.db = DB()
        self.db.useDatabase()
        # PART 1 - find all the data that is needed
        instList = []
        classLenList = []
        # week day list to match the class days
        weekDay = ['M', 'T', 'W', 'R', 'F']

        # create default preference for the priorities
        schoolDayPref = data.getSchoolDay()
        instPref = data.getNotSelectedInst()
        startPref = data.getStartTime()
        endPref = data.getEndTime()
        classLenPref = data.getClassLen()

        # loop through each class to get data
        for classes in self.classList:
            # get class length of each classes
            for classLen in classes.classTime:
                if classLen not in classLenList:
                    classLenList.append(classLen)

            # get instructor
            if classes.inst not in instList:
                instList.append(classes.inst)
            '''
            index = 0  # a index used to access list data
            # add all the days in to a nested list
            for day in classes.days:  # days contains a list of lesson days
                # start checking each day(mon-fri)
                for i in range(5):
                    if weekDay[i] in day:
                        self.weekList[i].append((classes.start[index], classes.end[index]))
                index += 1  # increment to the index for next lesson
            '''

        # PART 2 - check the priority state
        # calculate day off check, start check, end check, and classLength check.
        self.timeCheck(schoolDayPref, startPref, endPref, classLenList, classLenPref)
        # calculate route score
        self.routeCal()
        # calculate instructor check
        self.instructorCheck(instList, instPref)

        self.db.close()

    # print the crn(s) of the schedule
    def printData(self):
        for classes in self.classList:
            print(classes.crn, end = " ")
        print()

    # check the state of schoolday, start, end, and classLength
    def timeCheck(self, schoolDayPref, startPref, endPref, classLenList, classLenPref):
        schoolDayList = []  # store a list of day off
        dayOffList = []  # store the index of the day off in day off list to identify which day is day off
        startCount = 0
        endCount = 0
        classLenRef = ["0:50", "1:15", "2:45"]
        index = 0  # index to access start and end time

        # handling the classLength
        for i in range(3):
            if classLenPref[i]:
                if classLenRef[i] not in classLenList:  # when it is 1 but classLength not in the list
                    self.classLenCheck = False
                    break
            else:
                if classLenRef[i] in classLenList:  # when it is 0 but classLength is in the list
                    self.classLenCheck = False
                    break

        # handling start and end check
        for day in self.weekList:
            # check day off first
            if len(day) > 0:
                schoolDayList.append(1)
            else:  # when that day is a day off
                schoolDayList.append(0)
                startCount += 1
                endCount += 1
                continue

            # check day start: if class start after or at start time +1
            if day[0][0] >= startPref[index]:  # day[0][0] first index: first class of the day, second index: start time
                startCount += 1

            # check day end: if class end at or before end time +1
            if day[len(day)-1][1] <= endPref[index]:
                endCount += 1

            index += 1
        self.startCheck = startCount
        self.endCheck = endCount

        # evaluate day off list
        # setting up day off list
        for i in range(5):
            if not schoolDayList[i]:
                dayOffList.append(i)

        # true: user didn't chose a day off, false: there is day off
        mode = schoolDayPref.count(1) == 5

        if mode:
            if len(dayOffList):     # if there is dayoff
                self.schoolDayCheck = 3
            else:                   # no dayoff == match
                self.schoolDayCheck = 2
        else:
            # define temporary variables
            matchFlag = False
            matchCount = 0
            matchNum = schoolDayPref.count(0)
            matchIndex = 0

            # check if there is a match
            for dayoff in dayOffList:
                for i in range(5):
                    if not schoolDayPref[i] and i == dayoff:
                        matchCount += 1
                        matchIndex += 1
            if matchCount == matchNum:
                matchFlag = True

            # start assigning value to check
            if matchFlag:
                if len(dayOffList) > matchNum:  # if match and have extra day off
                    self.schoolDayCheck = 3
                else:                           # if match but no extra day off
                    self.schoolDayCheck = 2
            else:
                if len(dayOffList):             # if not all match but have day off
                    self.schoolDayCheck = 1
                else:                           # no dayoff at all
                    self.schoolDayCheck = 0

    # calculate the schedule route score
    def routeCal(self):
        # route calculation
        map = self.db.getMap()
        locationList = [[], [], [], [], []]
        weekDay = ['M', 'T', 'W', 'R', 'F']
        # create a dictionary of map
        mapDict = {row[0]: row[1] for row in map}

        # loop through each class and append location to list
        for classes in self.classList:
            index = 0  # a index used to access list data
            for day in classes.days:  # days contains a list of lesson days
                # start checking each day(mon-fri)
                for i in range(5):
                    if weekDay[i] in day:
                        locationList[i].append(classes.location[index])
                index += 1  # increment to the index for next lesson

        # start calculating score
        dayScore = [0,0,0,0,0]
        for day in range(5):
            for i in range(1,len(locationList[day])):
                location = locationList[day][i]
                lastLocation = locationList[day][i-1]

                # if location is TBA, assume the area is going to change
                if location == "TBA" or lastLocation == "TBA":
                    dayScore[day] += 100
                    continue

                building = location[0:3]
                lastBuilding = lastLocation[0:3]
                area = mapDict[building]
                lastArea = mapDict[lastBuilding]
                floor = location[4]
                lastFloor = lastLocation[4]

                if building != lastBuilding:
                    if area != lastArea:  # if area changed +100
                        dayScore[day] += 100
                    else:   # if building change in same area +10
                        dayScore[day] += 10
                        continue
                elif floor != lastFloor:  # if building didn't change but floor change +1
                    dayScore[day] += 1
                    continue

        # add score after calculation
        self.routeScore = sum(dayScore)/len(dayScore)

    # check the instructor list
    def instructorCheck(self, instList, instPref):
        count = 0
        for inst in instPref:
            if inst in instList:
                count += 1
        self.instCheck = count

    # override original deepcopy to deepcopy this object, used in bruteforce
    def __deepcopy__(self, memo):
        return Schedule(copy.deepcopy(self.classList, memo))