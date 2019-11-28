#CEIC Libros
#Tabla de estudiantes
#Desarrollado por Forward
#Responsable del módulo: Diego Peña, 15-11095
#Fecha de inicio: 22-10-19, Apróx a las 10:00 am hora de Venezuela, quizás antes, pero después de la 8:30
#Última modifcación: 22-10-19, 19:14 pm, Hora de Venezuela

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from validationFunctions import verification_estudiantes
from Prompt import InfoPrompt, ErrorPrompt
import sys

class AgregarEstudiante(QWidget):

    def __init__(self):
        #Inicialización de la ventana
        super().__init__()
        self.setWindowTitle("Gestión de estudiantes")
        self.setWindowIcon(QIcon("static/icono_CEIC.png"))
        self.setStyleSheet('background-color: rgb(236, 240, 241)')

        #Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")                                        # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
        self.db.open()

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.titleFont.setBold(True)
        self.labelFont = QFont("Helvetica", 13)
        self.labelFont.setBold(True)
        self.buttonFont = QFont("Arial", 12)
        self.buttonFont.setBold(True)

        # Título
        self.title = QLabel(self)
        self.title.setText("Agregar Estudiante")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 570, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Line edits para introducir los datos del estudiante
        self.carnetInput = QLineEdit(self)
        self.fnameInput = QLineEdit(self)
        self.lnameInput = QLineEdit(self)
        self.CIInput = QLineEdit(self)
        self.phoneInput = QLineEdit(self)
        self.emailInput = QLineEdit(self)

        # CSS, PlaceholderText y posicionamiento de los line edits
        self.carnetInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.carnetInput.setPlaceholderText(" Carnet del estudiante")
        self.carnetInput.setGeometry(130, 150, 600, 50)

        self.fnameInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.fnameInput.setPlaceholderText(" Nombre del estudiante")
        self.fnameInput.setGeometry(130, 220, 600, 50) 

        self.lnameInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.lnameInput.setPlaceholderText(" Apellido del estudiante")
        self.lnameInput.setGeometry(130, 290, 600, 50)

        self.CIInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.CIInput.setPlaceholderText(" Cédula del estudiante")
        self.CIInput.setGeometry(130, 360, 600, 50)

        self.phoneInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.phoneInput.setPlaceholderText(" Teléfono del estudiante")
        self.phoneInput.setGeometry(130, 430, 600, 50)

        self.emailInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.emailInput.setPlaceholderText(" Email del estudiante")
        self.emailInput.setGeometry(130, 500, 600, 50)

        #Botones
        self.agregar = QPushButton(self)
        self.agregar.setText("Agregar")
        self.agregar.setFont(self.buttonFont)
        self.agregar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.agregar.setGeometry(430, 610, 290, 40)

        self.cancelar = QPushButton(self)
        self.cancelar.setText("Cancelar")
        self.cancelar.setFont(self.buttonFont)
        self.cancelar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelar.setGeometry(130, 610, 290, 40)

        #CSS Botones
        self.agregar.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    background-color: rgb(55, 162, 228);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    background-color: rgb(35, 142, 208);\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 15px;\n"
                                  "    background-color: rgb(45, 152, 218);\n"
                                  "    color: white;\n"
                                  "}")

        self.cancelar.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    background-color: #F10000;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    background-color: #CC0000;\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 15px;\n"
                                  "    background-color: #C20000;\n"
                                  "    color: white;\n"
                                  "}")

        #Conexiones de los botones
        self.agregar.clicked.connect(self.agregarEstudiante)
        self.cancelar.clicked.connect(self.clean)

    @pyqtSlot()
    def agregarEstudiante(self):
        fields = [self.carnetInput.text(), self.fnameInput.text(), self.lnameInput.text(), self.CIInput.text(),\
            self.phoneInput.text(), self.emailInput.text()]

        correct = verification_estudiantes(fields, 6)

        if not correct:
            return

        self.query = QSqlQuery()
        self.query.prepare("INSERT INTO Estudiante(carnet, first_name, last_name, CI, phone, email) VALUES(:carnet, :fname, \
            :lname, :CI, :phone, :email ) RETURNING carnet")
        self.query.bindValue(0, fields[0])
        self.query.bindValue(1, fields[1])
        self.query.bindValue(2, fields[2])
        self.query.bindValue(3, int(fields[3]))
        self.query.bindValue(4, int(fields[4]))
        self.query.bindValue(5, fields[5])

        self.query.exec_()

        if self.query.first():
            InfoPrompt("Éxito", "La información del estudiante ha sido agregada exitosamente")
            self.clean()
        else:
            ErrorPrompt("Fracaso", "El estudiante no fue agregado al sistema")

    @pyqtSlot()
    def clean(self):
        self.carnetInput.clear()
        self.fnameInput.clear()
        self.lnameInput.clear()
        self.CIInput.clear()
        self.phoneInput.clear()
        self.emailInput.clear()