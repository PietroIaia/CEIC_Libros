#Última modifcación: 22-10-19, 19:14 pm, Hora de Venezuela

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from validationFunctions import verification_books
from Prompt import InfoPrompt, ErrorPrompt
from Tables import autoresTable
from agregarAutor import AgregarAutor
from AgregarLibro import AgregarLibro
from validationFunctions import check_name, check_quantity
import sys

class verificarAutor(QWidget):

    def __init__(self):
        # Inicialización de la ventana
        super().__init__()
        self.setWindowTitle("Verificación de Autor")
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
        self.instruccionFont = QFont("Helvetica", 10)
        self.instruccionFont.setBold(True)

        # Título
        self.title = QLabel(self)
        self.title.setText("Agregar Libro - Autores")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 570, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Instrucción
        self.instruccion = QLabel(self)
        self.instruccion.setText("Si alguno de los autores del libro a agregar no \n" \
                                 "            aparece en la lista, agréguelo.")
        self.instruccion.setStyleSheet('color: rgb(79, 90, 94)')
        self.instruccion.setFont(self.instruccionFont)
        self.instruccion.setGeometry(525, 240, 300, 50)

        # Layout para agregar autores
        self.agregarAutores = QVBoxLayout()
        self.agregarAutores.addStretch()

        self.agregar = QPushButton(self)
        self.agregar.setText("Agregar autor")
        self.agregar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.agregar.setGeometry(525, 380, 300, 30)
        self.agregar.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: rgb(55, 162, 228);\n"
                                  "    color: white;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: rgb(35, 142, 208);\n"
                                  "    color: white;\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: rgb(45, 152, 218);\n"
                                  "    color: white;\n"
                                  "}")

        self.cancelar = QPushButton(self)
        self.cancelar.setText("Cancelar")
        self.cancelar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelar.setGeometry(525, 420, 300, 30)
        self.cancelar.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: #C20000;\n"
                                  "    color: white;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: #CC0000;\n"
                                  "    color: white;\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: #F10000;\n"
                                  "    color: white;\n"
                                  "}")

        self.seguir = QPushButton(self)
        self.seguir.setText("Continuar")
        self.seguir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.seguir.setGeometry(525, 640, 300, 30)
        self.seguir.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: rgb(22, 46, 107);\n"
                                  "    color: white;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: rgb(2, 26, 87);\n"
                                  "    color: white;\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 10px;\n"
                                  "    background-color: rgb(12, 36, 97);\n"
                                  "    color: white;\n"
                                  "}")

        # Font para los botones
        self.buttonFont = QFont("Arial", 12)
        self.buttonFont.setBold(True)
        self.agregar.setFont(self.buttonFont)
        self.seguir.setFont(self.buttonFont)
        self.cancelar.setFont(self.buttonFont)

        # Widgets para agregar autores
        self.ingresarNombre = QLineEdit(self)
        self.ingresarNombre.setStyleSheet('background-color: white; border-radius: 10px; border: 1px solid rgb(210, 218, 226);')
        self.ingresarNombre.setPlaceholderText(" Ingrese el nombre del autor")
        self.ingresarNombre.setGeometry(525, 300, 300, 30)

        self.ingresarApellido = QLineEdit(self)
        self.ingresarApellido.setStyleSheet('background-color: white; border-radius: 10px; border: 1px solid rgb(210, 218, 226);')
        self.ingresarApellido.setPlaceholderText(" Ingrese el apellido del autor")
        self.ingresarApellido.setGeometry(525, 340, 300, 30)

        # Tabla donde aparecerán los datos
        self.table = autoresTable() #Tablas
        self.table.llenarAutores()
        self.widget = QWidget()
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.table)
        self.tableLayout.addWidget(self.widget)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.layout.addStretch()
        self.layout.addLayout(self.tableLayout)
        self.layout.addStretch()
        self.setLayout(self.layout)

        # Conexiones de botones
        self.agregar.clicked.connect(self.anadir)
        self.cancelar.clicked.connect(self.clean)

        # Mostrar en pantalla
        self.instruccion.raise_()
        self.ingresarNombre.raise_()
        self.ingresarApellido.raise_()
        self.agregar.raise_()
        self.seguir.raise_()
        self.cancelar.raise_()
        self.line.raise_()

    @pyqtSlot()
    def anadir(self):
      fields = [self.ingresarNombre.text(), self.ingresarApellido.text()]
      
      author_id = int(self.query[0][0]) + 1
      correct = check_name(str(fields[0]), 1) and check_name(str(fields[1]), 0) and check_quantity(str(author_id))

      if not correct:
          return

      self.query = QSqlQuery()
      self.query.prepare("INSERT INTO Author(first_name, last_name, author_id) VALUES(:first_name, :last_name, :author_id) RETURNING author_id")
      self.query.bindValue(0, fields[0])
      self.query.bindValue(1, fields[1])
      self.query.bindValue(2, int(fields[2]))

      self.query.exec_()

      if self.query.first():
          InfoPrompt("Éxito", "La información del autor ha sido agregada exitosamente")
          self.table.llenarAutores()
      else:
          ErrorPrompt("Fracaso", "El autor no fue agregado al sistema")

    @pyqtSlot()
    def clean(self):
        self.ingresarNombre.clear()
        self.ingresarApellido.clear()