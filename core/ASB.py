from core.Schedule import Schedule
from core.Course import *
from collections import OrderedDict
import copy


# modified A star search with back tracking
# modified part: choose the mandatory course with the least section to start with
# g(): choose the class that prune the least class
# h(): "by constantly deleting all the conflict class in the pool"we achieve the concept of always having the best option for next step.
# backtrack: go back one step if no result until the root is empty
# priority - mandatory -> level limit -> other classes


def ASBAlgo(courseList, lvLimitList, mandatoryList, courseLimit):
    print("> Starting Modified A* algorithm with Back Tracking to find possible schedules...  ", end="")
    # define variables
    courseCount = 0
    priorityCount = [0]
    lvLimitLst = []
    lvLimitCount = []
    poppedCourse = OrderedDict()
    poppedMand = []
    backtrackState = [-1]
    result = []
    lastMand = ''
    lastLv = ''

    # set up the list
    for limit in lvLimitList:
        if limit[1].isnumeric():
            lvLimitLst.append([limit[0], int(limit[1])])
            lvLimitCount.append([limit[0], 0])

    # set up priority count
    if not mandatoryList:
        priorityCount[0] += 1
    if not lvLimitLst:
        priorityCount[0] += 1

    # starting algorithm
    while courseCount != courseLimit:

        # get the courses base on priority
        tempCourse = getCourse(courseList, priorityCount, mandatoryList, lvLimitLst)

        # find the Course with least section
        backtrackFlag = [0]
        courseSelected = findLeastSectionCourse(tempCourse, backtrackFlag)
        updatePriority(courseSelected, priorityCount, mandatoryList, lvLimitLst, lvLimitCount, lastMand, lastLv)
        if not backtrackFlag:
            signal = backtrack(backtrackState, poppedCourse, courseList, lastMand, lastLv, priorityCount, lvLimitCount, mandatoryList, result)
            if signal:
                print("done")
                return  # NO RESULT
            courseCount = backtrackState[0]
            continue

        # find the section that prune the least class
        selectedClass = findLeastPruneClasses(courseSelected,  courseList, lvLimitLst, lvLimitCount, poppedCourse)
        # Append class to result
        result.append(selectedClass)
        courseCount += 1

        # Prune the courseList
        prune(selectedClass, courseList, lvLimitLst, lvLimitCount, poppedCourse)
    print("done")
    return [Schedule(result)]



# returns a temporary course list that contains the course that match the priority
def getCourse(courseList, priorityCount, mandatoryList, lvLimitLst):
    temp = []
    # looking for mandatory courses
    if priorityCount[0] == 0:
        for course in courseList:
            for mandatory in mandatoryList:
                if course.subj == mandatory[0] and course.crse == mandatory[1]:
                    temp.append(course)
        return temp

    # looking for course in the level
    elif priorityCount[0] == 1:
        for course in courseList:
            level = course.subj + course.crse[0]
            for levels in lvLimitLst:
                if level == levels[0]:
                    temp.append(course)
        return temp

    # looking for all class
    else:
        return courseList

# return a course with least classes in it
def findLeastSectionCourse(tempCourse, backtrackFlag):
    # first check if there are any class left, if yes: flag=true, if no flag=false
    for course in tempCourse:
        if len(course.classList) > 0:
            backtrackFlag = 1
            break

    smallestCount = len(tempCourse[0].classList)
    smallestIndex = 0

    # find the course with the least classes
    for i in range(1,len(tempCourse)):
        tempCount = len(tempCourse[i].classList)
        if  tempCount < smallestCount and tempCount > 0:
            smallestCount = tempCount
            smallestIndex = i

    return tempCourse[smallestIndex]

