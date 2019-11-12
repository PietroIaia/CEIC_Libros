from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from Tables import Books_Loan_Table, Active_Loan_Table
from validationFunctions import checkPattern, checkCarnet, checkTitle
import sys


# NOTAS:
# - Entre Labels dentro del frame "Informacion de prestamo" hay 30px de espacio

class prestamos(QWidget):

    def __init__(self):

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

        # Realizar prestamo
        self.button_realizar = QPushButton("Realizar Préstamo", self.frame_form_prestamo)
        self.button_realizar.setFixedWidth(220)
        self.button_realizar.setFixedHeight(28)
        self.button_realizar.move(27, 390)
        self.button_realizar.setFont(self.btnFont)
        self.button_realizar.setStyleSheet("QPushButton\n{\n border: 1px solid #C9C9C9;\n background-color: PowderBlue;\n}"
        "QPushButton:hover\n{\n background-color: #93BABF;\n}")
        self.button_realizar.setEnabled(False)

        # Tabla de prestamos
        self.Libros_prestamo = {}         # Para saber los libros que se van a prestar
        self.tabla_libros_prestamos = Books_Loan_Table(self)
        self.tabla_libros_prestamos.move(305, 60)

        # Tabla de prestamos activos
        # NOTA: Para agregar nuevas filas, usamos table.insertRow(rowPosition) donde rowposition es donde la queremos poner (de ultima)
        # https://stackoverflow.com/questions/24044421/how-to-add-a-row-in-a-tablewidget-pyqt
        self.active_loan_table = Active_Loan_Table(self)
        self.active_loan_table.move(30, 500)

        # Conexiones
        self.carnet.returnPressed.connect(lambda: self.buscarEstudiante(self.carnet.text()))
        self.button_agregar_libro.clicked.connect(lambda: self.buscarLibro(self.libro.text()))


    def buscarEstudiante(self, carnetBuscado):

        if(checkCarnet(carnetBuscado)):
            queryText = "SELECT * FROM Estudiante WHERE carnet = '" + carnetBuscado + "';"
            self.query = QSqlQuery()
            self.query.exec_(queryText)

            if self.query.first():
                self.Libros_prestamo.clear()
                self.nombre.setText(str(self.query.value(1)))
                self.apellido.setText(str(self.query.value(2)))
                self.deuda.setText(str(self.query.value(8)))

                queryText ="SELECT * FROM Loan WHERE carnet = '" + carnetBuscado + "';"
                self.query.exec_(queryText)
                if self.query.first():
                    self.prestamo.setText("Prestamo activo")

                    # Si le queda menos de 1 dia para regresar el libro, permitimos la renovacion
                    if(self.calculateTimeLeft(QDateTime.currentDateTime(), self.query.value(6)) < 2):
                        self.button_renovar.setEnabled(True)

                    # Mostramos los libros que se le prestaron
                    queryText ="SELECT title FROM Book WHERE book_id = '" + self.query.value(1) + "';"
                    self.query2 = QSqlQuery()
                    self.query2.exec_(queryText)
                    i = 0
                    while(True):
                        self.tabla_libros_prestamos.item(i, 0).setText(str(self.query.value(1)))
                        self.tabla_libros_prestamos.item(i, 1).setText(str(self.query2.value(0)))
                        i += 1
                        if(not self.query2.next()):
                            break

                else:
                    self.prestamo.setText("No prestamo activo")

                    self.libro.setEnabled(True)
                    self.button_agregar_libro.setEnabled(True)

            else:
                ErrorPrompt("Error", "No se encontró un Estudiante con ese carnet")
    

    # Funcion para buscar el libro e ingresarlo a la tabla de libros Prestamos cuando se este realizando un prestamo
    def buscarLibro(self, Libro):

        if(checkTitle(Libro)):
            queryText = "SELECT * FROM Book WHERE title = '" + Libro + "';"
            self.query = QSqlQuery()
            self.query.exec_(queryText)
            i = 0
            if(self.query.first()):
                self.button_realizar.setEnabled(True)
                while(self.tabla_libros_prestamos.item(i, 0).text() != ""):
                    i += 1

                # Si el libro esta en el diccionario y hay menos ejemplares que el total disponible de ese libro, se le permite agregarlo al prestamo
                if(str(Libro) in self.Libros_prestamo.keys() and self.Libros_prestamo[str(Libro)] < (self.query.value(4) - self.query.value(5))):
                    self.Libros_prestamo[str(Libro)] += 1
                    self.tabla_libros_prestamos.item(i, 0).setText(str(self.query.value(0)))
                    self.tabla_libros_prestamos.item(i, 1).setText(str(Libro))
                # Si el libro no esta en el diccionario, se agrega
                elif(str(Libro) not in self.Libros_prestamo.keys()):
                    self.Libros_prestamo[str(Libro)] = 0
                    # Si se estan prestando menos ejemplares que el total disponible de ese libro, se le permite agregarlo al prestamo
                    if(self.Libros_prestamo[str(Libro)] < (self.query.value(4) - self.query.value(5))):
                        self.Libros_prestamo[str(Libro)] = 1
                        self.tabla_libros_prestamos.item(i, 0).setText(str(self.query.value(0)))
                        self.tabla_libros_prestamos.item(i, 1).setText(str(Libro))
                else:
                    ErrorPrompt("Error", "No existen mas ejemplares disponibles de este libro")
            else:
                ErrorPrompt("Error", "No se encontró el Libro especificado")


    # Funcion para calcular el tiempo restante de el prestamo
    def calculateTimeLeft(start_time, return_time):
        startTimeAux = QDateTime.toSecsSinceEpoch(start_time)
        returnTimeAux = QDateTime.toSecsSinceEpoch(return_time)

        aux = (int(returnTimeAux) - int(startTimeAux))/86400
        return aux




if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = prestamos()
    form.show()
    sys.exit(app.exec_())