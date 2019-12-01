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
        self.deudasLabel = QLabel("Estudiantes endeudados", self)
        self.deudasLabel.setStyleSheet('background-color: #79B9E0')
        self.deudasLabel.setFont(self.instFont)
        self.deudasLabel.move(455, 432)

        # Tabla de Deudas
        self.debts_table = Debts_Table(self)
        self.debts_table.move(290, 460)

        # Conexiones
        self.carnet.returnPressed.connect(lambda: self.buscarEstudiante(self.carnet.text()))
        self.button_aplicar.clicked.connect(self.realizarSancion)
        self.button_finalizar.clicked.connect(lambda: self.finalizarSancion(self.currentStudent, True))

        # Montar Tabla de Deudores
        self.updateDebtTabla()
        # Montar Tabla de Sanciones
        self.updateSancionTable()


    # Funcion que busca al estudiante con su informacion acerca de sanciones
    def buscarEstudiante(self, carnetBuscado):
        if(check_carnet(carnetBuscado)):
            queryText = "SELECT * FROM Estudiante WHERE carnet = '" + carnetBuscado + "';"
            self.query = QSqlQuery()
            self.query.exec_(queryText)

            if self.query.first():
                self.currentStudent = carnetBuscado
                self.nombre.setText(str(self.query.value(1)))
                self.apellido.setText(str(self.query.value(2)))
                self.sancion.setValue(int(self.query.value(6)))
                self.sancion_books.setValue(int(self.query.value(7)))
                self.deuda.setText(str(self.query.value(9)))

                self.sancion.setReadOnly(False)
                self.sancion.setStyleSheet("QSpinBox\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
                self.sancion_books.setReadOnly(False)
                self.sancion_books.setStyleSheet("QSpinBox\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")

                self.button_aplicar.setEnabled(True)
                if(self.query.value(6) >= 1):
                    self.button_finalizar.setEnabled(True)
                else:
                    self.button_finalizar.setEnabled(False)
            else:
                ErrorPrompt("Error", "No se encontró un Estudiante con ese carnet")
        
        # Actualizamos las tablas
        self.updateDebtTabla()
        self.updateSancionTable()

    
    # Funcion que aplica la sancion al estudiante
    def realizarSancion(self):

        if(self.sancion.value() == 0):
            ErrorPrompt("Error", "Las sanciones deben durar al menos 1 dia!")
            return
        if(self.sancion_books.value() == 7):
            ErrorPrompt("Error", "La cantidad de libro por prestamo durante la sanción debe ser menor a 7!")
            return
        
        self.query = QSqlQuery()
        queryText = "UPDATE Estudiante SET days_blocked = '" + str(self.sancion.value()) + "', num_books_per_loan = '" + str(self.sancion_books.value()) + "', start_blocked_time = '"+  str(datetime.date.today()) +"' WHERE carnet = '" + str(self.currentStudent) + "';"
        success = self.query.exec_(queryText)

        if(not success):
            ErrorPrompt("Error", "No se pudo realizar la sanción.")
            return

        self.button_finalizar.setEnabled(True)
        InfoPrompt("Éxito", "La sanción ha sido impuesta con éxito!")
        # Actualizamos las tablas
        self.updateDebtTabla()
        self.updateSancionTable()
        

    # Funcion que finaliza la sancion, si prompt == True, devuelve un prompt con la informacion.
    def finalizarSancion(self, carnet, prompt):
        self.query = QSqlQuery()
        queryText = "UPDATE Estudiante SET days_blocked = '0', num_books_per_loan = '7', start_blocked_time = NULL WHERE carnet = '" + str(carnet) + "';"
        success = self.query.exec_(queryText)

        if(not success and prompt):
            ErrorPrompt("Error", "No se pudo finalizar la sanción.")
            return
        elif(success and prompt):
            self.button_finalizar.setEnabled(False)
            self.sancion.setValue(0)
            self.sancion_books.setValue(7)
            InfoPrompt("Éxito", "La sanción ha sido finalizada con éxito!")
            # Actualizamos las tablas
            self.updateDebtTabla()
            self.updateSancionTable()


    # Funcion que actualiza la tabla de Estudiantes endeudados
    def updateDebtTabla(self):
        self.debts_table.clear()
        queryText = "SELECT e.carnet, e.first_name, e.last_name, e.book_debt FROM Estudiante e WHERE e.book_debt > 0.0;"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        i = 0
        if(self.query.first()):
            while(True):
                self.debts_table.item(i, 0).setText(str(self.query.value(0)))
                self.debts_table.item(i, 1).setText(str(self.query.value(1)))
                self.debts_table.item(i, 2).setText(str(self.query.value(2)))
                self.debts_table.item(i, 3).setText(str(self.query.value(3)))

                i+= 1
                if(not self.query.next()):
                    break

    
    # Funcion para calcular el tiempo restante de la sancion
    def calculateTimeLeft(self, current_time, start_time, days):
        currentTimeAux = QDateTime.toSecsSinceEpoch(current_time)
        finishTimeAux = QDateTime.toSecsSinceEpoch(start_time) + (days * 86400)  #El tiempo de inicio mas los dias que quedan

        aux = (int(finishTimeAux) - int(currentTimeAux))/86400
        return aux


    # Funcion que actualiza la tabla de Sanciones activas
    def updateSancionTable(self):
        self.tabla_sanciones.clear()
        queryText = "SELECT e.carnet, e.first_name, e.last_name, e.days_blocked, e.num_books_per_loan, e.start_blocked_time FROM Estudiante e WHERE e.days_blocked >= 1;"
        self.query = QSqlQuery()
        self.query2 = QSqlQuery()
        self.query.exec_(queryText)

        i = 0
        if(self.query.first()):
            while(True):
                
                # Primero actualizamos el tiempo restante de la sancion
                time_left = int((self.calculateTimeLeft(QDateTime.currentDateTime(), self.query.value(5), self.query.value(3))//1) + 1)
                self.query2.exec_("UPDATE Estudiante SET days_blocked = '" + str(time_left) + "' WHERE carnet = '" + self.query.value(0) + "';")
                # Si la duracion de la sancion no se ha cumplido, aparece en la tabla
                if(int(time_left) >= 1):
                    self.tabla_sanciones.item(i, 0).setText(str(self.query.value(0)))
                    self.tabla_sanciones.item(i, 1).setText(str(self.query.value(1)))
                    self.tabla_sanciones.item(i, 2).setText(str(self.query.value(2)))
                    self.tabla_sanciones.item(i, 3).setText(str(time_left))
                    self.tabla_sanciones.item(i, 4).setText(str(self.query.value(4)))
                    i+= 1
                # Si la duracion ya se cumplio, no aparece en la tabla y se restaura la cuenta a la normalidad
                else:
                    self.finalizarSancion(self.query.value(0), False)

                if(not self.query.next()):
                    break