# update the priority list
def updatePriority(courseSelected, priorityCount, mandatoryList, lvLimitLst, lvLimitCount, lastMand, lastLv):
    # when priority is mandatory
    if priorityCount[0] == 0:
        mandCheck(courseSelected, priorityCount, mandatoryList, lastMand)
        lvCheck(courseSelected, priorityCount, lvLimitLst, lvLimitCount, lastLv)
    # when priority is level limit
    elif priorityCount[0] == 1:
        lvCheck(courseSelected, priorityCount, lvLimitLst, lvLimitCount, lastLv)

def mandCheck(courseSelected, priorityCount, mandatoryList, lastMand):
    if priorityCount[0] == 0:
        for i in range(len(mandatoryList)):
            if courseSelected.subj == mandatoryList[i][0] and courseSelected.crse == mandatoryList[i][1]:
                mandatoryList.pop(i)
                break
        if not mandatoryList:
            lastMand += courseSelected.subj + courseSelected.crse
            priorityCount[0] += 1

def lvCheck(courseSelected, priorityCount, lvLimitLst, lvLimitCount, lastLv):
    tempFlag = True
    selectedLevel = courseSelected.subj + courseSelected.crse[0]
    for i in range(len(lvLimitLst)):
        if selectedLevel == lvLimitLst[i][0] and lvLimitCount[i][1] < lvLimitLst[i][1]:
            lvLimitCount[i][1] += 1
            break
    for i in range(len(lvLimitLst)):
        if lvLimitCount[i][1] < lvLimitLst[i][1]:
            tempFlag = False
            break
    if tempFlag:
        if priorityCount[0] == 1:  # don't mess the priority count when it is at mandatory state
            lastLv += courseSelected.subj + courseSelected.crse
            priorityCount[0] += 1


# find the class that will prune the least
def findLeastPruneClasses(courseSelected,  courseList, lvLimitLst, lvLimitCount, poppedCourse):
    smallestCount = pruneCheck(courseSelected.classList[0], courseList, lvLimitLst, lvLimitCount, poppedCourse, 1)
    selectedClass = courseSelected.classList[0]
    for i in range(1,len(courseSelected.classList)):
        tempCount = pruneCheck(courseSelected.classList[i], courseList, lvLimitLst, lvLimitCount, poppedCourse, 1)
        if tempCount < smallestCount:
            smallestCount = tempCount
            selectedClass = courseSelected.classList[i]
    return selectedClass

# prune the course list with the selected class
def prune(selectedClass, courseList, lvLimitLst, lvLimitCount, poppedCourse):
    pruneCheck(selectedClass, courseList, lvLimitLst, lvLimitCount, poppedCourse, 0)

# flag is the control signal, 1: count 0: prune
def pruneCheck(selectedClass, courseList, lvLimitLst, lvLimitCount, poppedCourse, flag):
    count = 0
    tempValue = []
    tempKey = selectedClass.subj + selectedClass.crse

    for course in courseList:
        pruneArray = []
        pruneIndex = 0
        for classes in course.classList:
            # check course conflict
            if classes.crse == selectedClass.crse and classes.subj == selectedClass.subj:
                if flag:
                    count += 1
                    continue
                else:
                    pruneArray.append(pruneIndex)
                    pruneIndex += 1
                    continue

            # check time conflict
            timeFlag = False
            for i in range(len(selectedClass.days)):  # iterate through days in selected
                for selectedDay in selectedClass.days[i]:  # iterate each day in the days
                    for j in range(len(classes.days)):  # iterate through days in classes
                        if selectedDay in classes.days[j]:
                            if selectedClass.start[i] >= classes.start[j] and selectedClass.start[i] <= classes.end[j] \
                                or selectedClass.end[i] >= classes.end[j] and selectedClass.end[i] <= classes.end[j]:
                                if flag:
                                    count += 1
                                    timeFlag = True
                                    break
                                else:
                                    pruneArray.append(pruneIndex)
                                    pruneIndex += 1
                                    timeFlag = True
                                    break
                    if timeFlag:
                        break
                if timeFlag:
                    break
            if timeFlag:
                continue

            # check if it is itself
            if classes.crn == selectedClass.crn:
                if flag:
                    count += 1
                    continue
                else:
                    pruneArray.append(pruneIndex)
                    pruneIndex += 1
                    continue

            # check level conflict
            selectedLevel = selectedClass.subj + selectedClass.crse[0]
            level = classes.subj + classes.crse[0]
            lvflag = False
            for i in range(len(lvLimitLst)):
                if selectedLevel == lvLimitLst[i][0]:
                    if level == lvLimitLst[i][0] and lvLimitCount[i][1] + 1 == lvLimitLst[i][1]:
                        if flag:
                            count += 1
                            lvflag = True
                            break
                        else:
                            pruneArray.append(pruneIndex)
                            pruneIndex += 1
                            lvflag = True
                            break
            if lvflag:
                continue

        # prune the course first before going to next course
        if not flag:
            popCourse = createPopCourse(course.subj, course.crse)
            for index in pruneArray:
                if selectedClass.crn != course.classList[index].crn:  # we don't want the selected class in the trash can
                    popCourse.classList.append(course.classList[index])
                course.classList.pop(index)
            tempValue.append(popCourse)

    if flag:
        return count
    else:
        poppedCourse[tempKey] = tempValue

