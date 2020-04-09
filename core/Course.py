from database.DB import *
from core.Classes import *
import copy

class Course():
    def __init__(self, subj, crse):
        # connect to database
        self.db = DB()
        self.db.useDatabase()
        self.subj = subj
        self.crse = crse
        self.classList = self.createClassList(subj, crse)
        self.db.close()

    def createClassList(self, subj, crse):
        data = self.db.getLessonCount(subj, crse)
        list = []
        for i in data:
            tempClass = Classes(i[0])
            if int(tempClass.rem) > 0:
                list.append(Classes(i[0]))
        return list

    def setClassList(self, newClassList):
        self.classList = newClassList
