class Result():
    def __init__(self, scheduleList):
        self.scheduleList = scheduleList
        self.priority = ['School Day', 'Route Score', 'Length of Class', 'Start Time', 'End Time', 'Instructor']  # This is default

    def rank(self, data):
        # update check
        for schedule in self.scheduleList:
            schedule.updateCheck(self, data)

        # make a function list base on priority
        priority = data.getPriority()
        funcList = []
        for prio in priority:
            if prio == 'School Day':
                funcList.append(self.schoolDayRank)
            elif prio == 'Route Score':
                funcList.append(self.routeRank)
            elif prio == 'Length of Class':
                funcList.append(self.classLenRank)
            elif prio == 'Start Time':
                funcList.append(self.startTimeRank)
            elif prio == 'End Time':
                funcList.append(self.endTimeRank)
            elif prio == 'Instructor':
                funcList.append(self.instRank)

        # call the first function
        index = 0
        funcList[index](self, data, funcList, index)


    # rank day off classes: match and extra day off(3), match(2), no match but have day off(1), no dayoff(0)
    def schoolDayRank(self, data, funcList, index):
        pass

    def classLenRank(self, data, funcList, index):
        pass

    def startTimeRank(self, data, funcList, index):
        pass

    def endTimeRank(self, data, funcList, index):
        pass

    def instRank(self, data, funcList, index):
        pass

    def routeRank(self, data, funcList, index):
        pass