# create a course with empty classList for storing popped course
def createPopCourse(subj, crse):
    course = Course(subj, crse)
    course.setClassList([])
    return course

# resume to previous state
def backtrack(backtrackState, poppedCourse, courseList, lastMand, lastLv, priorityCount, lvLimitCount, mandatoryList, result):
    # a signal that indicates if there are no result or the courseList is restored
    signal = 0
    # initialize backtrack count
    if backtrackState[0] == -1:
        backtrackState[0] = len(poppedCourse)-1

    # restore popped course to course list
    # first check if popped course is empty
    # if it is at root and empty = no result
    # if not at root but empty = go one level up -> count -= 1
    isEmpty = True
    for course in poppedCourse:
        if len(poppedCourse.classList) > 0:
            isEmpty = False
            break

    if backtrackState[0] > 0 and isEmpty:
        backtrackState[0] -= 1
    elif backtrackState[0] == 0 and isEmpty:
        signal = 1
        return signal

    restore(backtrackState, poppedCourse, courseList, lastMand, lastLv, priorityCount, lvLimitCount, mandatoryList,  result)
    return signal

# start restoring the poppedCourse from the bottom
def restore(backtrackState, poppedCourse, courseList, lastMand, lastLv, priorityCount, lvLimitCount, mandatoryList,  result):
    for i in range(len(poppedCourse)-1, backtrackState[0]-1, -1):
        print(len(poppedCourse)-1)
        print(backtrackState[0]-1)
        print(poppedCourse)
        print(i)
        key = getKey(poppedCourse, i)
        # restore priority
        if key == lastLv:
            priorityCount[0] = 1
        elif key == lastMand:
            priorityCount[0] = 0
        # restore course
        for popped in poppedCourse[key]:
            for course in courseList:
                if popped.subj == course.subj and popped.crse == course.crse:
                    # restore mandatoryList and lvLimitLst
                    if priorityCount[0] < 2:
                        poppedLevel = popped.subj + popped.crse[0]
                        for levels in lvLimitCount:
                            if poppedLevel == levels[0]:
                                levels[1] -= 1
                    if priorityCount[0] == 0:
                        mandatoryList.append((popped.subj, popped.crse, 1))
                    tempClassList = course.classList + popped.classList
                    course.setClassList(tempClassList)

    for i in range(len(poppedCourse)-1, backtrackState[0]-1, -1):
        key = getKey(poppedCourse, i)
        # pop the poppedCourse dict
        poppedCourse.pop(key)
        # pop the result
        result = result.pop[i]

def getKey(dict, n):
    items = list(dict.items())
    return items[n][0]