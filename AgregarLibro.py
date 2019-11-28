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
from validationFunctions import verification_books
from Prompt import InfoPrompt, ErrorPrompt
import sys

autores = ""

class AgregarLibro(QWidget):

    def __init__(self):
        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 100, 600, 500)
        self.setMinimumSize(QSize(600, 500))
        self.setMaximumSize(QSize(600, 500))
        self.setWindowTitle("Gestión de libros")
        self.setWindowIcon(QIcon("static/icono_CEIC.png"))
        self.setStyleSheet('background-color: LightSkyBlue')

        #Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")
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
        self.titleBookLabel = QLabel("Título del libro")
        self.titleBookInput = QLineEdit(self)
        self.authorsLabel = QLabel("Nombre del autor")
        self.authorsInput = QComboBox(self)
        self.ISBNLabel = QLabel("ISBN")
        self.ISBNInput = QLineEdit(self)
        self.quantityLabel = QLabel("Número de ejemplares")
        self.quantityInput = QLineEdit(self)

        sql = "SELECT first_name, last_name FROM Author ORDER BY last_name"  ## cambiar esto
        queryx = QSqlQuery(sql)
        while queryx.next():
           
            IDX = str(queryx.value(0))
            IDX2 = str(queryx.value(1))
            IDX3 = IDX + " "+ IDX2
            self.authorsInput.addItem(IDX3)


        #CSS
        self.IDInput.setStyleSheet('background-color: white')
        self.titleBookInput.setStyleSheet('background-color: white')
        #self.authorsInput.setStyleSheet('background-color: white')
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
        self.authorsInput.activated[str].connect(self.seleccion)

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
            self.close()
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
        print(autores)

    @pyqtSlot()
    def closeWindow(self):
        self.close()
