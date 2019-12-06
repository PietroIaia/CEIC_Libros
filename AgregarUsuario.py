#CEIC Libros
#Ventana para agregar usuarios
#Desarrollado por Forward

# Importamos las librerias a utilizar
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from validationFunctions import verification_users
from Prompt import InfoPrompt, ErrorPrompt
from passlib.hash import bcrypt
import sys
import datetime 

class AgregarUsuario(QWidget):

    def __init__(self):
        # Inicialización de la ventana
        super().__init__()
        self.setWindowTitle("Gestión de usuarios")
        self.setWindowIcon(QIcon("static/icono_CEIC.png"))
        self.setStyleSheet('background-color: rgb(236, 240, 241)')

        # Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")         # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
        self.db.open()

        # Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.titleFont.setBold(True)
        self.labelFont = QFont("Helvetica", 13)
        self.labelFont.setBold(True)
        self.buttonFont = QFont("Arial", 12)
        self.buttonFont.setBold(True)

        # Título
        self.title = QLabel(self)
        self.title.setText("Agregar Usuario")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 570, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Label
        self.permisosLabel = QLabel(self)
        self.permisosLabel.setText("Permisos de Administrador")

        # Line edits para introducir los datos del usuario
        self.userInput = QLineEdit(self)
        self.contraseñaInput = QLineEdit(self)
        self.confirmContraseñaInput = QLineEdit(self)
        self.CIInput = QLineEdit(self)
        self.nombreInput = QLineEdit(self)
        self.apellidoInput = QLineEdit(self)
        self.emailInput = QLineEdit(self)
        self.permisosInput = QCheckBox(self)

        # CSS, PlaceholderText y posicionamiento de los line edits
        self.userInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.userInput.setPlaceholderText(" Nombre de usuario")
        self.userInput.setGeometry(130, 140, 600, 50)

        self.contraseñaInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.contraseñaInput.setPlaceholderText(" Contraseña")
        self.contraseñaInput.setGeometry(130, 200, 600, 50)

        self.confirmContraseñaInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.confirmContraseñaInput.setPlaceholderText(" Confirmar contraseña")
        self.confirmContraseñaInput.setGeometry(130, 260, 600, 50)

        self.CIInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.CIInput.setPlaceholderText(" Cédula")
        self.CIInput.setGeometry(130, 320, 600, 50)

        self.nombreInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.nombreInput.setPlaceholderText(" Nombre")
        self.nombreInput.setGeometry(130, 380, 600, 50)

        self.apellidoInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.apellidoInput.setPlaceholderText(" Apellido")
        self.apellidoInput.setGeometry(130, 440, 600, 50)

        self.emailInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.emailInput.setPlaceholderText(" Correo electrónico")
        self.emailInput.setGeometry(130, 500, 600, 50)

        self.permisosInput.setGeometry(370, 560, 50, 50)
        self.permisosLabel.setStyleSheet('color: rgb(79, 90, 94)')
        self.permisosLabel.setFont(self.labelFont)
        self.permisosLabel.setGeometry(140, 560, 250, 50)

        # Botones
        self.agregar = QPushButton(self)
        self.agregar.setText("Agregar")
        self.agregar.setFont(self.buttonFont)
        self.agregar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.agregar.setGeometry(430, 640, 290, 40)

        self.cancelar = QPushButton(self)
        self.cancelar.setText("Cancelar")
        self.cancelar.setFont(self.buttonFont)
        self.cancelar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelar.setGeometry(130, 640, 290, 40)

        # CSS Botones
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

        
        # Conexiones de los botones
        self.agregar.clicked.connect(self.agregarUsuario)
        self.cancelar.clicked.connect(self.clean)


    @pyqtSlot()
    def agregarUsuario(self):
        if(self.contraseñaInput.text() == "" or self.confirmContraseñaInput.text() == ""):
            ErrorPrompt("Error", "No puede dejar el campo de contraseñas en blanco")
            return

        if(self.contraseñaInput.text() == self.confirmContraseñaInput.text()):

            if(self.permisosInput.isChecked()):
                fields = [self.userInput.text(), self.nombreInput.text(), self.apellidoInput.text(), self.emailInput.text(), "Administrador"]
            else:
                fields = [self.userInput.text(), self.nombreInput.text(), self.apellidoInput.text(), self.emailInput.text(), "Usuario"]

            correct = verification_users(fields, 5)

            if not correct:
                return

            ultima_conexion = str(datetime.datetime.now())
            fecha_de_creacion = str(datetime.datetime.now())
            if(fields[4] == "Administrador"):
                fields[4] = 1
            elif(fields[4] == "Usuario"):
                fields[4] = 0

            puede = 1
            queryText2 = "SELECT * FROM CEIC_User WHERE username = '" + fields[0] + "';"
            self.query2 = QSqlQuery()
            self.query2.exec_(queryText2)

            if self.query2.first():
                puede = 0;

            if puede == 1:
                self.query = QSqlQuery()
                self.query.prepare("INSERT INTO CEIC_User (username, password_, first_name, last_name, email, permission_mask, last_login, creation_date) VALUES(:username, :password, \
                    :fname, :lname, :email, :permisos, :last_login, :creation_date ) RETURNING username")
                self.query.bindValue(0, fields[0])
                self.query.bindValue(1, bcrypt.hash(self.contraseñaInput.text()))
                self.query.bindValue(2, fields[1])
                self.query.bindValue(3, fields[2])
                self.query.bindValue(4, fields[3])
                self.query.bindValue(5, fields[4])
                self.query.bindValue(":last_login", ultima_conexion)
                self.query.bindValue(":creation_date", fecha_de_creacion)

                self.query.exec_()

                if self.query.first():
                    InfoPrompt("Éxito", "La información del usuario ha sido agregada exitosamente.")
                else:
                    ErrorPrompt("Fracaso", "El usuario no fue agregado al sistema.")
            else:
                ErrorPrompt("Error", "El nombre de usuario coincide con uno ya existente, por favor ingrese otro nombre.")
        else:
            ErrorPrompt("Error", "Las contraseñas no coinciden.")

    @pyqtSlot()
    def clean(self):
        self.userInput.clear()
        self.contraseñaInput.clear()
        self.confirmContraseñaInput.clear()
        self.CIInput.clear()
        self.nombreInput.clear()
        self.apellidoInput.clear()
        self.emailInput.clear()