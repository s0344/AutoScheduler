from core.Course import *
import os

if __name__ == '__main__':

    dir = os.getcwd()   # current directory
    print(dir)
    fileList = os.listdir(dir)  # files in current directory
    print(fileList)

    testdb = DB()
    flag = testdb.createDatabase()  # return 1 if database is newly created, 0 if database already created

    for file in fileList:
        if file[-4:] == '.csv': # only read the .csv file
            print(file)
            testdb.importData(file, flag)
    testdb.close()
