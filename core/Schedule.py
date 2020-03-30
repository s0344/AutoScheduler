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

    # override original deepcopy to deepcopy this object, used in bruteforce
    def __deepcopy__(self, memo):
        return Schedule(copy.deepcopy(self.classList, memo))