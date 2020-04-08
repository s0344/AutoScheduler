from core.Course import *
from core.bruteForce import bruteForceExecute
from core.Result import *

# this is the driver code for the core, takes UIdata as input, returns a result object
def coreDriver(data, flag):

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
        lvLimitList.append((subjLv.subj + subjLv.lv[0], subjLv.lvLimit, 0))
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

    # use bruteforce function if flag == 1, use modified A star search with back tracking if flag == 0
    if flag:
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
        return result
    else:
        print("> pruning course list...  ", end="")
        weekDay = ['M', 'T', 'W', 'R', 'F']
        schoolDayPref = data.getSchoolDay()
        instPref = data.getNotSelectedInst()
        startPref = data.getStartTime()
        endPref = data.getEndTime()
        classLenPref = data.getClassLen()
        classLenRef = ["0:50", "1:15", "2:45"]

        # prune the class first to reduce the size of initial data
        for course in courseList:
            for i in range(len(classList)):
                flag = False

                # pop the class if not match day pref
                # if pref is 0 than find if that day is in class.days, if in, pop
                # after pop, set flag to true and break loop so it can go to next class
                for j in range(5):
                    if not schoolDayPref[j]:
                        for day in course.classList[i].days:
                            if weekDay[j] in day:
                                course.classList.pop(i)
                                flag = True
                                break
                    if flag:
                            break
                if flag:
                    continue

                # pop the class if not match instructor pref
                # if the inst is same, pop, set flag to continue
                for inst in instPref:
                    if inst == course.classList[i].inst:
                        course.classList.pop(i)
                        flag = True
                        break
                if flag:
                        continue

                # check start time and end time
                for j in range(5):
                    count = 0
                    for day in course.classList[i].days:
                        if weekDay[j] in day:
                            if course.classList[i].start[count] < startPref[j] or course.classList[i].end[count] > endPref[j]:
                                course.classList.pop(i)
                                flag = True
                                break
                        count += 1
                    if flag:
                            break
                if flag:
                        continue

                # check class length
                for j in range(3):
                    if not classLenPref[j]:
                        for classLen in course.classList[i].classTime:
                            if classLenRef[j] == classLen:
                                course.classList.pop(i)
                                flag = True
                                break
                    if flag:
                            break
                if flag:
                        continue

        # now we done with pruning the courseList, we can send it to the algorithm







