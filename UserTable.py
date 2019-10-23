#CEIC Libros
#Tabla de usuarios
#Desarrollado por Forward


from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor
from Prompt import ErrorPrompt

class UserTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1) #Columnas
        self.setRowCount(8)
        self.setHorizontalHeaderLabels(["Información del usuario"])
        self.setVerticalHeaderLabels(['nombre_de_usuario', 'contraseña', 'nombre', 'apellido', 'correo_electronico', 'permisos', 'ultima_conexion', 'fecha_de_creacion']) #Header
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
        for i in range(8):
            fields.append(self.item(i, 0).text())

        return fields

    def getValues(self):
        updateRequest = "username = \'" + self.item(0, 0).text() + "\', "
        updateRequest += "password_ = \'" + self.item(1, 0).text() + "\', "
        updateRequest += "first_name = \'" + self.item(2, 0).text() + "\', "
        updateRequest += "last_name = \'" + self.item(3,0).text() + "\', "
        updateRequest += "email = \'" + self.item(4,0).text() + "\', "
        updateRequest += "permission_mask = " + self.item(5,0).text()

        return updateRequest
