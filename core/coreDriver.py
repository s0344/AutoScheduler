from core.Course import *
from core.bruteForce import bruteForceExecute
from core.Result import *

# this is the driver code for the core, takes UIdata as input, returns a result object
def coreDriver(data):

    # define variables
    print("> defining variables...  ", end="")
    course = data.getCourses()
    courseList = []
    classList = []
    mandatoryList = []

    # preference variables
    lvLimitList = []
    courseLimit = data.getCourseLimit()
    print("done")

    # adding data to a course list
    print("> Adding data to course list...  ", end="")
    for subjLv in course:
        crseList = subjLv.crseList
        lvLimitList.append((subjLv.subj + subjLv.lv[0], subjLv.lvLimit))
        for crse in crseList:
            if int(crse.mandatory):
                mandatoryList.append((subjLv.subj, crse.crseNum, crse.mandatory))
            courseList.append(Course(subjLv.subj, crse.crseNum))

    print("done")

    lvLimitList = dict(lvLimitList)

    print("> printing mandatory class")
    for mandClass in mandatoryList:
        print("     ", mandClass[0], mandClass[1])

    # concat all the classes into a class list
    print("> creating class list...  ", end="")
    for course in courseList:
        classList += course.classList
    print("done")

    # if class time is TBA, don't take it into account
    print("> Popping classes with TBA time...  ", end="")
    for classes in classList:
        if classes.start == "TBA":
            classList.pop(classes)
    print("done")

    # use bruteforce function
    print("> class list length is: ", len(classList))
    print("> course limit is: ", int(courseLimit))
    scheduleList = bruteForceExecute(classList, len(classList), int(courseLimit),mandatoryList, lvLimitList)
    print("> # of resulted schedule: ", len(scheduleList))
    print("> printing results")
    count = 1
    for schedule in scheduleList:
        print("     schedule",count,end=": ")
        schedule.printData()
        count += 1
        print()

    print("> Adding schedule list to result...", end="")
    result = Result(scheduleList)
    print("done")

    print("> ranking Result...", end="")
    result.rank(data)
    print("done")

    print("> printing results")
    result.printResult()


