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
from validationFunctions import verification_books
from Prompt import InfoPrompt, ErrorPrompt
import sys

autores = ""

class AgregarLibro(QWidget):

    def __init__(self):
        # Inicialización de la ventana
        super().__init__()
        self.setWindowTitle("Gestión de libros")
        self.setWindowIcon(QIcon("static/icono_CEIC.png"))
        self.setStyleSheet('background-color: rgb(236, 240, 241)')

        # Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")
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
        self.title.setText("Agregar Libro")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 570, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Line edits
        self.IDInput = QLineEdit(self)
        self.titleBookInput = QLineEdit(self)
        self.authorsLabel = QLabel(self)
        self.authorsLabel.setText("  Autor")
        self.authorsInput = QComboBox(self)
        self.ISBNInput = QLineEdit(self)
        self.quantityInput = QLineEdit(self)

        # CSS, PlaceholderText y posicionamiento de los line edits
        self.IDInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.IDInput.setPlaceholderText(" Ingrese el código de identificación del libro")
        self.IDInput.setGeometry(130, 150, 600, 50)

        self.titleBookInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.titleBookInput.setPlaceholderText(" Ingrese el título del libro")
        self.titleBookInput.setGeometry(130, 220, 600, 50)  

        self.authorsLabel.setGeometry(130, 290, 200, 50)
        self.authorsLabel.setStyleSheet('color: rgb(79, 90, 94)')
        self.authorsLabel.setFont(self.labelFont)
        self.authorsInput.setGeometry(200, 290, 530, 50)
        self.authorsInput.setStyleSheet('background-color: white; border: 1px solid rgb(210, 218, 226); border-radius: 20px;')

        self.ISBNInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.ISBNInput.setPlaceholderText(" Ingrese el ISBN del libro")
        self.ISBNInput.setGeometry(130, 360, 600, 50)

        self.quantityInput.setStyleSheet('background-color: white; border-radius: 20px; border: 1px solid rgb(210, 218, 226); font: 16px;')
        self.quantityInput.setPlaceholderText(" Ingrese el número de ejemplares que tiene el libro")
        self.quantityInput.setGeometry(130, 430, 600, 50)

        # Botones
        self.agregarAutor = QPushButton(self)
        self.agregarAutor.setText("Agregar autor")
        self.agregarAutor.setFont(self.buttonFont)
        self.agregarAutor.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.agregarAutor.setGeometry(130, 520, 300, 35)

        self.agregarLibro = QPushButton(self)
        self.agregarLibro.setText("Agregar libro")
        self.agregarLibro.setFont(self.buttonFont)
        self.agregarLibro.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.agregarLibro.setGeometry(432, 520, 300, 35)

        self.cancelar = QPushButton(self)
        self.cancelar.setText("Cancelar")
        self.cancelar.setFont(self.buttonFont)
        self.cancelar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelar.setGeometry(130, 565, 600, 35)

        # CSS Botones
        self.agregarLibro.setStyleSheet("QPushButton:hover\n"
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

        self.agregarAutor.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    background-color: rgb(22, 46, 107);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    background-color: rgb(2, 26, 87);\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 15px;\n"
                                  "    background-color: rgb(12, 36, 97);\n"
                                  "    color: white;\n"
                                  "}")

        self.cancelar.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    background-color: #C20000;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    background-color: #CC0000;\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 15px;\n"
                                  "    background-color: #F10000;\n"
                                  "    color: white;\n"
                                  "}")

        self.mostrarAutores()

        # Conexiones de botones
        self.cancelar.clicked.connect(self.clean)
        self.agregarLibro.clicked.connect(self.AgregarLibro)
        self.authorsInput.activated[str].connect(self.seleccion)

        # Raise
        self.title.raise_()
        self.line.raise_()

    @pyqtSlot()
    def AgregarLibro(self):
        global autores
        fields = [self.IDInput.text(), self.titleBookInput.text(), autores, self.ISBNInput.text(),\
            self.quantityInput.text()]

        correct = verification_books(fields, 5)

        if not correct:
            return

        self.query = QSqlQuery()
        self.query.prepare("INSERT INTO Book(book_id, title, authors, isbn, quantity, quantity_lent) VALUES(:ID, :title, \
            :authors, :ISBN, :quantity, '0') RETURNING book_id")
        self.query.bindValue(0, int(fields[0]))
        self.query.bindValue(1, fields[1])
        self.query.bindValue(2, fields[2])
        self.query.bindValue(3, fields[3])
        self.query.bindValue(4, int(fields[4]))

        self.query.exec_()

        if self.query.first():
            InfoPrompt("Éxito", "La información del libro ha sido agregada exitosamente")
        else:
            ErrorPrompt("Fracaso", "El libro no fue agregado al sistema")

        for i in range(int(fields[4])):
            self.query.exec_("INSERT INTO Book_copy (copy_id, book_id) VALUES('" + str(i+1) + "', '" + str(fields[0]) + "');")

    @pyqtSlot()
    def seleccion(self):
        global autores
        autores = autores + self.authorsInput.currentText()+ " , "
        InfoPrompt("Éxito", "Su autor ha sido seleccionado exitosamente")
        self.authorsInput.removeItem(self.authorsInput.currentIndex())

    @pyqtSlot()
    def mostrarAutores(self):
        # Query para mostrar todos los autores en authorsInput
        sql = "SELECT first_name, last_name FROM Author ORDER BY last_name"  ## cambiar esto
        queryx = QSqlQuery(sql)
        while queryx.next():
           
            IDX = str(queryx.value(0))
            IDX2 = str(queryx.value(1))
            IDX3 = IDX + " "+ IDX2
            self.authorsInput.addItem(IDX3)

    @pyqtSlot()
    def clean(self):
        self.IDInput.clear()
        self.titleBookInput.clear()
        self.ISBNInput.clear()
        self.quantityInput.clear()