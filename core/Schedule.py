import copy
from database.DB import *

class Schedule():
    def __init__(self, classList):
        self.db = DB()
        self.db.useDatabase()
        self.classList = copy.deepcopy(classList)
        self.weekList = [[], [], [], [], []]
        self.inst = None
        self.classLen = None
        self.routeRank = None
        self.score = None
        self.priority = ['School Day', 'Length of Class', 'Start Time', 'End Time', 'Instructor'] # This is default
        self.priorityCheck = None

    '''
    Priority type:
    School Day(indicating value): match and extra day off(3), match(2), no match but have day off(1), no day off(0)
    Length of Class(indicating value): match(1), not match(0)
    Start Time: base on how many days match (0-5)
    End Time: base on how many days match(0-5)
    Instructor: base on how many instructor that the user doesn't want is in the scheduler(0-5) lower better
    route: value lower the better
    '''

    # check if the schedule match the default priority
    def setupCheck(self):

        # PART 1 - find all the data that is needed
        # add all the days in to a nested list
        weekDay = ['M', 'T', 'W', 'R', 'F']

        # create default value for the priorities
        schoolDay = [1,1,1,1,1]
        notSelectedInst = []
        start = []
        end = []
        classLen = []

        # loop through each class to get data
        for classes in self.classList:
            index = 0 # a index used to access list data
            for day in classes.days: # days contains a list of lesson days
                # start checking each day(mon-fri)
                for i in range(5):
                    if weekDay[index] in day:
                        self.weekList.append((classes.start[index],classes.end[index]))
                index += 1 # increment to the index for next lesson

        # route calculation
        map = self.db.getMap()

    # check if the schedule match the user priority
    def setupCheck(self,priority):
        pass

    # print the crn(s) of the schedule
    def printData(self):
        for classes in self.classList:
            print(classes.crn, end = " ")
        print()

    # check the state of schoolday, start, and end
    def timeCheck(self, schoolDay, start, end):
        classLenList = ["0:50", "1:15"]
        # loop through each day
        for day in self.weekList:
            pass

    # calculate a score for the route
    def routeCal(self):
        # route calculation
        map = self.db.getMap()
        locationList = []
        # create a dictionary of map
        mapDict = {row[0]: row[1] for row in map}

        # loop through each class and append location to list
        for classes in self.classList:
            locationList.append(classes.location)

        # start calculating score
        score = 0
        for i in range(1,len(locationList)):
            Location = locationList[i]
            lastLocation = locationList[i-1]
            building = Location[0:3]
            lastBuilding = lastLocation[0:3]
            area = mapDict[building]
            lastArea = mapDict[lastBuilding]
            floor = Location[4]
            lastFloor = Location[4]

            if building != lastBuilding:
                if area != lastArea:  # if area changed +100
                    score += 100
                else:   # if building change in same area +10
                    score += 10
                    continue
            elif floor != lastFloor:  # if building didn't change but floor change +1
                score += 1
                continue

        # add score after calculation
        self.routeScore = score


    # override original deepcopy to deepcopy this object, used in bruteforce
    def __deepcopy__(self, memo):
        return Schedule(copy.deepcopy(self.classList, memo))