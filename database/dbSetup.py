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
