from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
import sys

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

        # Título
        self.title = QLabel("Prestamos", self)
        self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)
        self.title.move(30, 10)

        # Frame del form
        frame_form_prestamo = QFrame(self)
        frame_form_prestamo.setFrameShape(QFrame.StyledPanel)
        frame_form_prestamo.setFixedWidth(300)
        frame_form_prestamo.setFixedHeight(370)
        frame_form_prestamo.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: white;\n"
        "}")
        frame_form_prestamo.move(30, 60)

        # Carnet de estudiante #carnet del estudiante
        self.currentStudent = "" #GUarda el valor del carnet del estudiante actualmente mostrado en pantalla
        self.carnetLabel = QLabel("Número de carnet: ", frame_form_prestamo)
        self.carnetLabel.move(10, 10)
        self.carnet = QLineEdit(frame_form_prestamo)
        self.carnet.setStyleSheet('background-color: white')
        self.carnet.move(10, 30)