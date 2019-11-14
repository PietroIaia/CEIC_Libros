from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor
from Prompt import ErrorPrompt
###################################################
#           Tabla de libros de un autor           #
###################################################

class AuthorSearchTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2) #Columnas
        self.setRowCount(10)
        self.setHorizontalHeaderLabels(["Título", "Código"])
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setColumnWidth(0, 500)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def getQTableWidgetSize(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

    def setTableColors(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem())
                self.item(i, j).setBackground(QColor(224, 255, 255))

    def clear_table(self):
        self.table.setRowCount(5)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                self.item(i, j).setBackground(QColor(224, 255, 255))
