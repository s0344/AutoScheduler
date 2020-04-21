# this file is used to import data from csv file to the database
import csv
import pymysql


class DB():
    # connect to database
    def __init__(self, host="localhost", user="root", passwd="root"):
        # connect to mysql server and database
        self.db = pymysql.connect(
            host=host,
            user=user,
            passwd=passwd
        )

    def useDatabase(self):
        self.cur = self.db.cursor()
        self.cur.execute("USE courses")
        self.cur.close()

    def createDatabase(self):
        # create cursor to communicate with database
        self.cur = self.db.cursor()

        # create or enter database
        try:
            self.cur.execute("USE courses")
            self.cur.close()
            return 0
        except:
            self.cur.execute("CREATE DATABASE courses")
            self.cur.execute("USE courses")
            # create tables
            self.cur.execute("CREATE TABLE IF NOT EXISTS subject(\
                                                subj VARCHAR(4),\
                                                primary key(subj))")

            self.cur.execute("CREATE TABLE IF NOT EXISTS classes(\
                                                prereq1 VARCHAR(20),\
                                                prereq2 VARCHAR(20),\
                                                prereq3 VARCHAR(20),\
                                                subj VARCHAR(4),\
                                                crse VARCHAR(3),\
                                                level VARCHAR(3),\
                                                cred VARCHAR(1),\
                                                title VARCHAR(100),\
                                                primary key(subj,crse),\
                                                foreign key(subj) references subject(subj) on delete cascade)")

            self.cur.execute("CREATE TABLE IF NOT EXISTS section(\
                                                crn VARCHAR(4),\
                                                subj VARCHAR(4),\
                                                crse VARCHAR(3),\
                                                sec VARCHAR(2),\
                                                rem VARCHAR(2),\
                                                inst VARCHAR(50),\
                                                date VARCHAR(11),\
                                                primary key(crn),\
                                                foreign key(subj,crse) references classes(subj,crse) on delete cascade)")

            self.cur.execute("CREATE TABLE IF NOT EXISTS lesson(\
                                                crn VARCHAR(4),\
                                                days VARCHAR(5),\
                                                start VARCHAR(5),\
                                                end VARCHAR(5),\
                                                location VARCHAR(8),\
                                                primary key(crn, days, start, end, location),\
                                                foreign key(crn) references section(crn) on delete cascade)")

            self.cur.execute("CREATE TABLE IF NOT EXISTS map(\
                                                building VARCHAR(3),\
                                                area VARCHAR(1),\
                                                primary key(building))")
            self.db.commit()
            self.cur.close()
            return 1

    def importData(self, fileName, flag):
        if flag:
            # create self.cursor to communicate with database
            self.cur = self.db.cursor()

            # queries for inserting data into the tables
            subjectSql = "INSERT IGNORE INTO subject (subj) VALUES (%s)"
            classesSql = "INSERT IGNORE INTO " \
                         "classes (prereq1, prereq2, prereq3, subj, crse, level, cred, title) " \
                         "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            sectionSql = "INSERT IGNORE INTO " \
                         "section (crn, subj, crse, sec, rem, inst, date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            lessonSql = "INSERT INTO lesson (crn, days, start, end, location) VALUES (%s,%s,%s,%s,%s)"
            mapSql = "INSERT INTO map(building, area) VALUES (%s,%s)"

            print(fileName)
            print(type(fileName))
            print(fileName == 'map.csv')

            if fileName == 'map.csv':
                print("map in")
                # reading the classes into value and store the data to database through quries
                with open(fileName) as file:
                    reader = csv.reader(file, delimiter=',')
                    line = 0
                    for row in reader:
                        if line:
                            building = row[0]
                            area = row[1]
                            mapData = (building, area)
                            self.cur.execute(mapSql, mapData)
                        line += 1
                    print(fileName + ' process ended')
            else:
                # reading the classes into value and store the data to database through quries
                with open(fileName) as file:
                    reader = csv.reader(file, delimiter=',')
                    line = 0
                    for row in reader:
                        if line:
                            prereq1 = row[0]
                            prereq2 = row[1]
                            prereq3 = row[2]
                            crn = row[3]
                            subj = row[4]
                            crse = row[5]
                            sec = row[6]
                            cred = row[7]
                            title = row[8]
                            days = row[9]
                            start = row[10]
                            end = row[11]
                            rem = row[12]
                            inst = row[13]
                            date = row[14]
                            location = row[15]

                            # calculate level
                            level = crse[0] + "00"

                            subjectData = subj
                            classesData = (prereq1, prereq2, prereq3, subj, crse, level, cred, title)
                            sectionData = (crn, subj, crse, sec, rem, inst, date)
                            lessonData = (crn, days, start, end, location)
                            self.cur.execute(subjectSql, subjectData)
                            self.cur.execute(classesSql, classesData)
                            self.cur.execute(sectionSql, sectionData)
                            self.cur.execute(lessonSql, lessonData)
                        line += 1
                    print(fileName + ' process ended')

            self.db.commit()
            self.cur.close()

    def getSubject(self):
        self.cur = self.db.cursor()
        sql = "select * from subject;"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        # result = list(result)
        result = [item[0] for item in result]
        self.cur.close()
        return result

    # return the levels of subject
    def getLevel(self, subj):
        self.cur = self.db.cursor()
        sql = "select distinct subj, level from classes where subj = %s"
        var = subj
        self.cur.execute(sql, var)
        result = self.cur.fetchall()
        result = [item[1] for item in result]
        self.cur.close()
        return result

    # return the classes of subject-level
    def getCourse(self, subj, level):
        self.cur = self.db.cursor()
        sql = "select distinct subj, crse from classes where subj = %s and level = %s"
        var = (subj, level)
        self.cur.execute(sql, var)
        result = self.cur.fetchall()
        result = [item[1] for item in result]
        self.cur.close()
        return result

    # return the classes of subject-course#
    def getTitle(self, subj, crse):
        self.cur = self.db.cursor()
        sql = "select title from classes where subj = %s and crse = %s"
        var = (subj, crse)
        self.cur.execute(sql, var)
        result = self.cur.fetchall()
        result = [item[0] for item in result]
        self.cur.close()
        return result

    # return distinct Instructor of subject-course#
    def getInst(self, subj, crse):
        self.cur = self.db.cursor()
        sql = "select distinct inst from section where subj = %s and crse = %s"
        var = (subj, crse)
        self.cur.execute(sql, var)
        result = self.cur.fetchall()
        result = [item[0] for item in result]
        self.cur.close()
        return result

    def getMap(self):
        self.cur = self.db.cursor()
        sql = "select * from map"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.cur.close()
        return result

    # return data that is needed for course object
    def getClassData(self, crn):
        self.cur = self.db.cursor()
        sql = "select crn,subj,crse,rem,inst,days,start,end,location,date,prereq1,prereq2,prereq3,sec " \
              "from classes natural join section natural join lesson where crn = %s"
        var = (crn)
        self.cur.execute(sql, var)
        result = self.cur.fetchall()
        self.cur.close()
        return result

    # return the count of lesson for each crn
    def getLessonCount(self, subj, crse):
        self.cur = self.db.cursor()
        sql = "select crn, count(*) " \
              "from classes natural join section natural join lesson where subj = %s and crse = %s and start <> %s " \
              "group by crn;"
        var = (subj, crse,"TBA")
        self.cur.execute(sql, var)
        result = self.cur.fetchall()
        self.cur.close()
        return result

    # return prerequisites of course
    def getPrereq(self, subj, crse):
        self.cur = self.db.cursor()
        sql = "select prereq1, prereq2, prereq3 from classes where subj = %s and crse = %s"
        var = (subj, crse)
        self.cur.execute(sql, var)
        result = self.cur.fetchall()
        result = result[0]
        self.cur.close()
        return result

    def getCourse_TimeTBA(self):
        self.cur = self.db.cursor()
        sql = "select subj, crse from section where crn in (select distinct crn from lesson where start = 'TBA')"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.cur.close()
        return result

    # close the database connection
    def close(self):
        self.db.close()