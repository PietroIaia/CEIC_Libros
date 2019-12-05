from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from Tables import Active_Loan_Table, Debts_Table
import sys
import datetime 


class Inicio(QWidget):

    def __init__(self):

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
        self.title.setText("Inicio")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 350, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Titulo de tabla de Deudas
        self.titulo_Deudas = QFrame(self)
        self.titulo_Deudas.setFrameShape(QFrame.NoFrame)
        self.titulo_Deudas.setFrameShadow(QFrame.Sunken)
        self.titulo_Deudas.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.titulo_Deudas.setFixedWidth(536)
        self.titulo_Deudas.setFixedHeight(40)
        self.titulo_Deudas.move(290, 88)
        self.Deudas = QLabel("Deudas Activas", self.titulo_Deudas)
        self.Deudas.setStyleSheet('background-color: #79B9E0')
        self.Deudas.setFont(self.instFont)
        self.Deudas.move(192, 8)

        # Tabla de Deudas
        self.debts_table = Debts_Table(self)
        self.debts_table.move(290, 125)

        # Titulo de tabla de prestamos activos
        self.titulo_prestamos = QFrame(self)
        self.titulo_prestamos.setFrameShape(QFrame.NoFrame)
        self.titulo_prestamos.setFrameShadow(QFrame.Sunken)
        self.titulo_prestamos.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.titulo_prestamos.setFixedWidth(796)
        self.titulo_prestamos.setFixedHeight(40)
        self.titulo_prestamos.move(30, 382)
        self.prestamos = QLabel("Prestamos Activos", self.titulo_prestamos)
        self.prestamos.setStyleSheet('background-color: #79B9E0')
        self.prestamos.setFont(self.instFont)
        self.prestamos.move(310, 8)

        # Tabla Prestamos activos
        self.active_loan_table = Active_Loan_Table(self)
        self.active_loan_table.setMaximumHeight(300)
        self.active_loan_table.setMinimumHeight(300)
        self.active_loan_table.move(30, 420)

        # Frame de actualizar Deuda agregada por dia
        self.frame_deuda = QFrame(self)
        self.frame_deuda.setFrameShape(QFrame.StyledPanel)
        self.frame_deuda.setFixedWidth(255)
        self.frame_deuda.setFixedHeight(150)
        self.frame_deuda.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: white;\n"
        "}")
        self.frame_deuda.move(28, 90)

        # Actualizar Monto Deuda
        self.info_prestamo_frame = QFrame(self.frame_deuda)
        self.info_prestamo_frame.setFrameShape(QFrame.NoFrame)
        self.info_prestamo_frame.setFrameShadow(QFrame.Sunken)
        self.info_prestamo_frame.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.info_prestamo_frame.setFixedWidth(235)
        self.info_prestamo_frame.setFixedHeight(40)
        self.info_prestamo_frame.move(10, 10)
        self.Info_prestamo = QLabel("Libros por prestamo", self.info_prestamo_frame)
        self.Info_prestamo.setStyleSheet('color: black')
        self.Info_prestamo.setFont(self.instFont)
        self.Info_prestamo.move(50, 7)

        # Monto deuda por dia
        self.act_deuda_label = QLabel("Cantidad ", self.frame_deuda)
        self.act_deuda_label.move(10, 69)
        self.act_deuda_label.setFont(self.subFont)
        self.books_per_loan = QSpinBox(self.frame_deuda)
        self.books_per_loan.move(85, 67)
        self.query = QSqlQuery()
        self.query.exec_("SELECT monto_libro_per_loan FROM Books_per_loan WHERE id = 0;")
        self.query.first()
        self.books_per_loan.setValue(self.query.value(0))
        self.books_per_loan.setMinimum(0) 
        self.books_per_loan.setMaximum(7)
        self.books_per_loan.setSuffix(" Libros")
        self.books_per_loan.setStyleSheet("QSpinBox\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.books_per_loan.setFixedWidth(150)
        self.books_per_loan.setFixedHeight(25)

        # Boton Actualizar Monto deuda
        self.button_act_monto = QPushButton("Actualizar", self.frame_deuda)
        self.button_act_monto.setFixedWidth(120)
        self.button_act_monto.setFixedHeight(28)
        self.button_act_monto.move(120, 110)
        self.button_act_monto.setFont(self.btnFont)
        self.button_act_monto.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")

        # Conexiones
        self.button_act_monto.clicked.connect(self.updateBooksPerLoan)

        # Montar tabla de prestamos activos
        self.updateActiveLoanTable()
        # Montar tabla de deudas activas
        self.updateDebtTabla()


    # Funcion para calcular el tiempo restante de el prestamo
    def calculateTimeLeft(self, start_time, return_time):
        startTimeAux = QDateTime.toSecsSinceEpoch(start_time)
        returnTimeAux = QDateTime.toSecsSinceEpoch(return_time)

        aux = (int(returnTimeAux) - int(startTimeAux))/86400
        return aux


    def updateBooksPerLoan(self):
        self.query = QSqlQuery()

        success = self.query.exec_("UPDATE Books_per_loan SET monto_libro_per_loan = '" + str(self.books_per_loan.value()) + "' WHERE id = 0;")
        if(success):
            InfoPrompt("Éxito", "Máximo de libros por prestamo actualizado!")
        else:
            ErrorPrompt("Error", "No se pudo actualizar la cantidad máxima de libros por prestamo")


    # Funcion que actualiza la tabla de prestamos activos
    def updateActiveLoanTable(self):
        self.active_loan_table.clear()
        queryText = "SELECT L.carnet, e.first_name, e.last_name, L.estimated_return_time, L.book_id, L.copy_id FROM Loan L, Estudiante e WHERE L.carnet = e.carnet;"
        self.query = QSqlQuery()
        self.query2 = QSqlQuery()
        self.query.exec_(queryText)
        i = -1

        if(self.query.first()):
            oldStudent = ""
            while(True):
                newStudent = self.query.value(0)
                if(newStudent != oldStudent):
                    i += 1
                    self.active_loan_table.item(i, 0).setText(str(self.query.value(0)))
                    self.active_loan_table.item(i, 1).setText(str(self.query.value(1)))
                    self.active_loan_table.item(i, 2).setText(str(self.query.value(2)))
                    time_left = int(self.calculateTimeLeft(QDateTime.currentDateTime(), self.query.value(3))//1)
                    self.active_loan_table.item(i, 3).setText(str(time_left) + " Dias")
                    self.query2.exec_("SELECT title FROM Book WHERE book_id ='" + str(self.query.value(4)) + "';")
                    self.query2.first()
                    self.active_loan_table.item(i, 4).setText(str(self.query2.value(0)))
                else:
                    # Buscamos el intervalo de prestamo mas pequeño y ese sera el intervalo de prestamo del prestamo
                    if((self.calculateTimeLeft(QDateTime.currentDateTime(), self.query.value(3))//1) <= time_left):
                        time_left = int(self.calculateTimeLeft(QDateTime.currentDateTime(), self.query.value(3))//1)
                        self.active_loan_table.item(i, 3).setText(str(time_left) + " Dias")

                    self.query2.exec_("SELECT title FROM Book WHERE book_id ='" + str(self.query.value(4)) + "';")
                    self.query2.first()
                    self.active_loan_table.item(i, 4).setText(self.active_loan_table.item(i, 4).text() + ", " + str(self.query2.value(0)))

                oldStudent = self.query.value(0)
                if(not self.query.next()):
                    break
        
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