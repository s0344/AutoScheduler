from database.DB import *
from core.Course import *


if __name__ == '__main__':

    csFile = 'cs.csv'
    langFile = 'lang.csv'
    rootsFile = 'roots.csv'
    mapFile = 'map.csv'

    testdb = DB()
    flag = testdb.createDatabase()  # return 1 if database is newly created, 0 if database already created
    testdb.importData(csFile, flag)
    testdb.importData(langFile, flag)
    testdb.importData(rootsFile, flag)
    testdb.importData(mapFile, flag)

    testdb.close()


    '''
    l1 = testdb.getSubject()
    l2 = testdb.getLevel("CMPT")
    l3 = testdb.getCourse("CMPT", "100")
    l4 = testdb.getTitle("CMPT", "101")
    l5 = testdb.getInst("CMPT", "101")
    map = testdb.getMap()

    print("hello")
    for row in map:
        print(row[0],row[1])


    mapDict = {row[0]:row[1] for row in map}
    print(mapDict)
    print("hello")
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
    
    
    c = Course("CMPT","239","1")
    for classes in c.classList:
        classes.printDetailData()
        classes.printSimpleData()
        
        
      class idk():
        def __init___(self):

    def sth():
        # empty nested list: match and extra day off(3), match(2), no match but have day off(1), no dayoff(0)
        list = {}
        values = [12,48,1,9,10]
        me = ["me1", "me2", "me3", "me4", "me5"]
        length = len(me)
        for i in range(length):
            list[me[i]] = values[i]


        print(list)

    sth()

    '''
