from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from Tables import InventarioBooksTable
import sys

class Inventario(QWidget):

	def __init__(self):
		# Inicialización de la ventana
		super().__init__()

		self.setWindowTitle("Inventario")
		self.setWindowIcon(QIcon("static/icono_CEIC.png"))
		self.setStyleSheet('background-color: rgb(236, 240, 241)')

		# Base de datos
		self.db = QSqlDatabase.database('qt_sql_default_connection')
		self.db.setHostName("localhost")
		self.db.setDatabaseName("pruebaceic")
		self.db.setUserName("postgres")
		self.db.setPassword("postgres")
		self.db.open()

		# Creación de fonts para las letras
		self.titleFont = QFont("Serif", 20)
		self.titleFont.setBold(True)

		# Título
		self.title = QLabel(self)
		self.title.setText("Inventario")
		self.title.setStyleSheet('color: rgb(30, 39, 46)')
		self.title.setFont(self.titleFont)
		self.title.setGeometry(10, 15, 570, 50)

		# Línea debajo del título
		self.line = QtWidgets.QFrame(self)
		self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setObjectName("line")

		# Tabla donde aparecerán los datos
		self.table = InventarioBooksTable() # Tablas
		self.tableLayout = QHBoxLayout()
		self.tableLayout.addWidget(self.table)
		self.setLayout(self.tableLayout)

		self.llenarTabla()

	def llenarTabla(self):
		row = 0
		sql = "SELECT book_id, title FROM Book ORDER BY title"
		queryx = QSqlQuery(sql)
		while queryx.next():
		    self.table.insertRow(row)
		    IDX = QTableWidgetItem(str(queryx.value(0)))
		    titulox = QTableWidgetItem(str(queryx.value(1)))
		    self.table.setItem(row, 0, IDX)
		    self.table.setItem(row, 1, titulox)
		    row = row + 1

		self.table.setRowCount(row)
		self.table.setTableColors()
		header = self.table.horizontalHeader()       
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
