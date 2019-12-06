from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

#import psycopg2

class Politica(QWidget):

	def __init__(self):

		# Inicialización de la ventana
		super().__init__()
		self.setGeometry(200, 0, 600, 600)
		self.setWindowTitle("Política de Préstamo")
		self.setStyleSheet('background-color: rgb(236, 240, 241)')

		# Base de datos
		#self.con = psycopg2.connect("dbname=pruebaceic user=postgres host=localhost password=12345 port=5433")
		#self.cur = self.con.cursor()
		self.db = QSqlDatabase.database('qt_sql_default_connection')
		self.db.setHostName("localhost")
		self.db.setDatabaseName("pruebaCEIC")
		self.db.setUserName("postgres")
		self.db.setPassword("Tranc0nReloj-7aha")
		self.db.open()

		# Frame para la información de la política de préstamo
		self.frame_politica = QFrame(self)
		self.frame_politica.setGeometry(QtCore.QRect(70, 70, 700, 610))
		self.frame_politica.setStyleSheet("background-color: white; border-radius: 10px;")

		# Font para las letras
		self.titleFont = QFont("Serif", 20)
		self.titleFont.setBold(True)
		self.button_font = QFont("Helvetica", 12)
		self.button_font.setBold(True)
		self.text_font = QFont("Helvetica", 10)
		self.subtitle_font = QFont("Serif", 13)
		self.subtitle_font.setBold(True)

		# Título
		self.title = QtWidgets.QLabel(self)
		self.title.setText("Política de Préstamo")
		self.title.setStyleSheet('color: #2d3436; background-color: rgba(0, 0, 0, 0);')
		self.title.setFont(self.titleFont)
		self.title.setGeometry(280, 100, 300, 30)

		# Línea debajo del título
		self.line = QtWidgets.QFrame(self)
		self.line.setGeometry(QtCore.QRect(190, 140, 450, 5))
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setStyleSheet('border: 40px solid rgb(236, 240, 241)')

		# Frame para la regla sobre préstamos
		self.frame_prestamos = QFrame(self)
		self.frame_prestamos.setGeometry(110, 180, 620, 120)
		self.frame_prestamos.setStyleSheet("background-color: #f5f6fa; border-radius: 10px; border: 1px solid #CAD3C8;")

		# Frame para la regla sobre multas
		self.frame_multas = QFrame(self)
		self.frame_multas.setGeometry(110, 320, 620, 120)
		self.frame_multas.setStyleSheet("background-color: #f5f6fa; border-radius: 10px; border: 1px solid #CAD3C8;")

		# Frame para la regla sobre sanciones
		self.frame_sanciones = QFrame(self)
		self.frame_sanciones.setGeometry(110, 460, 620, 120)
		self.frame_sanciones.setStyleSheet("background-color: #f5f6fa; border-radius: 10px; border: 1px solid #CAD3C8;")

		# Íconos para la regla de préstamos
		self.icon_prestamos = QPushButton(self)
		self.icon_prestamos.setGeometry(120, 190, 100, 100)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("static/préstamos-2790b4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.icon_prestamos.setIcon(icon)
		self.icon_prestamos.setIconSize(QtCore.QSize(80, 80))
		self.icon_prestamos.setFlat(True)
		self.icon_prestamos.setStyleSheet("background-color: rgba(0,0,0,0)")

		# Íconos para la regla de multas
		self.icon_multas = QPushButton(self)
		self.icon_multas.setGeometry(120, 330, 100, 100)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("static/fines-2790b4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.icon_multas.setIcon(icon)
		self.icon_multas.setIconSize(QtCore.QSize(90, 90))
		self.icon_multas.setFlat(True)
		self.icon_multas.setStyleSheet("background-color: rgba(0,0,0,0)")

		# Íconos para la regla de sanciones
		self.icon_sanciones = QPushButton(self)
		self.icon_sanciones.setGeometry(120, 470, 100, 100)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("static/banned-2790b4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.icon_sanciones.setIcon(icon)
		self.icon_sanciones.setIconSize(QtCore.QSize(90, 90))
		self.icon_sanciones.setFlat(True)
		self.icon_sanciones.setStyleSheet("background-color: rgba(0,0,0,0)")

		# Subtítulo para la regla de préstamos
		self.title_prestamos = QLabel(self)
		self.title_prestamos.setGeometry(230, 190, 200, 20)
		self.title_prestamos.setFont(self.subtitle_font)
		self.title_prestamos.setAutoFillBackground(True)
		self.title_prestamos.setStyleSheet("color: #2d3436; background-color: rgba(0,0,0,0);")
		self.title_prestamos.setText("Préstamos")

		# Subtítulo para la regla de multas
		self.title_multas = QLabel(self)
		self.title_multas.setGeometry(230, 330, 200, 20)
		self.title_multas.setFont(self.subtitle_font)
		self.title_multas.setAutoFillBackground(True)
		self.title_multas.setStyleSheet("color: #2d3436; background-color: rgba(0,0,0,0);")
		self.title_multas.setText("Multas")

		# Subtítulo para la regla de sanciones
		self.title_sanciones = QLabel(self)
		self.title_sanciones.setGeometry(230, 470, 200, 20)
		self.title_sanciones.setFont(self.subtitle_font)
		self.title_sanciones.setAutoFillBackground(True)
		self.title_sanciones.setStyleSheet("color: #2d3436; background-color: rgba(0,0,0,0);")
		self.title_sanciones.setText("Sanciones")

		# Label para la regla de préstamos
		self.rule_prestamos = QLabel(self)
		self.rule_prestamos.setGeometry(230, 210, 490, 80)
		self.rule_prestamos.setStyleSheet("background-color: rgba(0,0,0,0)")
		self.rule_prestamos.setWordWrap(True)
		self.rule_prestamos.setFont(self.text_font)
		self.rule_prestamos.setAlignment(Qt.AlignLeft)

		# Label para la regla de multas
		self.rule_multas = QLabel(self)
		self.rule_multas.setGeometry(230, 350, 490, 80)
		self.rule_multas.setStyleSheet("background-color: rgba(0,0,0,0)")
		self.rule_multas.setWordWrap(True)
		self.rule_multas.setFont(self.text_font)
		self.rule_multas.setAlignment(Qt.AlignLeft)

		# Label para la regla de sanciones
		self.rule_sanciones = QLabel(self)
		self.rule_sanciones.setGeometry(230, 490, 490, 80)
		self.rule_sanciones.setStyleSheet("background-color: rgba(0,0,0,0)")
		self.rule_sanciones.setWordWrap(True)
		self.rule_sanciones.setFont(self.text_font)
		self.rule_sanciones.setAlignment(Qt.AlignLeft)

		# Colocamos las reglas almacenadas en la base de datos en los labels
		self.mostrar_politica()

		# Botón para modificar la política de préstamos
		self.modificar = QPushButton(self)
		self.modificar.setGeometry(110, 615, 300, 40)
		self.modificar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.modificar.setFont(self.button_font)
		self.modificar.setText("Modificar")
		self.modificar.setStyleSheet("QPushButton:hover\n"
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

		# Botón para cerrar la política de préstamos
		self.entendido = QPushButton(self)
		self.entendido.setGeometry(430, 615, 300, 40)
		self.entendido.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.entendido.setFont(self.button_font)
		self.entendido.setText("Entendido")
		self.entendido.setStyleSheet("QPushButton:hover\n"
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

		# Botón para guardar las modificaciones
		self.guardar = QPushButton(self)
		self.guardar.setGeometry(430, 615, 300, 40)
		self.guardar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.guardar.setFont(self.button_font)
		self.guardar.setText("Guardar")
		self.guardar.setStyleSheet("QPushButton:hover\n"
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
									 "		background-color: #1d87aa;"
									 "}")

		# Botón para cancelar las modificaciones
		self.cancelar = QPushButton(self)
		self.cancelar.setGeometry(110, 615, 300, 40)
		self.cancelar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.cancelar.setFont(self.button_font)
		self.cancelar.setText("Cancelar")
		self.cancelar.setStyleSheet("QPushButton:hover\n"
									 "{\n"
									 "		background-color: #C20000;"
									 "}\n"
									 "QPushButton:pressed\n"
									 "{\n"
									 "		background-color: #CC0000;"
									 "}\n"
									 "QPushButton\n"
									 "{\n"
									 "		color: white;"
									 "		border-radius: 20px;"
									 "		background-color: #F10000;"
									 "}")

		# Line edits para modificar las reglas de la política de préstamo
		self.modificar_prestamos = QTextEdit(self)
		self.modificar_prestamos.setGeometry(220, 180, 510, 120)
		self.modificar_prestamos.setStyleSheet("background-color: white; border: 1px solid #CAD3C8;")
		self.modificar_prestamos.setFont(self.text_font)
		self.modificar_prestamos.setText(self.prestamos_text)

		self.modificar_multas = QTextEdit(self)
		self.modificar_multas.setGeometry(220, 320, 510, 120)
		self.modificar_multas.setStyleSheet("background-color: white; border: 1px solid #CAD3C8;")
		self.modificar_multas.setFont(self.text_font)
		self.modificar_multas.setText(self.multas_text)

		self.modificar_sanciones = QTextEdit(self)
		self.modificar_sanciones.setGeometry(220, 460, 510, 120)
		self.modificar_sanciones.setStyleSheet("background-color: white; border: 1px solid #CAD3C8;")
		self.modificar_sanciones.setFont(self.text_font)
		self.modificar_sanciones.setText(self.sanciones_text)

		# Escondemos los line edits
		self.modificar_prestamos.hide()
		self.modificar_multas.hide()
		self.modificar_sanciones.hide()
		self.guardar.hide()
		self.cancelar.hide()

		# Conexiones de los botones
		self.modificar.clicked.connect(self.modificar_politica)
		self.guardar.clicked.connect(self.guardar_politica)
		self.cancelar.clicked.connect(self.cancelar_modificacion)

	def modificar_politica(self):
		self.modificar_prestamos.show()
		self.modificar_multas.show()
		self.modificar_sanciones.show()
		self.guardar.show()
		self.cancelar.show()

	def guardar_politica(self):
		update_prestamos_text = self.modificar_prestamos.toPlainText()
		update_multas_text = self.modificar_multas.toPlainText()
		update_sanciones_text = self.modificar_sanciones.toPlainText()

		query_text = "UPDATE Politica_prestamo SET prestamos = '" + str(update_prestamos_text) + \
					 "', multas = '" + str(update_multas_text) + "', sanciones = '" + str(update_sanciones_text) + \
					 "' WHERE id_ = 1;"
		try:
			########################################
			#self.cur.execute(query_text)
			#elf.con.commit()
			self.query = QSqlQuery()
			self.query.exec_(query_text)
			self.query.first()
			########################################

			self.prestamos_text = update_prestamos_text
			self.multas_text = update_multas_text
			self.sanciones_text = update_sanciones_text

			self.rule_prestamos.setText(self.prestamos_text)
			self.rule_multas.setText(self.multas_text)
			self.rule_sanciones.setText(self.sanciones_text)

			self.modificar_prestamos.setText(self.prestamos_text)
			self.modificar_multas.setText(self.multas_text)
			self.modificar_sanciones.setText(self.sanciones_text)

			self.modificar_prestamos.hide()
			self.modificar_multas.hide()
			self.modificar_sanciones.hide()
			self.guardar.hide()
			self.cancelar.hide()
		
		except:
			self.modificar_prestamos.setText(self.prestamos_text)
			self.modificar_multas.setText(self.multas_text)
			self.modificar_sanciones.setText(self.sanciones_text)
			self.modificar_prestamos.hide()
			self.modificar_multas.hide()
			self.modificar_sanciones.hide()
			self.guardar.hide()
			self.cancelar.hide()

	def cancelar_modificacion(self):
		self.modificar_prestamos.setText(self.prestamos_text)
		self.modificar_multas.setText(self.multas_text)
		self.modificar_sanciones.setText(self.sanciones_text)
		self.modificar_prestamos.hide()
		self.modificar_multas.hide()
		self.modificar_sanciones.hide()
		self.guardar.hide()
		self.cancelar.hide()

	def mostrar_politica(self):
		# Obtenemos la regla para los préstamos
		query_text_prestamos = "SELECT prestamos FROM Politica_prestamo"
		#############################################
		#self.cur.execute(query_text_prestamos)
		#prestamos_result = self.cur.fetchall()
		#prestamos_result = prestamos_result[0][0]
		self.query = QSqlQuery()
		self.query.exec_(query_text_prestamos)
		self.query.first()
		prestamos_result = self.query.value(0)
		#############################################

		# Obtenemos la regla para las multas
		query_text_multas = "SELECT multas FROM Politica_prestamo"
		#############################################
		#self.cur.execute(query_text_multas)
		#multas_result = self.cur.fetchall()
		#multas_result = multas_result[0][0]
		self.query = QSqlQuery()
		self.query.exec_(query_text_multas)
		self.query.first()
		multas_result = self.query.value(0)
		#############################################

		# Obtenemos la regla para las sanciones
		query_text_sanciones = "SELECT sanciones FROM Politica_prestamo"
		#############################################
		#self.cur.execute(query_text_sanciones)
		#sanciones_result = self.cur.fetchall()
		#sanciones_result = sanciones_result[0][0]
		self.query = QSqlQuery()
		self.query.exec_(query_text_sanciones)
		self.query.first()
		sanciones_result = self.query.value(0)
		#############################################

		# Mostramos las reglas en pantalla
		self.prestamos_text = prestamos_result
		self.multas_text = multas_result
		self.sanciones_text = sanciones_result

		self.rule_prestamos.setText(self.prestamos_text)
		self.rule_multas.setText(self.multas_text)
		self.rule_sanciones.setText(self.sanciones_text)

