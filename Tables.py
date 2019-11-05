#CEIC Libros
#Tabla de estudiantes
#Desarrollado por Forward
#Responsable del módulo: Diego Peña, 15-11095
#Fecha de inicio: 21-10-19, Apróx 8:20 am, Hora de Venezuela
#Última modifcación: 22-10-19, 19:13, Hora de Venezuela

#Actualización: Clear está listo

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor
from Prompt import ErrorPrompt


###################################################
#                 Tabla de Estudiantes            #
###################################################
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

    def clear(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setText("")
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


###################################################
#                 Tabla de Libros                 #
###################################################
class BooksTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1) #Columnas
        self.setRowCount(7)
        self.setHorizontalHeaderLabels(["Información del Libro"])
        self.setVerticalHeaderLabels(["ID", "Titulo", "Autores", "ISBN", "Cantidad", "Cantidad prestada", "Duracion del prestamo en dias"]) #Header
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

    def clear(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setText("")
            self.item(i, 0).setBackground(QColor(224, 255, 255))

    def getFields(self):
        fields = []
        for i in range(7):
            fields.append(self.item(i, 0).text())

        return fields

    def getValues(self):
        updateRequest = "book_id = \'" + self.item(0, 0).text() + "\', "
        updateRequest += "title = \'" + self.item(1, 0).text() + "\', "
        updateRequest += "authors = \'" + self.item(2, 0).text() + "\', "
        updateRequest += "isbn = \'" + self.item(3,0).text() + "\', "
        updateRequest += "quantity = \'" + self.item(4,0).text() + "\', "
        updateRequest += "quantity_lent = \'" + self.item(5,0).text() + "\', "
        updateRequest += "loan_duration = \'" + self.item(6,0).text() +"\'"

        return updateRequest


###################################################
#                 Tabla de Usuarios               #
###################################################
class UserTable(QTableWidget):
    def __init__(self):
        super().__init__()
        # Creamos el ComboBox para los permisos
        comboBox = QComboBox()
        comboBox.insertItem(0, "Usuario")
        comboBox.insertItem(1, "Administrador")
        comboBox.insertItem(2, "")                                     #El segundo item es el default
        comboBox.setCurrentIndex(2)
        comboBox.model().item(2).setEnabled(False)                     #lo ponemos disabled para que el usuario no pueda clickearlo
        # Creamos la tabla
        self.setColumnCount(1) #Columnas
        self.setRowCount(7)
        self.setHorizontalHeaderLabels(["Información del usuario"])
        self.setVerticalHeaderLabels(['Nombre de usuario', 'Nombre', 'Apellido', 'Email', 'Permisos', 'Ultima conexion', 'Fecha de creacion']) #Header
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setCellWidget(4, 0, comboBox)
        self.setTableColors()
        self.cellWidget(4, 0).setEnabled(False)
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
        self.cellWidget(4, 0).setStyleSheet('background-color: rgb(224, 255, 255); border: 0px')

    def clear(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setText("")
            self.item(i, 0).setBackground(QColor(224, 255, 255))
        self.cellWidget(4, 0).setCurrentIndex(2)

    def getFields(self):
        fields = []
        for i in range(7):
            if(i == 4):
                fields.append(str(self.cellWidget(4, 0).currentText()))
            else:
                fields.append(self.item(i, 0).text())

        return fields

    def getValues(self):
        updateRequest = "username = \'" + self.item(0, 0).text() + "\', "
        updateRequest += "first_name = \'" + self.item(1, 0).text() + "\', "
        updateRequest += "last_name = \'" + self.item(2,0).text() + "\', "
        updateRequest += "email = \'" + self.item(3,0).text() + "\', "
        if (self.item(4, 0).text() == "Administrador"):
            updateRequest += "permission_mask = 1"
        else:
            updateRequest += "permission_mask = 0"

        return updateRequest

