from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from Tables import Books_Loan_Table, Active_Loan_Table
from validationFunctions import checkPattern, checkCarnet, checkTitle
import sys
import datetime 


# NOTAS:
# - Entre Labels dentro del frame "Informacion de prestamo" hay 30px de espacio

class prestamos(QWidget):

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
        self.title = QLabel("Préstamos", self)
        self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)
        self.title.move(30, 10)

        # Frame del form
        self.frame_form_prestamo = QFrame(self)
        self.frame_form_prestamo.setFrameShape(QFrame.StyledPanel)
        self.frame_form_prestamo.setFixedWidth(275)
        self.frame_form_prestamo.setFixedHeight(430)
        self.frame_form_prestamo.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: white;\n"
        "}")
        self.frame_form_prestamo.move(30, 60)

        # Informacion de prestamo
        self.info_prestamo_frame = QFrame(self.frame_form_prestamo)
        self.info_prestamo_frame.setFrameShape(QFrame.NoFrame)
        self.info_prestamo_frame.setFrameShadow(QFrame.Sunken)
        self.info_prestamo_frame.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.info_prestamo_frame.setFixedWidth(255)
        self.info_prestamo_frame.setFixedHeight(40)
        self.info_prestamo_frame.move(10, 10)
        self.Info_prestamo = QLabel("Información de prestamo", self.info_prestamo_frame)
        self.Info_prestamo.setStyleSheet('color: black')
        self.Info_prestamo.setFont(self.instFont)
        self.Info_prestamo.move(15, 7)

        # Subtitulo estudiante
        self.sub_estudiante = QLabel("Estudiante", self.frame_form_prestamo)
        self.sub_estudiante.setStyleSheet('color: #858585')
        self.sub_estudiante.setFont(self.subFont)
        self.sub_estudiante.move(100, 57)

        # Carnet de estudiante
        self.currentStudent = "" #Guarda el valor del carnet del estudiante actualmente mostrado en pantalla
        self.carnetLabel = QLabel("Carnet ", self.frame_form_prestamo)
        self.carnetLabel.move(10, 87)
        self.carnetLabel.setFont(self.subFont)
        self.carnet = QLineEdit(self.frame_form_prestamo)
        self.carnet.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.carnet.setFixedWidth(150)
        self.carnet.setFixedHeight(25)
        self.carnet.setTextMargins(5, 0, 0, 0)
        self.carnet.move(85, 85)
        self.carnet.setMaxLength(8)

        # Nombre de estudiante
        self.nombreLabel = QLabel("Nombre ", self.frame_form_prestamo)
        self.nombreLabel.move(10, 117)
        self.nombreLabel.setFont(self.subFont)
        self.nombre = QLineEdit(self.frame_form_prestamo)
        self.nombre.setReadOnly(True)
        self.nombre.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.nombre.setFixedWidth(150)
        self.nombre.setFixedHeight(25)
        self.nombre.setTextMargins(5, 0, 0, 0)
        self.nombre.move(85, 115)

        # Nombre de estudiante
        self.apellidoLabel = QLabel("Apellido ", self.frame_form_prestamo)
        self.apellidoLabel.move(10, 147)
        self.apellidoLabel.setFont(self.subFont)
        self.apellido = QLineEdit(self.frame_form_prestamo)
        self.apellido.setReadOnly(True)
        self.apellido.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.apellido.setFixedWidth(150)
        self.apellido.setFixedHeight(25)
        self.apellido.setTextMargins(5, 0, 0, 0)
        self.apellido.move(85, 145)

        # Prestamo activo de estudiante
        self.prestamoLabel = QLabel("Préstamo ", self.frame_form_prestamo)
        self.prestamoLabel.move(10, 177)
        self.prestamoLabel.setFont(self.subFont)
        self.prestamo = QLineEdit(self.frame_form_prestamo)
        self.prestamo.setReadOnly(True)
        self.prestamo.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.prestamo.setFixedWidth(150)
        self.prestamo.setFixedHeight(25)
        self.prestamo.setTextMargins(5, 0, 0, 0)
        self.prestamo.move(85, 175)

        # Deuda de estudiante
        self.deudaLabel = QLabel("Deuda ", self.frame_form_prestamo)
        self.deudaLabel.move(10, 207)
        self.deudaLabel.setFont(self.subFont)
        self.deuda = QLineEdit(self.frame_form_prestamo)
        self.deuda.setReadOnly(True)
        self.deuda.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: #F2F2F2;\n}")
        self.deuda.setFixedWidth(150)
        self.deuda.setFixedHeight(25)
        self.deuda.setTextMargins(5, 0, 0, 0)
        self.deuda.move(85, 205)

        # Renovar prestamo
        self.button_renovar = QPushButton("Renovar Préstamo", self.frame_form_prestamo)
        self.button_renovar.setFixedWidth(180)
        self.button_renovar.setFixedHeight(28)
        self.button_renovar.move(55, 240)
        self.button_renovar.setFont(self.btnFont)
        self.button_renovar.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_renovar.setEnabled(False)

        # Subtitulo estudiante
        self.sub_libro = QLabel("Libro", self.frame_form_prestamo)
        self.sub_libro.setStyleSheet('color: #858585')
        self.sub_libro.setFont(self.subFont)
        self.sub_libro.move(120, 277)

        # Libro a prestar
        self.libroLabel = QLabel("Libro ", self.frame_form_prestamo)
        self.libroLabel.move(10, 307)
        self.libroLabel.setFont(self.subFont)
        self.libro = QLineEdit(self.frame_form_prestamo)
        self.libro.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.libro.setFixedWidth(150)
        self.libro.setFixedHeight(25)
        self.libro.setTextMargins(5, 0, 0, 0)
        self.libro.move(85, 305)
        self.libro.setEnabled(False)

        # Agregar libro al prestamo
        self.button_agregar_libro = QPushButton("Agregar Libro", self.frame_form_prestamo)
        self.button_agregar_libro.setFixedWidth(180)
        self.button_agregar_libro.setFixedHeight(28)
        self.button_agregar_libro.move(55, 340)
        self.button_agregar_libro.setFont(self.btnFont)
        self.button_agregar_libro.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_agregar_libro.setEnabled(False)

        # Marcar prestamo como finalizado
        self.button_devuelto = QPushButton("Finalizar Préstamo", self.frame_form_prestamo)
        self.button_devuelto.setFixedWidth(110)
        self.button_devuelto.setFixedHeight(28)
        self.button_devuelto.move(22, 390)
        self.button_devuelto.setFont(self.smallbtn)
        self.button_devuelto.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_devuelto.setEnabled(False)

        # Realizar prestamo
        self.button_realizar = QPushButton("Realizar Préstamo", self.frame_form_prestamo)
        self.button_realizar.setFixedWidth(110)
        self.button_realizar.setFixedHeight(28)
        self.button_realizar.move(142, 390)
        self.button_realizar.setFont(self.smallbtn)
        self.button_realizar.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_realizar.setEnabled(False)

        # Refrescar tabla prestamo
        self.button_refrescar = QPushButton("Refrescar Tabla", self)
        self.button_refrescar.setFixedWidth(150)
        self.button_refrescar.setFixedHeight(28)
        self.button_refrescar.move(647, 690)
        self.button_refrescar.setFont(self.btnFont)
        self.button_refrescar.setStyleSheet("QPushButton\n{\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_refrescar.setEnabled(True)

        # Tabla de prestamos
        self.Libros_prestamo = {}         # Para saber los libros que se van a prestar
        self.tabla_libros_prestamos = Books_Loan_Table(self)
        self.tabla_libros_prestamos.move(305, 60)

        # Tabla de prestamos activos
        # NOTA: Para agregar nuevas filas, usamos table.insertRow(rowPosition) donde rowposition es donde la queremos poner (de ultima) https://stackoverflow.com/questions/24044421/how-to-add-a-row-in-a-tablewidget-pyqt
        self.active_loan_table = Active_Loan_Table(self)
        self.active_loan_table.move(30, 500)
        self.updateActiveLoanTable()                      # Actualizamos la tabla con los prestamos activos

        # Conexiones
        self.carnet.returnPressed.connect(lambda: self.buscarEstudiante(self.carnet.text()))
        self.button_agregar_libro.clicked.connect(lambda: self.buscarLibro(self.libro.text()))
        self.button_realizar.clicked.connect(lambda: self.realizarPrestamo(Username))
        self.button_devuelto.clicked.connect(lambda: self.finalizarPrestamo())
        self.button_refrescar.clicked.connect(self.updateActiveLoanTable)
        self.button_renovar.clicked.connect(self.renovarPrestamo)
        # NOTA: Si se agregan mas filas, no van a tener una conexion con los botones. Luego podemos arreglar eso!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tabla_libros_prestamos.cellWidget(0, 2).clicked.connect(lambda: self.eliminarLibro(0))
        self.tabla_libros_prestamos.cellWidget(1, 2).clicked.connect(lambda: self.eliminarLibro(1))
        self.tabla_libros_prestamos.cellWidget(2, 2).clicked.connect(lambda: self.eliminarLibro(2))
        self.tabla_libros_prestamos.cellWidget(3, 2).clicked.connect(lambda: self.eliminarLibro(3))
        self.tabla_libros_prestamos.cellWidget(4, 2).clicked.connect(lambda: self.eliminarLibro(4))
        self.tabla_libros_prestamos.cellWidget(5, 2).clicked.connect(lambda: self.eliminarLibro(5))
        self.tabla_libros_prestamos.cellWidget(6, 2).clicked.connect(lambda: self.eliminarLibro(6))


    # Funcion que busca al estudiante con su informacion acerca de prestamos
    def buscarEstudiante(self, carnetBuscado):
        if(checkCarnet(carnetBuscado)):
            self.currentStudent = carnetBuscado
            queryText = "SELECT * FROM Estudiante WHERE carnet = '" + carnetBuscado + "';"
            self.query = QSqlQuery()
            self.query.exec_(queryText)

            if self.query.first():
                self.tabla_libros_prestamos.clear()
                self.Libros_prestamo.clear()
                self.nombre.setText(str(self.query.value(1)))
                self.apellido.setText(str(self.query.value(2)))
                self.deuda.setText(str(self.query.value(8)))
                for i in range(self.tabla_libros_prestamos.rowCount()):
                    self.tabla_libros_prestamos.cellWidget(i, 2).setText("")
                    self.tabla_libros_prestamos.cellWidget(i, 2).setEnabled(False)

                queryText ="SELECT L.book_id, B.title, L.estimated_return_time FROM Loan L, Book B WHERE L.carnet = '" + carnetBuscado + "' AND L.book_id = B.book_id;"
                self.query.exec_(queryText)
                if self.query.first():
                    self.prestamo.setText("Prestamo activo")
                    self.libro.setEnabled(False)
                    self.button_agregar_libro.setEnabled(False)
                    self.button_realizar.setEnabled(False)
                    self.button_devuelto.setEnabled(True)

                    # Si le queda menos de 1 dia para regresar el libro, permitimos la renovacion
                    time_left = 10000

                    i = 0
                    while(True):
                        self.tabla_libros_prestamos.item(i, 0).setText(str(self.query.value(0)))
                        self.tabla_libros_prestamos.item(i, 1).setText(str(self.query.value(1)))
                        # Buscamos el intervalo de prestamo mas pequeño y ese sera el intervalo de prestamo del prestamo
                        if(self.calculateTimeLeft(QDateTime.currentDateTime(), self.query.value(2)) <= time_left):
                            time_left = self.calculateTimeLeft(QDateTime.currentDateTime(), self.query.value(2))

                        i += 1
                        if(not self.query.next()):
                            break
                    
                    # Si al prestamo le falta 1 dia para vencerse, se deja renovar
                    if(time_left < 2):
                        self.button_renovar.setEnabled(True)

                else:
                    self.prestamo.setText("No prestamo activo")

                    self.libro.setEnabled(True)
                    self.button_agregar_libro.setEnabled(True)
                    self.button_devuelto.setEnabled(False)

            else:
                ErrorPrompt("Error", "No se encontró un Estudiante con ese carnet")
    

    # Funcion para buscar el libro e ingresarlo a la tabla de libros Prestamos cuando se este realizando un prestamo
    def buscarLibro(self, Libro):
        if(checkTitle(Libro)):
            queryText = "SELECT * FROM Book WHERE title = '" + Libro + "';"
            self.query = QSqlQuery()
            self.query.exec_(queryText)
            if(self.query.first()):
                i = 0
                while(i != self.tabla_libros_prestamos.rowCount()):
                    if(self.tabla_libros_prestamos.item(i, 0).text() != ""):
                        i += 1
                    elif(self.tabla_libros_prestamos.item(i, 0).text() == ""):
                        break

                    if(i == self.tabla_libros_prestamos.rowCount()):
                        ErrorPrompt("Error", "Todas las casillas estan llenas, no puede pedir otro libro.")
                        return

                # Si el libro esta en el diccionario y hay menos ejemplares que el total disponible de ese libro, se le permite agregarlo al prestamo
                if(str(Libro) in self.Libros_prestamo.keys() and self.Libros_prestamo[str(Libro)] < (self.query.value(4) - self.query.value(5))):
                    self.Libros_prestamo[str(Libro)] += 1
                    self.tabla_libros_prestamos.item(i, 0).setText(str(self.query.value(0)))
                    self.tabla_libros_prestamos.item(i, 1).setText(str(Libro))
                    self.tabla_libros_prestamos.cellWidget(i, 2).setEnabled(True)
                    self.tabla_libros_prestamos.cellWidget(i, 2).setText("X")
                # Si el libro no esta en el diccionario, se agrega
                elif(str(Libro) not in self.Libros_prestamo.keys()):
                    self.Libros_prestamo[str(Libro)] = 0
                    # Si se estan prestando menos ejemplares que el total disponible de ese libro, se le permite agregarlo al prestamo
                    if(self.Libros_prestamo[str(Libro)] < (self.query.value(4) - self.query.value(5))):
                        self.Libros_prestamo[str(Libro)] = 1
                        self.tabla_libros_prestamos.item(i, 0).setText(str(self.query.value(0)))
                        self.tabla_libros_prestamos.item(i, 1).setText(str(Libro))
                        self.tabla_libros_prestamos.cellWidget(i, 2).setEnabled(True)
                        self.tabla_libros_prestamos.cellWidget(i, 2).setText("X")
                else:
                    ErrorPrompt("Error", "No existen mas ejemplares disponibles de este libro")
            else:
                ErrorPrompt("Error", "No se encontró el Libro especificado")

            self.button_realizar.setEnabled(True)


    # Funcion para calcular el tiempo restante de el prestamo
    def calculateTimeLeft(self, start_time, return_time):
        startTimeAux = QDateTime.toSecsSinceEpoch(start_time)
        returnTimeAux = QDateTime.toSecsSinceEpoch(return_time)

        aux = (int(returnTimeAux) - int(startTimeAux))/86400
        return aux


    # Funcion para realizar el prestamo
    def realizarPrestamo(self, Username):
        self.query = QSqlQuery()
        start_date = str(datetime.datetime.now())
        hours = start_date.split()

        i = 0
        while(i != self.tabla_libros_prestamos.rowCount()):
            if(self.tabla_libros_prestamos.item(i, 0).text() != ""):
                queryText = "INSERT INTO Loan (carnet, lender, start_time, book_id, copy_id, estimated_return_time) VALUES ('" + self.carnet.text() + "', '" + Username + "', '" + start_date + "', "
                self.query.exec_("SELECT loan_duration FROM Book WHERE book_id = '" + self.tabla_libros_prestamos.item(i, 0).text() + "';")

                # Aqui completamos el queryText con la informacion faltante y restamos la cantidad de copias de cada libro en el diccionario
                if(self.query.first()):
                    return_date = str(datetime.date.today() + datetime.timedelta(days=(self.query.value(0)))) + " " + str(hours[1])
                    queryText = queryText + "'" + str(self.tabla_libros_prestamos.item(i, 0).text()) + "', '" + str(self.Libros_prestamo[str(self.tabla_libros_prestamos.item(i, 1).text())]) +"', '" + return_date + "');"
                    self.Libros_prestamo[str(self.tabla_libros_prestamos.item(i, 1).text())] -= 1
                    # Se actualiza la cantidad de copias prestadas del libro
                    self.query.exec_("UPDATE Book SET quantity_lent = quantity_lent + 1 WHERE book_id='" + str(self.tabla_libros_prestamos.item(i, 0).text()) + "';")
                    # Se realiza la insercion a la tabla Loan, es decir, se realiza el prestamo
                    self.query.exec_(queryText)

                    i += 1
                else: 
                    ErrorPrompt("Error", "No se pudo realizar el préstamo")
                    return
            else:
                break
        InfoPrompt("Éxito", "Se realizo el préstamo!")
        self.button_agregar_libro.setEnabled(False)
        self.button_realizar.setEnabled(False)
    

    # Funcion para marcar como finalizado el prestamo
    def finalizarPrestamo(self):
        self.query = QSqlQuery()
        success = self.query.exec_("DELETE FROM Loan WHERE carnet='" + str(self.currentStudent) + "';")

        if(success):
            i = 0
            # Actualizamos la cantidad prestada de cada libro
            while(i != self.tabla_libros_prestamos.rowCount()):
                if(self.tabla_libros_prestamos.item(i, 0).text() != ""):
                    self.query.exec_("UPDATE Book SET quantity_lent = quantity_lent - 1 WHERE book_id='" + str(self.tabla_libros_prestamos.item(i, 0).text()) + "';")
                    i += 1
                else:
                    break
        else:
            ErrorPrompt("Error", "No se pudo marcar el préstamo como finalizado")
            return
        InfoPrompt("Éxito", "Se marco el préstamo como finalizado!")

    
    # Funcion para eliminar libro de la tabla
    def eliminarLibro(self, row):
        self.Libros_prestamo[str(self.tabla_libros_prestamos.item(row, 1).text())] -= 1
        self.tabla_libros_prestamos.item(row, 0).setText("")
        self.tabla_libros_prestamos.item(row, 1).setText("")
        self.tabla_libros_prestamos.cellWidget(row, 2).setText("")
        self.tabla_libros_prestamos.cellWidget(row, 2).setEnabled(False)
    

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

    
    def renovarPrestamo(self):
        self.query = QSqlQuery()
        start_date = str(datetime.datetime.now())
        hours = start_date.split()

        i = 0
        while(i != self.tabla_libros_prestamos.rowCount()):
            if(self.tabla_libros_prestamos.item(i, 0).text() != ""):
                self.query.exec_("SELECT loan_duration FROM Book WHERE book_id = '" + self.tabla_libros_prestamos.item(i, 0).text() + "';")
                if(self.query.first()):
                    return_date = str(datetime.date.today() + datetime.timedelta(days=(self.query.value(0)))) + " " + str(hours[1])
                    print(return_date)
                    self.query.exec_("UPDATE Loan SET estimated_return_time = '" + return_date + "' WHERE book_id = '" + self.tabla_libros_prestamos.item(i, 0).text() + "';")
                    i += 1
                else:
                    ErrorPrompt("Error", "Ocurrio un error renovando el prestamo")
            else:
                break
        InfoPrompt("Éxito", "El prestamo se renovó con exito!")

