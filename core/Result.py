class Result():
    def __init__(self, scheduleList):
        self.scheduleList = scheduleList

    def rank(self, data):
        # update check
        for schedule in self.scheduleList:
            schedule.updateCheck(data)

        # make a function list base on priority
        priority = data.getPriority()
        funcList = []
        for eachPrio in priority:
            if eachPrio == 'School Day':
                funcList.append(self.schoolDayRank)
            elif eachPrio == 'Length of Class':
                funcList.append(self.classLenRank)
            elif eachPrio == 'Start Time':
                funcList.append(self.startTimeRank)
            elif eachPrio == 'End Time':
                funcList.append(self.endTimeRank)
            elif eachPrio == 'Instructor':
                funcList.append(self.instRank)

        # call the first function
        index = 0
        maxIndex = len(priority) - 1
        newScheduleList = []
        funcList[index](newScheduleList, self.scheduleList, funcList, index, maxIndex)
        self.scheduleList = newScheduleList

    def schoolDayRank(self, newScheduleList, scheduleList, funcList, index, maxIndex):
        # empty nested list: match and extra day off(3), match(2), no match but have day off(1), no dayoff(0)
        list = [[] for _ in range(4)]

        # split up list
        switcher = { # kinda like switch statement
            3: 0,
            2: 1,
            1: 2,
            0: 3,
        }
        for schedule in scheduleList:
            i = switcher.get(schedule.schoolDayCheck)
            list[i].append(schedule)

        # check first if this is the leaf node (lowest level), if yes: rank route score and return
        if index == maxIndex:
            # start ranking all sublist with route score
            for sublist in list:
                sublist = self.routeRank(sublist)
                newScheduleList += sublist
            return

        # if it is not last node, call next function
        for sublist in list:
            if len(sublist) > 1:  # when more than one schedule in the sublist go to next
                funcList[index + 1](newScheduleList, sublist, funcList, index + 1, maxIndex)
            elif len(sublist) == 1:  # when there is only one schedule, append
                newScheduleList += sublist

    def classLenRank(self, newScheduleList, scheduleList, funcList, index, maxIndex):
        # empty nested list: match(1), not match(0)
        list = [[] for _ in range(2)]

        # split up list
        switcher = {  # if match, store in first list etc.
            1: 0,
            0: 1,
        }
        for schedule in scheduleList:
            i = switcher.get(schedule.schoolDayCheck)
            list[i].append(schedule)

        # check first if this is the leaf node (lowest level), if yes: rank route score and return
        if index == maxIndex:
            # start ranking all sublist with route score
            for sublist in list:
                sublist = self.routeRank(sublist)
                newScheduleList += sublist
            return

        # if it is not last node, call next function
        for sublist in list:
            if len(sublist)>1:  # when more than one schedule in the sublist go to next
                funcList[index + 1](newScheduleList, sublist, funcList, index + 1, maxIndex)
            elif len(sublist)==1:  # when there is only one schedule, append
                newScheduleList += sublist

    def startTimeRank(self, newScheduleList, scheduleList, funcList, index, maxIndex):
        # empty nested list: base on how many days match (5-0)
        list = [[] for _ in range(6)]

        # split up list
        switcher = {  # if all match, store in first list etc.
            5: 0,
            4: 1,
            3: 2,
            2: 3,
            1: 4,
            0: 5,
        }
        for schedule in scheduleList:
            i = switcher.get(schedule.schoolDayCheck)
            list[i].append(schedule)

        # check first if this is the leaf node (lowest level), if yes: rank route score and return
        if index == maxIndex:
            # start ranking all sublist with route score
            for sublist in list:
                sublist = self.routeRank(sublist)
                newScheduleList += sublist
            return

        # if it is not last node, call next function
        for sublist in list:
            if len(sublist)>1:  # when more than one schedule in the sublist go to next
                funcList[index + 1](newScheduleList, sublist, funcList, index + 1, maxIndex)
            elif len(sublist)==1:  # when there is only one schedule, append
                newScheduleList += sublist

    def endTimeRank(self, newScheduleList, scheduleList, funcList, index, maxIndex):
        # empty nested list: base on how many days match (5-0)
        list = [[] for _ in range(6)]

        # split up list
        switcher = {  # if all match, store in first list etc.
            5: 0,
            4: 1,
            3: 2,
            2: 3,
            1: 4,
            0: 5,
        }
        for schedule in scheduleList:
            i = switcher.get(schedule.schoolDayCheck)
            list[i].append(schedule)

        # check first if this is the leaf node (lowest level), if yes: rank route score and return
        if index == maxIndex:
            # start ranking all sublist with route score
            for sublist in list:
                sublist = self.routeRank(sublist)
                newScheduleList += sublist
            return

        # if it is not last node, call next function
        for sublist in list:
            if len(sublist)>1:  # when more than one schedule in the sublist go to next
                funcList[index + 1](newScheduleList, sublist, funcList, index + 1, maxIndex)
            elif len(sublist)==1:  # when there is only one schedule, append
                newScheduleList += sublist

    def instRank(self, newScheduleList, scheduleList, funcList, index, maxIndex):
        # empty nested list: no unwant instructer in list(0), one(1), two(2), three+(3)
        list = [[] for _ in range(4)]

        # split up list
        switcher = {  # if all match, store in first list etc.
            0: 0,
            1: 1,
            2: 2,
        }
        for schedule in scheduleList:
            i = switcher.get(schedule.schoolDayCheck,3)
            list[i].append(schedule)

        # check first if this is the leaf node (lowest level), if yes: rank route score and return
        if index == maxIndex:
            # start ranking all sublist with route score
            for sublist in list:
                sublist = self.routeRank(sublist)
                newScheduleList += sublist
            return

        # if it is not last node, call next function
        for sublist in list:
            if len(sublist)>1:  # when more than one schedule in the sublist go to next
                funcList[index + 1](newScheduleList, sublist, funcList, index + 1, maxIndex)
            elif len(sublist)==1:  # when there is only one schedule, append
                newScheduleList += sublist

    # always run at the end of one node
    def routeRank(self, sublist):
        # create list of tuples to sort
        sort = {}
        # create new list to store the sorted list
        result = []

        # put data into the tuple list for sorting
        length = len(sublist)
        for i in range(length):
            sort[sublist[i]] = sublist[i].routeScore

        # perform sorting
        sortedList = sorted(sort.items, key=lambda x: x[1])

        # put the sorted dictionary to result
        for tuple in sortedList:
            result.append(tuple[0])

        return result

    def printResult(self):
        index = 0
        weekDay = ['M', 'T', 'W', 'R', 'F']
        for schedule in self.scheduleList:
            print("Schedule ", index, ": ")
            print("Time table: ")
            for i in range(5):
                print(weekDay[i], end= ": ")
                for classtime in schedule.weekList[i]:
                    print("(" , classtime[0].time() , classtime[0].time() , "), ")
                print()
            print("School Day Check: ", schedule.schoolDayCheck)
            print("Start Time Check: ", schedule.startCheck)
            print("End Time Check: ", schedule.endCheck)
            print("Class Length Check: ", schedule.classLenCheck)
            print("Instructor Check: ", schedule.instCheck)
            print("Route Score: ", schedule.routeScore)
            print("=============================================================================")