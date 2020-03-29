from database.DB import *
from core.Course import *
from core.coreDriver import core

if __name__ == '__main__':
    '''
    csFile = 'cs.csv'
    langFile = 'lang.csv'
    rootsFile = 'roots.csv'

    testdb = DB()
    flag = testdb.createDatabase()  # return 1 if database is newly created, 0 if database already created
    testdb.importData(csFile, flag)
    testdb.importData(langFile, flag)
    testdb.importData(rootsFile, flag)

    l1 = testdb.getSubject()
    l2 = testdb.getLevel("CMPT")
    l3 = testdb.getCourse("CMPT", "100")
    l4 = testdb.getTitle("CMPT", "101")
    l5 = testdb.getInst("CMPT", "101")

    print(l1)
    #print(type(l1))
    # print(l1[1][0])
    # print(l1[1])
    print(l2)
    # print(l2[1][0])
    # print(l2[1])
    print(l3)
    # print(l3[1][0])
    # print(l3[1])
    print(l4)
    print(l5)

    r1 = testdb.getClassData("8197")
    r2 = testdb.getLessonCount("CMPT","239")

    print(r1)
    print(type(r1))
    print(r1[0][5])
    print(r1[1][5])
    print(r2)
    print(type(r2))
    print(r2[0][0])
    print(r2[1][0])

    print(len(r1))
    print(len(r2))

    for i in r2:
        for j in range(2):
            print(i[j],end=" ")
        print()

    starttime = datetime.strptime(r1[0][6], '%H:%M')
    endtime = datetime.strptime(r1[0][7], '%H:%M')
    print(starttime)
    print(endtime-starttime)

    testdb.close()
    '''

    c = Course("CMPT","239","1")
    for classes in c.classList:
        classes.printDetailData()
        classes.printSimpleData()
    '''
    test = ""
    test1 = "123"
    test2 = "123+345"

    data = test.split("+")
    data1 = test1.split("+")
    data2 = test2.split("+")

    print(data)
    print(data1)
    print(data2)
    '''