from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
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

        # Título
        self.title = QLabel("Prestamos", self)
        self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)
        self.title.move(30, 10)

        # Frame del form
        self.frame_form_prestamo = QFrame(self)
        self.frame_form_prestamo.setFrameShape(QFrame.StyledPanel)
        self.frame_form_prestamo.setFixedWidth(275)
        self.frame_form_prestamo.setFixedHeight(370)
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
        self.nombre.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
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
        self.apellido.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.apellido.setFixedWidth(150)
        self.apellido.setFixedHeight(25)
        self.apellido.setTextMargins(5, 0, 0, 0)
        self.apellido.move(85, 145)

        # Prestamo activo de estudiante
        self.prestamoLabel = QLabel("Prestamo ", self.frame_form_prestamo)
        self.prestamoLabel.move(10, 177)
        self.prestamoLabel.setFont(self.subFont)
        self.prestamo = QLineEdit(self.frame_form_prestamo)
        self.prestamo.setReadOnly(True)
        self.prestamo.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.prestamo.setFixedWidth(150)
        self.prestamo.setFixedHeight(25)
        self.prestamo.setTextMargins(5, 0, 0, 0)
        self.prestamo.move(85, 175)

        # Deuda de estudiante
        self.deudaLabel = QLabel("Deuda ", self.frame_form_prestamo)
        self.deudaLabel.move(10, 205)
        self.deudaLabel.setFont(self.subFont)
        self.deuda = QLineEdit(self.frame_form_prestamo)
        self.deuda.setReadOnly(True)
        self.deuda.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.deuda.setFixedWidth(150)
        self.deuda.setFixedHeight(25)
        self.deuda.setTextMargins(5, 0, 0, 0)
        self.deuda.move(85, 205)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = prestamos()
    form.show()
    sys.exit(app.exec_())