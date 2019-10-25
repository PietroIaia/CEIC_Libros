#CEIC Libros
#Tabla de estudiantes
#Desarrollado por Forward
#Responsable del módulo: Diego Peña, 15-11095
#Fecha de inicio: 22-10-19, Apróx a las 10:00 am hora de Venezuela, quizás antes, pero después de la 8:30
#Última modifcación: 22-10-19, 19:14 pm, Hora de Venezuela

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from validationFunctions import verification
from Prompt import InfoPrompt, ErrorPrompt
import sys

class AgregarEstudiante(QWidget):

    def __init__(self):
        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 100, 600, 500)
        self.setMinimumSize(QSize(600, 500))
        self.setMaximumSize(QSize(600, 500))
        self.setWindowTitle("Gestión de estudiantes")
        self.setStyleSheet('background-color: LightSkyBlue')

        #Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")                                        # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
        self.db.open()

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        #self.instFont = QFont("Serif", 12)

        #Título
        self.title = QLabel("Agregar nuevo estudiante")
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Aquí vienen los campos
        self.carnetLabel = QLabel("Carnet del estudiante")
        self.carnetInput = QLineEdit(self)
        self.fnameLabel = QLabel("Nombre del estudiante")
        self.fnameInput = QLineEdit(self)
        self.lnameLabel = QLabel("Apellido del estudiante")
        self.lnameInput = QLineEdit(self)
        self.CILabel = QLabel("CI")
        self.CIInput = QLineEdit(self)
        self.phoneLabel = QLabel("Teléfono")
        self.phoneInput = QLineEdit(self)
        self.emailLabel = QLabel("Email del estudiante")
        self.emailInput = QLineEdit(self)

        #CSS
        self.carnetInput.setStyleSheet('background-color: white')
        self.fnameInput.setStyleSheet('background-color: white')
        self.lnameInput.setStyleSheet('background-color: white')
        self.CIInput.setStyleSheet('background-color: white')
        self.phoneInput.setStyleSheet('background-color: white')
        self.emailInput.setStyleSheet('background-color: white')

        #Botones
        self.agregar = QPushButton("Agregar")
        self.cancelar = QPushButton("Cancelar")

        #Layout del título
        #self.titleLayout = QVBoxLayout()
        #self.titleLayout.addWidget(self.title)

        #LAyout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.carnetLabel)
        self.layout.addWidget(self.carnetInput)
        self.layout.addWidget(self.fnameLabel)
        self.layout.addWidget(self.fnameInput)
        self.layout.addWidget(self.lnameLabel)
        self.layout.addWidget(self.lnameInput)
        self.layout.addWidget(self.CILabel)
        self.layout.addWidget(self.CIInput)
        self.layout.addWidget(self.phoneLabel)
        self.layout.addWidget(self.phoneInput)
        self.layout.addWidget(self.emailLabel)
        self.layout.addWidget(self.emailInput)
        self.layout.addWidget(self.agregar)
        self.layout.addWidget(self.cancelar)

        self.setLayout(self.layout)

        self.agregar.clicked.connect(self.agregarEstudiante)
        self.cancelar.clicked.connect(self.closeWindow)

    @pyqtSlot()
    def agregarEstudiante(self):
        fields = [self.carnetInput.text(), self.fnameInput.text(), self.lnameInput.text(), self.CIInput.text(),\
            self.phoneInput.text(), self.emailInput.text()]

        correct = verification(fields, 6)

        if not correct:
            return

        print("Probando2")

        self.query = QSqlQuery()
        print("Probando")
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
            self.close()
        else:
            ErrorPrompt("Fracaso", "El estudiante no fue agregado al sistema")

    @pyqtSlot()
    def closeWindow(self):
        self.close()