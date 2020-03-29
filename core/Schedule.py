import copy


class Schedule():
    def __init__(self, classList):
        self.classList = copy.deepcopy(classList)
        self.mon = None
        self.tue = None
        self.wed = None
        self.thu = None
        self.fri = None
        self.inst = None
        self.classLen = None
        self.routeRank = None
        self.score = None
        self.priority = ['School Day', 'Length of Class', 'Start Time', 'End Time', 'Instructor'] # This is default
        self.priorityCheck = None

    # check if the schedule match the default priority
    def setupCheck(self):
        defaultPrio = ['School Day', 'Length of Class', 'Start Time', 'End Time', 'Instructor']

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