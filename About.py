from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class About(QWidget):

	def __init__(self):

		# Inicialización de la ventana
		super().__init__()
		self.setGeometry(200, 0, 600, 600)
		self.setWindowTitle("About")
		self.setStyleSheet('background-color: rgb(236, 240, 241)')

		# Frame para la información de about
		self.frame_about = QFrame(self)
		self.frame_about.setGeometry(QtCore.QRect(100, 110, 650, 540))
		self.frame_about.setStyleSheet("background-color: white; border-radius: 10px;")

		# Ícono de about en el frame
		self.icon_about = QPushButton(self)
		self.icon_about.setGeometry(375, 60, 100, 100)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("static/about-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.icon_about.setIcon(icon)
		self.icon_about.setIconSize(QtCore.QSize(80, 80))
		self.icon_about.setFlat(True)
		self.icon_about.setStyleSheet("background-color: white; border-radius: 50px;")

		# Font para las letras
		self.titleFont = QFont("Serif", 20)
		self.titleFont.setBold(True)
		self.button_font = QFont("Helvetica", 12)
		self.button_font.setBold(True)
		self.text_font = QFont("Helvetica", 14)

		# Título de about
		self.title = QtWidgets.QLabel(self)
		self.title.setText("About")
		self.title.setStyleSheet('color: #CAD3C8; background-color: rgba(0, 0, 0, 0);')
		self.title.setFont(self.titleFont)
		self.title.setGeometry(385, 150, 100, 50)

		# Línea debajo del título
		self.line = QtWidgets.QFrame(self)
		self.line.setGeometry(QtCore.QRect(100, 200, 650, 5))
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setStyleSheet('border: 40px solid rgb(236, 240, 241)')

		# Botón de política de préstamos
		self.politica_prestamos = QPushButton(self)
		self.politica_prestamos.setGeometry(305, 580, 250, 40)
		self.politica_prestamos.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.politica_prestamos.setFont(self.button_font)
		self.politica_prestamos.setText("Política de Préstamo")
		self.politica_prestamos.setStyleSheet("QPushButton:hover\n"
											  "{\n"
											  "		background-color: #2790b4;"
											  "}\n"
											  "QPushButton:pressed\n"
											  "{\n"
											  "		background-color: #319bbe;"
											  "}\n"
											  "QPushButton\n"
											  "{\n"
											  "		color: white;"
											  "		border-radius: 20px;"
											  "		background-color: qlineargradient(spread:pad, x1:0, \
											   		y1:0, x2:1, y2:0, stop:0 rgba(39, 144, 180, 255), stop:1 rgba(26, 22, 102, 255));"
											  "}")

		# Label donde se muestra el texto con la información del sistema
		self.about_text = QLabel(self)
		self.about_text.setGeometry(140, 220, 570, 320)
		self.about_text.setFont(self.text_font)
		self.about_text.setStyleSheet("background-color: white; color: #576574;")
		self.about_text.setWordWrap(True)
		self.about_text.setAlignment(Qt.AlignHCenter)
		self.about_text.setText("La aplicación CEIC Libros es un proyecto pensado por el Centro de Estudiantes de "
								"Ingeniería de la Computación, de la Universidad Simón Bolívar, para darle a "
								"los estudiantes de la carrera, la posibilidad de acceder a los libros de las "
								"materias que puedan estar cursando durante el trimestre. \n"
								"A través de esta aplicación el CEIC podrá administrar el inventario de su biblioteca, "
								"así como también los préstamos que estén en curso o que se hayan realizado en el pasado, "
								"llevando un control de los estudiantes que han utilizado o utilizan el sistema de préstamos "
								"de libros del CEIC. \n"
								"Esta aplicación ha sido desarrollada por los estudiantes\n"
								"Cristopher Bolívar, Pablo González, Pietro Iaia, Diego Peña y Daniela Zorrilla.")

