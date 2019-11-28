from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from validationFunctions import check_name, check_quantity
from Prompt import InfoPrompt, ErrorPrompt
import sys

class AgregarAutor(QWidget):

    def __init__(self):
        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 100, 600, 500)
        self.setMinimumSize(QSize(500, 300))
        self.setMaximumSize(QSize(500, 300))
        self.setWindowTitle("Gestión de libros")
        self.setWindowIcon(QIcon("static/icono_CEIC.png"))
        self.setStyleSheet('background-color: LightSkyBlue')

        #Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaCEIC")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")
        self.db.open()

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)

        #Título
        self.title = QLabel("Agregar Autor")
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Aquí vienen los campos
        self.nombreLabel = QLabel("Nombre del autor")
        self.nombreInput = QLineEdit(self)
        self.apellidoLabel = QLabel("Apellido del autor")
        self.apellidoInput = QLineEdit(self)

        #CSS
        self.nombreInput.setStyleSheet('background-color: white')
        self.apellidoInput.setStyleSheet('background-color: white')
        #Botones
        self.agregar = QPushButton("Agregar")
        self.cancelar = QPushButton("Cancelar")

        #LAyout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.nombreLabel)
        self.layout.addWidget(self.nombreInput)
        self.layout.addWidget(self.apellidoLabel)
        self.layout.addWidget(self.apellidoInput)
        self.layout.addWidget(self.agregar)
        self.layout.addWidget(self.cancelar)

        self.setLayout(self.layout)

        self.agregar.clicked.connect(self.anadir)
        self.cancelar.clicked.connect(self.closeWindow)

    @pyqtSlot()
    def anadir(self):
        fields = [self.nombreInput.text(), self.apellidoInput.text()]

        correct = check_name(fields[0], 1) and check_name(fields[1], 0)

        if not correct:
            return


        self.query = QSqlQuery()
        self.query.prepare("INSERT INTO Author(first_name, last_name) VALUES(:first_name, :last_name) RETURNING author_id")
        self.query.bindValue(0, fields[0])
        self.query.bindValue(1, fields[1])

        self.query.exec_()

        if self.query.first():
            InfoPrompt("Éxito", "La información del autor ha sido agregada exitosamente")
            self.close()
        else:
            ErrorPrompt("Fracaso", "El autor no fue agregado al sistema")

        self.close()


    @pyqtSlot()
    def closeWindow(self):
        self.close()