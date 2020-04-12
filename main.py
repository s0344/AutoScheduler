import sys
from mainWindow import *
from pResult import Dialog_sort


def openChild():
    child = Dialog_sort(window)
    child.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    child = Dialog_sort(window)

    btnSort = window.pResult.buttonSort
    btnSort.clicked.connect(lambda: openChild())


    window.show()
    sys.exit(app.exec_())
