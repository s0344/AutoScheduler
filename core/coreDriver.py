from core.Course import *
from core.bruteForce import bruteForceExecute

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
    instList = []
    priority = data.getPriority()
    schoolDay = data.getSchoolDay()
    dayStart = []
    dayEnd = []
    classLen = data.getClassLen()
    print("done")

    # convert day start and end from string to timedelta object
    print("> preference start time convert...  ", end="")
    for time in data.getStartTime():
        dayStart.append(datetime.strptime(time,"%H:%M"))
    print("done")

    print("> preference end time convert...  ", end="")
    for time in data.getEndTime():
        dayEnd.append(datetime.strptime(time, "%H:%M"))
    print("done")

    # adding data to a course list
    print("> Adding data to course list...  ", end="")
    for subjLv in course:
        crseList = subjLv.crseList
        lvLimitList.append((subjLv.subj, subjLv.lv, subjLv.lvLimit))
        for crse in crseList:
            if int(crse.mandatory):
                mandatoryList.append((subjLv.subj, crse.crseNum, crse.mandatory))
            courseList.append(Course(subjLv.subj, crse.crseNum))

    print("done")

    print("> printing mandatory class")
    for mandClass in mandatoryList:
        print("     ", mandClass[0], mandClass[1])

    # concat all the classes into a class list
    print("> creating class list...  ", end="")
    for course in courseList:
        classList += course.classList
    print("done")

    # use bruteforce function
    print("> class list length is: ", len(classList))
    print("> course limit is: ", int(courseLimit))
    scheduleList = bruteForceExecute(classList, len(classList), int(courseLimit),mandatoryList)
    print("> # of resulted schedule: ", len(scheduleList) )
    print("> printing results")
    count = 1
    for schedule in scheduleList:
        print("     schedule",count,end=": ")
        schedule.printData()
        count += 1
        print()


       # preference rating


