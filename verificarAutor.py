#Última modifcación: 22-10-19, 19:14 pm, Hora de Venezuela

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from validationFunctions import verification_books
from Prompt import InfoPrompt, ErrorPrompt
from Tables import autoresTable
from agregarAutor import AgregarAutor
from AgregarLibro import AgregarLibro
import sys

class verificarAutor(QWidget):

    def __init__(self):
        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 100, 600, 500)
        self.setMinimumSize(QSize(700, 700))
        self.setMaximumSize(QSize(700, 700))
        self.setWindowTitle("Verificación de Autor")
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
        self.titleFont = QFont("Serif", 12)

        #Título
        self.title = QLabel("     Por favor verifique si los autores del libro que va a gregar aparecen en la lista. \n              si alguno no aparece añadalo tocando el botón \"agregar autor\"")
        self.title.setStyleSheet('color: Black')
        self.title.setFont(self.titleFont)

        #Tabla donde aparecerán los datos
        self.table = autoresTable() #Tablas
        self.table.llenarAutores()
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.table)

        #Botones
        self.agregar = QPushButton("Agregar autor")
        self.seguir = QPushButton("Seguir a agregar libro")

        self.agregar.setStyleSheet('background-color: PowderBlue')
        self.seguir.setStyleSheet('background-color: PowderBlue')

        self.searchLayout = QVBoxLayout()
        self.searchLayout.addWidget(self.agregar)
        self.searchLayout.addWidget(self.seguir)

        #LAyout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.tableLayout)
        self.layout.addLayout(self.searchLayout)
        self.setLayout(self.layout)

        self.agregar.clicked.connect(self.anadir)
        self.seguir.clicked.connect(self.seguirLibro)

    @pyqtSlot()
    def anadir(self):
       self.form = AgregarAutor()
       self.form.show()
       self.close()

    @pyqtSlot()
    def seguirLibro(self):
       self.form2 = AgregarLibro()
       #self.form2.varglobal("nose bro")
       self.form2.show()
       self.close()

    @pyqtSlot()
    def closeWindow(self):
        self.close()