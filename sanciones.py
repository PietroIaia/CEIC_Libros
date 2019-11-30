from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from Tables import Sanciones_Table, Debts_Table
from validationFunctions import check_pattern, check_carnet, check_debt
import sys
import datetime 


# NOTAS:
# - Entre Labels dentro del frame "Informacion de prestamo" hay 30px de espacio

class sanciones(QWidget):

    def __init__(self, Username, perm_mask):

        # Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Sanciones")
        self.setStyleSheet('background-color: rgb(236, 240, 241)')

        # Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.titleFont.setBold(True)
        self.instFont = QFont("Serif", 12)
        self.subFont = QFont("Serif", 10)
        self.btnFont = QFont("Serif", 9)
        self.smallbtn = QFont("Serif", 7)

        # Título
        self.title = QtWidgets.QLabel(self)
        self.title.setText("Sanciones")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 350, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Frame del form
        self.frame_form_multas = QFrame(self)
        self.frame_form_multas.setFrameShape(QFrame.StyledPanel)
        self.frame_form_multas.setFixedWidth(275)
        self.frame_form_multas.setFixedHeight(420)
        self.frame_form_multas.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: white;\n"
        "}")
        self.frame_form_multas.move(10, 150)

        # Informacion de préstamo
        self.info_prestamo_frame = QFrame(self.frame_form_multas)
        self.info_prestamo_frame.setFrameShape(QFrame.NoFrame)
        self.info_prestamo_frame.setFrameShadow(QFrame.Sunken)
        self.info_prestamo_frame.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.info_prestamo_frame.setFixedWidth(255)
        self.info_prestamo_frame.setFixedHeight(40)
        self.info_prestamo_frame.move(10, 10)
        self.Info_prestamo = QLabel("     Información de Sación", self.info_prestamo_frame)
        self.Info_prestamo.setStyleSheet('color: black')
        self.Info_prestamo.setFont(self.instFont)
        self.Info_prestamo.move(15, 7)

        # Subtitulo estudiante
        self.sub_estudiante = QLabel("Estudiante", self.frame_form_multas)
        self.sub_estudiante.setStyleSheet('color: #858585')
        self.sub_estudiante.setFont(self.subFont)
        self.sub_estudiante.move(120, 57)

        # Carnet de estudiante
        self.currentStudent = "" #Guarda el valor del carnet del estudiante actualmente mostrado en pantalla
        self.carnetLabel = QLabel("Carnet ", self.frame_form_multas)
        self.carnetLabel.move(10, 89)
        self.carnetLabel.setFont(self.subFont)
        self.carnet = QLineEdit(self.frame_form_multas)
        self.carnet.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.carnet.setFixedWidth(150)
        self.carnet.setFixedHeight(25)
        self.carnet.setTextMargins(5, 0, 0, 0)
        self.carnet.move(105, 85)
        self.carnet.setMaxLength(8)

        # Nombre de estudiante
        self.nombreLabel = QLabel("Nombre ", self.frame_form_multas)
        self.nombreLabel.move(10, 119)
        self.nombreLabel.setFont(self.subFont)
        self.nombre = QLineEdit(self.frame_form_multas)
        self.nombre.setReadOnly(True)
        self.nombre.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.nombre.setFixedWidth(150)
        self.nombre.setFixedHeight(25)
        self.nombre.setTextMargins(5, 0, 0, 0)
        self.nombre.move(105, 115)

        # Apellido de estudiante
        self.apellidoLabel = QLabel("Apellido ", self.frame_form_multas)
        self.apellidoLabel.move(10, 149)
        self.apellidoLabel.setFont(self.subFont)
        self.apellido = QLineEdit(self.frame_form_multas)
        self.apellido.setReadOnly(True)
        self.apellido.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.apellido.setFixedWidth(150)
        self.apellido.setFixedHeight(25)
        self.apellido.setTextMargins(5, 0, 0, 0)
        self.apellido.move(105, 145)

        # Numero de dias sancion
        self.deudalabel = QLabel("Deuda Bs. ", self.frame_form_multas)
        self.deudalabel.move(10, 179)
        self.deudalabel.setFont(self.subFont)
        self.deuda = QLineEdit(self.frame_form_multas)
        self.deuda.setReadOnly(True)
        self.deuda.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.deuda.setFixedWidth(150)
        self.deuda.setFixedHeight(25)
        self.deuda.setTextMargins(5, 0, 0, 0)
        self.deuda.move(105, 175)

        # Subtitulo Sanción
        self.sub_estudiante = QLabel("Sanción", self.frame_form_multas)
        self.sub_estudiante.setStyleSheet('color: #858585')
        self.sub_estudiante.setFont(self.subFont)
        self.sub_estudiante.move(120, 219)

        # Numero de dias sancion
        self.sancionLabel = QLabel("Num. Días ", self.frame_form_multas)
        self.sancionLabel.move(10, 249)
        self.sancionLabel.setFont(self.subFont)
        self.sancion = QSpinBox(self.frame_form_multas)
        self.sancion.setValue(0)
        self.sancion.setMinimum(0) 
        self.sancion.setMaximum(365)
        self.sancion.setSuffix(" Días")
        self.sancion.setReadOnly(True)
        self.sancion.setStyleSheet("QSpinBox\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.sancion.setFixedWidth(150)
        self.sancion.setFixedHeight(25)
        self.sancion.move(105, 247)

        # Numero de libros sancion
        self.sancion_booksLabel = QLabel("Num. Libros ", self.frame_form_multas)
        self.sancion_booksLabel.move(10, 279)
        self.sancion_booksLabel.setFont(self.subFont)
        self.sancion_books = QSpinBox(self.frame_form_multas)
        self.sancion_books.setValue(0)
        self.sancion_books.setMinimum(0) 
        self.sancion_books.setMaximum(7)
        self.sancion_books.setSuffix(" Libros")
        self.sancion_books.setReadOnly(True)
        self.sancion_books.setStyleSheet("QSpinBox\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.sancion_books.setFixedWidth(150)
        self.sancion_books.setFixedHeight(25)
        self.sancion_books.move(105, 277)

        # Botón de Aplicar Sanción
        self.button_aplicar = QPushButton("Aplicar", self.frame_form_multas)
        self.button_aplicar.setFixedWidth(200)
        self.button_aplicar.setFixedHeight(28)
        self.button_aplicar.move(40, 319)
        self.button_aplicar.setFont(self.btnFont)
        self.button_aplicar.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_aplicar.setEnabled(False)

        # Botón de Finalizar Sanción
        self.button_finalizar = QPushButton("Finalizar Sanción", self.frame_form_multas)
        self.button_finalizar.setFixedWidth(200)
        self.button_finalizar.setFixedHeight(28)
        self.button_finalizar.move(40, 379)
        self.button_finalizar.setFont(self.btnFont)
        self.button_finalizar.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_finalizar.setEnabled(False)

        # Titulo de tabla de Sanciones
        self.titulo_Sanciones = QFrame(self)
        self.titulo_Sanciones.setFrameShape(QFrame.NoFrame)
        self.titulo_Sanciones.setFrameShadow(QFrame.Sunken)
        self.titulo_Sanciones.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.titulo_Sanciones.setFixedWidth(535)
        self.titulo_Sanciones.setFixedHeight(40)
        self.titulo_Sanciones.move(290, 70)
        self.titulo_SancionesLabel = QLabel("Sanciones Activas", self)
        self.titulo_SancionesLabel.setStyleSheet('background-color: #79B9E0')
        self.titulo_SancionesLabel.setFont(self.instFont)
        self.titulo_SancionesLabel.move(485, 77)

        # Tabla sanciones
        self.tabla_sanciones = Sanciones_Table(self)
        self.tabla_sanciones.move(290, 105)

        # Titulo de tabla de Deudas
        self.titulo_deudas = QFrame(self)
        self.titulo_deudas.setFrameShape(QFrame.NoFrame)
        self.titulo_deudas.setFrameShadow(QFrame.Sunken)
        self.titulo_deudas.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.titulo_deudas.setFixedWidth(535)
        self.titulo_deudas.setFixedHeight(40)
        self.titulo_deudas.move(290, 425)
        self.deudasLabel = QLabel("Deudas Pendientes", self)
        self.deudasLabel.setStyleSheet('background-color: #79B9E0')
        self.deudasLabel.setFont(self.instFont)
        self.deudasLabel.move(485, 432)

        # Tabla de Deudas
        self.debts_table = Debts_Table(self)
        self.debts_table.move(290, 460)