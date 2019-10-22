#CEIC Libros
#Tabla de estudiantes
#Desarrollado por Forward
#Responsable del módulo: Diego Peña, 15-11095
#Fecha de inicio: 21-10-19, Apróx 8:20 am, Hora de Venezuela
#Última modifcación: 21-10-19, 22:00, Hora de Venezuela

#Actualización: Esto estaba en gestionEstudiante.py, pero lo moví para la modularidad del código
#to do: Terminar validaciones.

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor
from Prompt import ErrorPrompt

class StudentTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1) #Columnas
        self.setRowCount(10)
        self.setHorizontalHeaderLabels(["Información del estudiante"])
        self.setVerticalHeaderLabels(["Carnet", "Nombre", "Apellido", "CI", "Tlf.", "email", "Días bloqueado", "Libros prestados actualmente", "Deuda Bs.", "Deuda USD."]) #Header
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
            self.setItem(i, 0, QTableWidgetItem())
            self.item(i, 0).setBackground(QColor(224, 255, 255))

    def getFields(self):
        fields = []
        for i in range(10):
            fields.append(self.item(i, 0).text())

        return fields

    def getValues(self):
        updateRequest = "carnet = \'" + self.item(0, 0).text() + "\', "
        updateRequest += "first_name = \'" + self.item(1, 0).text() + "\', "
        updateRequest += "last_name = \'" + self.item(2, 0).text() + "\', "
        updateRequest += "CI = " + self.item(3,0).text() + ", "
        updateRequest += "phone = " + self.item(4,0).text() + ", "
        updateRequest += "email = \'" + self.item(5,0).text() + "\', "
        updateRequest += "days_blocked = " + self.item(6,0).text() + ", "
        updateRequest += "current_Books = " + self.item(7,0).text() + ", "
        updateRequest += "book_debt = " + self.item(8,0).text()

        return updateRequest
