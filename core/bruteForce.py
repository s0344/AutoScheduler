from core.Schedule import Schedule
import time
import random

# In order to generate all possible course
# we chosen a Brute Force method as our Resource Allocation Algorithm
# It will return a schedule list
def bruteForceExecute(classList, classListLen, courseLimit, mandatoryList, lvLimitList):
    # shuffle the classList
    random.shuffle(classList)

    # Temporary classListay to store combination
    temp = [0] * courseLimit
    scheduleList = []
    # bruteForce function will store the result in the scheduleList
    print("> Starting brute force algorithm to find possible schedules...  ")
    startTime = time.time()
    bruteForce(classList, temp, 0, classListLen - 1, 0, courseLimit, scheduleList, mandatoryList,lvLimitList, True, startTime)
    print("  done")
    return scheduleList


# classList[]: A list of classes
# temp[]: Temporary list for one combination
# start & end: Staring and Ending indexes in classList[]
# index: Current index in temp[]
# courseLimit: Size of a combination
# schedulist: such that each result could append to the schedule list
# mandatoryList: use to check if all the mandatory class in schedule
def bruteForce(classList, temp, start, end, index, courseLimit, scheduleList, mandatoryList, lvLimitList, flag, startTime):
    checkTime = time.time()
    elapsed = checkTime - startTime
    if elapsed > 300:
        return

    # When the result is ready, check list and append to schedule list
    if (index == courseLimit):
        if checkClasses(temp, mandatoryList,lvLimitList):
            scheduleList.append(Schedule(temp))
        return

    i = start
    while (i <= end and end - i + 1 >= courseLimit - index):
        # print("while loop in")
        temp[index] = classList[i]
        bruteForce(classList, temp, i + 1, end, index + 1, courseLimit, scheduleList, mandatoryList, lvLimitList, False, startTime)
        if flag:
            print("  progress at branch", i+1)
        i += 1


# This function check through the previous class to see if there are any conflicts
# Conflicts: same course, day time conflict, missing mandatory course, check level limit
# True: there is NO conflict  False: there is a conflict

def checkClasses(temp, mandatoryList, lvLimitList):

    # check course conflict
    courseSet = set()
    for classes in temp:
        courseStr = classes.subj + classes.crse
        if courseStr in courseSet:
            return False
        else:
            courseSet.add(courseStr)

    # check if all the mandatory class is in the schedule
    # if the mandatory course is not in the schedule's course set, return false
    for mandClass in mandatoryList:
        courseStr = mandClass[0] + mandClass[1]
        if courseStr not in courseSet:
            return False

    # check day time conflict
    weekList = [[], [], [], [], []]  # contains list for each days which also should be a list
    weekDay = ['M', 'T', 'W', 'R', 'F']

    def dayTimeConflict(day, dayList, classDay, start, end):
        if day in classDay:  # e.g. if M exist in "MTF" => which returns true
            # start looping through that day see if there is conflict, yes then
            # return false, no then add to the list
            for timeRange in dayList:
                # if there are conflicts:
                if start >= timeRange[0] and start <= timeRange[1] \
                        or end >= timeRange[0] and end <= timeRange[1]:
                    return True  # return true for the check process outside to end
            # after check no conflict in that day add to list
            dayList.append((start, end))

    for classes in temp:  # loop through each class in the temp class list
        j = 0;  # A count that use as the index of different lesson days e.g. ["MTF","W"] then "MTF" is 0, "W" is 1, used for the start and end
        for day in classes.days:  # days contains a list of lesson days e.g. ["MTF","W"]
            # start checking each day(mon-fri)
            for i in range(5):
                if dayTimeConflict(weekDay[i], weekList[i], day, classes.start[j], classes.end[j]):
                    return False
            j += 1

    # check level limit
    level = {}
    for classes in temp:
        levelstr = classes.subj + " " + classes.crse[0]
        if not lvLimitList[levelstr].isnumeric():   # check if it should be ignored
            continue
        else:  # when it shouldn't be ignored
            if levelstr in level.keys():  # check if the key exist, false: create new dict, true: dict +1
                if int(lvLimitList[levelstr]) > level[levelstr]:  # check if the count reach the limit yet
                    level[levelstr] += 1
                else:
                    return False
            else:
                level.update({levelstr: 1})

    return True
