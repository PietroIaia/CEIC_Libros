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
from validationFunctions import verification_books
from Prompt import InfoPrompt, ErrorPrompt
import sys

class AgregarLibro(QWidget):

    def __init__(self):
        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 100, 600, 500)
        self.setMinimumSize(QSize(600, 500))
        self.setMaximumSize(QSize(600, 500))
        self.setWindowTitle("Gestión de libros")
        self.setStyleSheet('background-color: LightSkyBlue')

        #Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaCEIC")
        self.db.setUserName("postgres")
        self.db.setPassword("Tranc0nReloj-7aha")
        self.db.open()

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)

        #Título
        self.title = QLabel("Agregar nuevo libro")
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Aquí vienen los campos
        self.IDLabel = QLabel("ID del libro")
        self.IDInput = QLineEdit(self)
        self.titleBookLabel = QLabel("Titulo del libro")
        self.titleBookInput = QLineEdit(self)
        self.authorsLabel = QLabel("Nombre del autor")
        self.authorsInput = QLineEdit(self)
        self.ISBNLabel = QLabel("ISBN")
        self.ISBNInput = QLineEdit(self)
        self.quantityLabel = QLabel("Numero de ejemplares")
        self.quantityInput = QLineEdit(self)

        #CSS
        self.IDInput.setStyleSheet('background-color: white')
        self.titleBookInput.setStyleSheet('background-color: white')
        self.authorsInput.setStyleSheet('background-color: white')
        self.ISBNInput.setStyleSheet('background-color: white')
        self.quantityInput.setStyleSheet('background-color: white')

        #Botones
        self.agregar = QPushButton("Agregar")
        self.cancelar = QPushButton("Cancelar")

        #LAyout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.IDLabel)
        self.layout.addWidget(self.IDInput)
        self.layout.addWidget(self.titleBookLabel)
        self.layout.addWidget(self.titleBookInput)
        self.layout.addWidget(self.authorsLabel)
        self.layout.addWidget(self.authorsInput)
        self.layout.addWidget(self.ISBNLabel)
        self.layout.addWidget(self.ISBNInput)
        self.layout.addWidget(self.quantityLabel)
        self.layout.addWidget(self.quantityInput)
        self.layout.addWidget(self.agregar)
        self.layout.addWidget(self.cancelar)

        self.setLayout(self.layout)

        self.agregar.clicked.connect(self.AgregarLibro)
        self.cancelar.clicked.connect(self.closeWindow)

    @pyqtSlot()
    def AgregarLibro(self):
        fields = [self.IDInput.text(), self.titleBookInput.text(), self.authorsInput.text(), self.ISBNInput.text(),\
            self.quantityInput.text()]

        correct = verification_books(fields, 5)

        if not correct:
            return


        self.query = QSqlQuery()
        self.query.prepare("INSERT INTO Book(book_id, title, authors, isbn, quantity) VALUES(:ID, :title, \
            :authors, :ISBN, :quantity) RETURNING book_id")
        self.query.bindValue(0, int(fields[0]))
        self.query.bindValue(1, fields[1])
        self.query.bindValue(2, fields[2])
        self.query.bindValue(3, fields[3])
        self.query.bindValue(4, int(fields[4]))

        self.query.exec_()

        if self.query.first():
            InfoPrompt("Éxito", "La información del libro ha sido agregada exitosamente")
            self.close()
        else:
            ErrorPrompt("Fracaso", "El libro no fue agregado al sistema")

    @pyqtSlot()
    def closeWindow(self):
        self.close()