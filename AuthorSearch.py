from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Tables import AuthorSearchTable
import sys

class AuthorSearch(QWidget):

    def __init__(self):

        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaCEIC")                         
        self.db.setUserName("postgres")
        self.db.setPassword("Tranc0nReloj-7aha")                               # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
        self.db.open()

        # Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 100, 600, 600)
        self.setWindowTitle("Búsqueda por autor")
        self.setStyleSheet('background-color: rgb(236, 240, 241)')

        # Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.titleFont.setBold(True)
        self.labelFont = QFont("Helvetica", 13)
        self.labelFont.setBold(True)
        self.buttonFont = QFont("Arial", 12)
        self.buttonFont.setBold(True)

        # Título
        self.title = QtWidgets.QLabel(self)
        self.title.setText("Búsqueda por autor")
        self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 300, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Instrucciones
        self.instrucciones = QtWidgets.QLabel(self)
        self.instrucciones.setText("Seleccione el autor cuyos libros desea conocer")
        self.instrucciones.setStyleSheet('color: rgb(109, 120, 124)')
        self.instrucciones.setFont(self.labelFont)
        self.instrucciones.setGeometry(230, 85, 400, 20)

        # Línea debajo de las instrucciones
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(230, 100, 370, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.instrucciones.raise_()

        # Tabla para los libros de los autores
        self.table = AuthorSearchTable()

        # Label de autor
        self.authorLabel = QtWidgets.QLabel(self)
        self.authorLabel.setText("Autor")
        self.authorLabel.setFont(self.labelFont)
        self.authorLabel.setStyleSheet('color: rgb(79, 90, 94)')
        self.authorLabel.setGeometry(100, 630, 100, 30)

        # QComboBox para los autores
        self.authorList = QComboBox(self)
        self.setAuthorList()
        self.authorList.setStyleSheet('background-color: white; border: 1px solid rgb(210, 218, 226); border-radius: 10px;')
        self.authorList.setGeometry(155, 630, 590, 30)

        # Botón de consulta
        self.search = QPushButton(self)
        self.search.setText("Consultar")
        self.search.setFont(self.buttonFont)
        self.search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search.setGeometry(155, 670, 590, 30)
        self.search.setStyleSheet("QPushButton:hover\n"
                                  "{\n"
                                  "    background-color: rgb(55, 162, 228);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed\n"
                                  "{\n"
                                  "    background-color: rgb(35, 142, 208);\n"
                                  "}\n"
                                  "QPushButton\n"
                                  "{\n"
                                  "    border-radius: 15px;\n"
                                  "    background-color: rgb(45, 152, 218);\n"
                                  "    color: white;\n"
                                  "}")

        # Botón para regresar a la pestaña de gestión de libros
        self.back = QPushButton(self)
        self.back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.back.setGeometry(780, 665, 40, 40)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("static/go-back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon)
        self.back.setIconSize(QtCore.QSize(40, 40))
        self.back.setFlat(True)
        self.back.setStyleSheet("QPushButton:hover\n"
                                "{\n"
                                "    background-color: rgb(210, 210, 210);\n"
                                "}\n"
                                "\n"
                                "QPushButton:pressed\n"
                                "{\n"
                                "    background-color: rgb(200, 200, 200);\n"
                                "}\n"
                                "QPushButton\n"
                                "{\n"
                                "    border-radius: 20px;\n"
                                "}")

        # Layout final
        self.textLayout = QHBoxLayout()
        self.textLayout.addWidget(self.table)
        self.setLayout(self.textLayout)

        # Conexión del botón de consulta
        self.search.clicked.connect(self.consulta)

    # Busca los autores registrados en la base de datos y los despliega en el menú
    def setAuthorList(self):
        self.query = QSqlQuery()
        self.query.exec_("SELECT * FROM Author ORDER BY last_name ASC;")
        index = 0
        while self.query.next():
            if self.query.value(0) == "NA":
                name = self.query.value(1)
            else:
                name = self.query.value(1) + ", " + self.query.value(0)
            self.authorList.insertItem(index, name)
            index += 1
        
        self.authorList.insertItem(index, "")
        self.authorList.setCurrentIndex(index)

    @pyqtSlot()
    def consulta(self):
        self.table.clearTable()
        names = self.authorList.currentText().split(", ")
        queryText = "SELECT b.title, b.book_id, b.quantity, b.quantity_lent, b.loan_duration \
                     FROM Book as b\
                     JOIN WrittenBy as w ON w.book_id = b.book_id\
                     WHERE w.author_id = (SELECT author_id\
                                          FROM Author\
                                          WHERE last_name = \'" + names[0] + "\'"
        if (len(names) > 1):
            queryText += "AND first_name = \'" + names[1] + "\')"
        else:
            queryText += ")"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        i = 0
        while self.query.next():
            for j in range(4):
                if j < 2:
                    self.table.item(i, j).setText(str(self.query.value(j)))
                elif j == 2:
                    remain = str(int(self.query.value(2)) - int(self.query.value(3)))
                    self.table.item(i, j).setText(remain)
                else:
                    self.table.item(i, j).setText(str(self.query.value(4))) 
                
            i += 1