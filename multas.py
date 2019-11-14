from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from Tables import Payments_Table, Debts_Table
from validationFunctions import checkPattern, checkCarnet
import sys
import datetime 


# NOTAS:
# - Entre Labels dentro del frame "Informacion de prestamo" hay 30px de espacio

class multas(QWidget):

    def __init__(self, Username):

        # Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de Estudiantes")
        self.setStyleSheet('background-color: LightSkyBlue')

        # Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.instFont = QFont("Serif", 12)
        self.subFont = QFont("Serif", 10)
        self.btnFont = QFont("Serif", 9)
        self.smallbtn = QFont("Serif", 7)


        # Título
        self.title = QLabel("Multas", self)
        self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)
        self.title.move(30, 10)


        # Frame del form
        self.frame_form_multas = QFrame(self)
        self.frame_form_multas.setFrameShape(QFrame.StyledPanel)
        self.frame_form_multas.setFixedWidth(275)
        self.frame_form_multas.setFixedHeight(420)
        self.frame_form_multas.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: white;\n"
        "}")
        self.frame_form_multas.move(10, 120)

        # Informacion de prestamo
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
        self.Info_prestamo = QLabel("Transacción", self.info_prestamo_frame)
        self.Info_prestamo.setStyleSheet('color: black')
        self.Info_prestamo.setFont(self.instFont)
        self.Info_prestamo.move(80, 10)

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
        self.carnet.move(85, 85)
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
        self.nombre.move(85, 115)

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
        self.apellido.move(85, 145)

        # Deuda de estudiante
        self.deudaLabel = QLabel("Deuda ", self.frame_form_multas)
        self.deudaLabel.move(10, 179)
        self.deudaLabel.setFont(self.subFont)
        self.deuda = QLineEdit(self.frame_form_multas)
        self.deuda.setReadOnly(True)
        self.deuda.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.deuda.setFixedWidth(150)
        self.deuda.setFixedHeight(25)
        self.deuda.setTextMargins(5, 0, 0, 0)
        self.deuda.move(85, 175)

        # Subtitulo estudiante
        self.sub_estudiante = QLabel("Pago", self.frame_form_multas)
        self.sub_estudiante.setStyleSheet('color: #858585')
        self.sub_estudiante.setFont(self.subFont)
        self.sub_estudiante.move(140, 219)

        # Método de pago a utilizar
        self.tipoLabel = QLabel("Tipo ", self.frame_form_multas)
        self.tipoLabel.move(10, 249)
        self.tipoLabel.setFont(self.subFont)
        self.tipo = QComboBox(self.frame_form_multas)
        self.tipo.addItem("Transferencia")
        self.tipo.addItem("Divisas")
        self.tipo.setStyleSheet("QComboBox\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.tipo.setFixedWidth(150)
        self.tipo.setFixedHeight(25)
        self.tipo.move(85, 245)
        self.tipo.setEnabled(False)

        # Monto a cancelar
        self.montoLabel = QLabel("Monto ", self.frame_form_multas)
        self.montoLabel.move(10, 279)
        self.montoLabel.setFont(self.subFont)
        self.monto = QLineEdit(self.frame_form_multas)
        self.monto.setReadOnly(True)
        self.monto.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.monto.setFixedWidth(150)
        self.monto.setFixedHeight(25)
        self.monto.setTextMargins(5, 0, 0, 0)
        self.monto.move(85, 275)

        # Banco del estudiante
        self.bancoLabel = QLabel("Banco ", self.frame_form_multas)
        self.bancoLabel.move(10, 309)
        self.bancoLabel.setFont(self.subFont)
        self.banco = QLineEdit(self.frame_form_multas)
        self.banco.setReadOnly(True)
        self.banco.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.banco.setFixedWidth(150)
        self.banco.setFixedHeight(25)
        self.banco.setTextMargins(5, 0, 0, 0)
        self.banco.move(85, 305)

        # Referencia de transferencia
        self.codigoLabel = QLabel("Código ", self.frame_form_multas)
        self.codigoLabel.move(10, 339)
        self.codigoLabel.setFont(self.subFont)
        self.codigo = QLineEdit(self.frame_form_multas)
        self.codigo.setReadOnly(True)
        self.codigo.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.codigo.setFixedWidth(150)
        self.codigo.setFixedHeight(25)
        self.codigo.setTextMargins(5, 0, 0, 0)
        self.codigo.move(85, 335)

        # Botón de Cancelar
        self.button_cancelar = QPushButton("Cancelar", self.frame_form_multas)
        self.button_cancelar.setFixedWidth(90)
        self.button_cancelar.setFixedHeight(28)
        self.button_cancelar.move(25, 375)
        self.button_cancelar.setFont(self.btnFont)
        self.button_cancelar.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_cancelar.setEnabled(False)

        # Botón de Aplicar
        self.button_aplicar = QPushButton("Aplicar Pago", self.frame_form_multas)
        self.button_aplicar.setFixedWidth(90)
        self.button_aplicar.setFixedHeight(28)
        self.button_aplicar.move(165, 375)
        self.button_aplicar.setFont(self.btnFont)
        self.button_aplicar.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_aplicar.setEnabled(False)

        # Tabla de transferencias

        # Titulo de tabla de Transferencias
        self.titulo_transfer = QFrame(self)
        self.titulo_transfer.setFrameShape(QFrame.NoFrame)
        self.titulo_transfer.setFrameShadow(QFrame.Sunken)
        self.titulo_transfer.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.titulo_transfer.setFixedWidth(535)
        self.titulo_transfer.setFixedHeight(40)
        self.titulo_transfer.move(290, 40)
        self.transfer = QLabel("Transferencias", self)
        self.transfer.setStyleSheet('background-color: #79B9E0')
        self.transfer.setFont(self.instFont)
        self.transfer.move(485, 47)

        self.tabla_transferencias = Payments_Table(self)
        self.tabla_transferencias.move(290, 80)

        # Tabla de Deudas

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
        self.titulo_deudas.move(290, 410)
        self.deudas = QLabel("Deudas Pendientes", self)
        self.deudas.setStyleSheet('background-color: #79B9E0')
        self.deudas.setFont(self.instFont)
        self.deudas.move(485, 417)

        self.debts_table = Debts_Table(self)
        self.debts_table.move(290, 450)

        # Conexiones
        self.carnet.returnPressed.connect(lambda: self.buscarEstudiante(self.carnet.text()))


    # Funcion que busca al estudiante con su informacion acerca de prestamos
    def buscarEstudiante(self, carnetBuscado):
        if(checkCarnet(carnetBuscado)):
            self.currentStudent = carnetBuscado
            queryText = "SELECT * FROM Estudiante WHERE carnet = '" + carnetBuscado + "';"
            self.query = QSqlQuery()
            self.query.exec_(queryText)

            if self.query.first():
                self.tabla_transferencias.clear()
                self.nombre.setText(str(self.query.value(1)))
                self.apellido.setText(str(self.query.value(2)))
                self.deuda.setText(str(self.query.value(8)))
                self.tipo.setEnabled(True)
                self.monto.setReadOnly(False)
                self.banco.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")                
                self.banco.setReadOnly(False)
                self.codigo.setReadOnly(False)
            else:
                ErrorPrompt("Error", "No se encontró un Estudiante con ese carnet")


    # Funcion para calcular el tiempo restante de el prestamo
    def calculateTimeLeft(self, start_time, return_time):
        startTimeAux = QDateTime.toSecsSinceEpoch(start_time)
        returnTimeAux = QDateTime.toSecsSinceEpoch(return_time)

        aux = (int(returnTimeAux) - int(startTimeAux))/86400
        return aux

    
    # Funcion que actualiza la tabla de prestamos activos
    def updateActiveLoanTable(self):
        queryText = "SELECT carnet, first_name, last_name FROM Loan L, Estudiante e WHERE L.carnet = e.carnet;"
        self.query = QSqlQuery()
        self.query.exec_(queryText)
        i = 0

        if(self.query.first()):
            oldStudent = self.query.value(0)
            while(True):
                newStudent = self.query.value(0)
                if(newStudent != oldStudent):
                    self.debts_table.item(i, 0).setText(str(self.query.value(0)))
                    self.debts_table.item(i, 1).setText(str(self.query.value(1)))