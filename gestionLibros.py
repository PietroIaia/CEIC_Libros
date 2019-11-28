#CEIC Libros
#Tabla de Libros
#Desarrollado por Forward
#Responsable del módulo: Pietro Iaia, 15-10718
#Fecha de inicio: 23-10-19
#Última modifcación: 23-10-19

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from Tables import BooksTable, InventarioBooksTable
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from validationFunctions import verification_books
from AgregarLibro import AgregarLibro
from verificarAutor import verificarAutor                              # Falta crear agregarLibro.py
from AuthorSearch import AuthorSearch
import sys
import re

class gestionLibros(QWidget):

    def __init__(self, perm_mask):

        # Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de Libros")
        self.setStyleSheet('background-color: rgb(236, 240, 241)')

        # Regex del Titulo
        self.libroPattern = re.compile(r"[a-zA-Z]")

        # Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.titleFont.setBold(True)
        self.instFont = QFont("Serif", 12)
        self.buttonFont = QFont("Arial", 11)
        self.buttonFont.setBold(True)

        # Título
        self.title = QtWidgets.QLabel(self)
        self.title.setText("Gestión de Libros")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 250, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Tabla donde aparecerán los datos
        self.table = BooksTable() #Tablas

        # Botones de agregar, modificar, cancelar y confirmar (Acciones)
        self.author = QPushButton(self)
        self.modificar = QPushButton(self)
        self.eliminar = QPushButton(self)
        self.guardar = QPushButton(self)
        self.cancel = QPushButton(self)
        self.confirm = QPushButton(self)
        self.deleteCancel = QPushButton(self)
        
        # Se esconden los botones
        self.confirm.hide()
        self.deleteCancel.hide()
        self.guardar.hide()
        self.cancel.hide()

        # Ícono para el botón modificar
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("static/edit-book-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modificar.setIcon(icon1)
        self.modificar.setIconSize(QtCore.QSize(30, 30))
        self.modificar.setFlat(True)

        # Ícono para el botón eliminar
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("static/delete-book-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eliminar.setIcon(icon2)
        self.eliminar.setIconSize(QtCore.QSize(28, 28))
        self.eliminar.setFlat(True)

        # Texto de los botones
        self.modificar.setText("     Modificar")
        self.guardar.setText("Guardar")
        self.cancel.setText("Cancelar")
        self.eliminar.setText("       Eliminar")
        self.confirm.setText("Confirmar")
        self.deleteCancel.setText("Cancelar")
        self.author.setText("Buscar por autor")

        # CSS de los botones
        self.set_button_style_sheet("modificar", "#2D98DA", "#238ED0", "#C8C8C8", "17px")
        self.set_button_style_sheet("cancel", "#55c1ff", "#41acee", "#4bb6f8", "15px")
        self.set_button_style_sheet("guardar", "#55c1ff", "#41acee", "#4bb6f8", "15px")
        self.set_button_style_sheet("eliminar", "#C20000", "#CC0000", "#C8C8C8", "17px")
        self.set_button_style_sheet("confirm", "#b80000", "#CC0000", "#D60000", "15px")
        self.set_button_style_sheet("deleteCancel", "#b80000", "#CC0000", "#D60000", "15px")
        self.set_button_style_sheet("author", "#162e6b", "#021a57", "#0c2461", "15px")

        # Cursor para los botones
        self.modificar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.guardar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.eliminar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.author.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteCancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Posición para los botones
        self.modificar.setGeometry(657, 150, 180, 35)
        self.guardar.setGeometry(657, 535, 180, 30)
        self.cancel.setGeometry(657, 570, 180, 30)
        self.eliminar.setGeometry(657, 190, 180, 35)
        self.confirm.setGeometry(657, 535, 180, 30)
        self.deleteCancel.setGeometry(657, 570, 180, 30)
        self.author.setGeometry(657, 680, 180, 30)

        # Font de los botones
        self.modificar.setFont(self.buttonFont)
        self.cancel.setFont(self.buttonFont)
        self.guardar.setFont(self.buttonFont)
        self.eliminar.setFont(self.buttonFont)
        self.author.setFont(self.buttonFont)
        self.confirm.setFont(self.buttonFont)
        self.deleteCancel.setFont(self.buttonFont)
        
        # Configuración del layout
        self.actionsLayout = QVBoxLayout()
        self.actionsLayout.addStretch()
        self.widget = QWidget()
        self.actionsLayout.addWidget(self.widget)
        self.actionsLayout.addStretch()

        # Desactivar botones
        self.modificar.setEnabled(False)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.confirm.setEnabled(False)
        self.deleteCancel.setEnabled(False)

        # Ponemos la tabla y los botones en un mismo LAyout
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.table)
        self.tableLayout.addLayout(self.actionsLayout)
        self.setLayout(self.tableLayout)

        # Titulo del libro
        self.currentStudent = "" #Guarda el valor del titulo del libro actualmente mostrado en pantalla
        
        self.tituloLabel = QtWidgets.QLabel(self)
        self.tituloLabelFont = QFont("Arial", 12)
        self.tituloLabelFont.setBold(True)
        self.tituloLabel.setFont(self.tituloLabelFont)
        self.tituloLabel.setText("Título del libro ")
        self.tituloLabel.setStyleSheet('color: rgb(72, 84, 96)')
        self.tituloLabel.setGeometry(10, 645, 500, 30)

        # Edit para ingresar el título del libro
        self.titulo = QLineEdit(self)
        self.titulo.setStyleSheet('background-color: white; \n border-radius: 10px; border: 1px solid rgb(190, 198, 206); font: 12px;')
        self.titulo.setPlaceholderText(" Ingrese el título del libro a consultar, modificar o eliminar")
        self.titulo.setGeometry(125, 645, 525, 30)

        # Botón de consulta
        self.search = QPushButton(self)
        self.set_button_style_sheet("search", "#37A2E4", "#238ED0", "#2D98DA", "15px")
        self.search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search.setText("Consultar")
        self.search.setGeometry(125, 680, 525, 30)
        self.search.setFont(self.buttonFont)
        self.search.setEnabled(False)

        # Conexiones de los botones para cambiar colores
        self.modificar.clicked.connect(lambda: self.set_button_style_sheet("modificar", "#2D98DA", "#238ED0", "#2D98DA", "17px"))
        self.guardar.clicked.connect(lambda: self.set_button_style_sheet("modificar", "#2D98DA", "#238ED0", "#C8C8C8", "17px"))
        self.cancel.clicked.connect(lambda: self.set_button_style_sheet("modificar", "#2D98DA", "#238ED0", "#C8C8C8", "17px"))
        self.eliminar.clicked.connect(lambda: self.set_button_style_sheet("eliminar", "#C20000", "#CC0000", "#C20000", "17px"))
        self.confirm.clicked.connect(lambda: self.set_button_style_sheet("eliminar", "#C20000", "#CC0000", "#C8C8C8", "17px"))
        self.deleteCancel.clicked.connect(lambda: self.set_button_style_sheet("eliminar", "#C20000", "#CC0000", "#C8C8C8", "17px"))

        # Conexiones de los botones
        self.search.clicked.connect(self.consulta)
        self.modificar.clicked.connect(lambda: self.update(perm_mask))
        self.cancel.clicked.connect(self.cancelUpdate)
        self.guardar.clicked.connect(self.saveUpdate)
        self.eliminar.clicked.connect(self.deleteRequest)
        self.confirm.clicked.connect(self.confirmDelete)
        self.deleteCancel.clicked.connect(self.cancelDelete)
        self.titulo.textChanged[str].connect(self.check_disable)

        # Guarda la cantidad de copias que tiene el libro, si se llega a modificar, la usaremos para ver cuantas copias hay que agregar al sistema
        self.noCopy = 0

    # Función para cambiar el stylesheet de los botones
    def set_button_style_sheet(self, button_id, hover_color, pressed_color, bg_color, radius):
        button = getattr(self, '%s' %button_id)
        button.setStyleSheet("QPushButton:hover\n"
                "{\n"
                "    background-color: " + hover_color + ";\n"
                "}\n"
                "\n"
                "QPushButton:pressed\n"
                "{\n"
                "    background-color: " + pressed_color + ";\n"
                "}\n"
                "QPushButton\n"
                "{\n"
                "    background-color: " + bg_color + ";\n"
                "    border-radius: " + radius + ";\n"
                "    color: white;\n"
                "}")

    @pyqtSlot()
    def consulta(self):
        inputTitulo = self.titulo.text()

        if (self.libroPattern.match(inputTitulo) is None):
            ErrorPrompt("Error de formato", "Error: Ese no es el formato del título de un libro")
            return

        self.consultaAux(inputTitulo)

    def consultaAux(self, tituloBuscado):
        queryText = "SELECT * FROM Book WHERE title = '" + tituloBuscado + "';"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            self.currentBook = tituloBuscado
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
            for i in range(self.table.rowCount()):
                if(i == 4):
                    self.noCopy = int(self.query.value(i))
                self.table.item(i, 0).setText(str(self.query.value(i)))

            self.modificar.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("Error de búsqueda", "Error: Libro no encontrado")

    @pyqtSlot()
    def update(self, perm_mask):
        # Permito modificar la tabla
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
        self.table.item(0, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "ID"
        self.table.item(5, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Cantidad prestada"
        if(perm_mask == 0):
            self.table.item(6, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                     # No deja modificar la fila "Duracion de prestamo" si el usuario no es Admin
        self.search.setEnabled(False)
        self.author.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.modificar.setEnabled(False)
        self.guardar.setEnabled(True)
        self.cancel.setEnabled(True)
        self.guardar.show()
        self.cancel.show()
        InfoPrompt("Modificación activada", "Se ha activado el modo modificación")

    @pyqtSlot()
    def saveUpdate(self):
        fields = self.table.getFields()
        correct = verification_books(fields, 7)

        if not correct:
            return

        values = self.table.getValues()
        queryText = "UPDATE Book SET " + values + " WHERE book_id = '" + self.table.item(0, 0).text() + "' returning book_id"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            InfoPrompt("Actualización completada", "La información del libro ha sido actualizada exitosamente")
            self.search.setEnabled(True)
            self.author.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.modificar.setEnabled(True)
            self.guardar.setEnabled(False)
            self.cancel.setEnabled(False)
            self.guardar.hide()
            self.cancel.hide()
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("Error", "La información del libro no pudo ser modificada")
            self.author.setEnabled(True)
            self.guardar.hide()
            self.cancel.hide()

    @pyqtSlot()
    def cancelUpdate(self):
        InfoPrompt("Modificación cancelada", "Los cambios hechos no fueron guardados")
        self.consultaAux(self.currentBook)
        self.search.setEnabled(True)
        self.author.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.modificar.setEnabled(True)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.guardar.hide()
        self.cancel.hide()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot()
    def deleteRequest(self):
        ConfirmPrompt("Eliminación de Libro", "Se ha solicitado eliminar el libro. Marque botón de eliminación para confirmar")
        self.search.setEnabled(False)
        self.author.setEnabled(False)
        self.modificar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.confirm.setEnabled(True)
        self.deleteCancel.setEnabled(True)
        self.confirm.show()
        self.deleteCancel.show()

    @pyqtSlot()
    def confirmDelete(self):
        if (int(self.table.item(5, 0).text()) != 0):
            ErrorPrompt("Error en la eliminación", "Una copia del libro está siendo prestada a un estudiante, no se puede eliminar")
        else:
            queryText = "DELETE FROM Book_copy WHERE book_id = " + self.table.item(0, 0).text() + " RETURNING book_id"
            self.query = QSqlQuery()
            self.query.exec_(queryText)
            queryText = "DELETE FROM WrittenBy WHERE book_id = " + self.table.item(0, 0).text() + " RETURNING book_id"
            self.query = QSqlQuery()
            self.query.exec_(queryText)
            queryText = "DELETE FROM Book WHERE book_id = " + self.table.item(0, 0).text() + " RETURNING book_id"
            self.query = QSqlQuery()
            self.query.exec_(queryText)

            if self.query.first():
                InfoPrompt("Eliminación exitosa", "El libro ha sido eliminado del sistema")
                self.search.setEnabled(True)
                self.author.setEnabled(True)
                self.confirm.setEnabled(False)
                self.deleteCancel.setEnabled(False)
                self.confirm.hide()
                self.deleteCancel.hide()
                self.table.clear()
                self.titulo.setText("")
            else:
                ErrorPrompt("Error en la eliminación", "El libro no pudo ser eliminado")
                self.author.setEnabled(True)
                self.confirm.hide()
                self.deleteCancel.hide()

    @pyqtSlot()
    def cancelDelete(self):
        self.search.setEnabled(True)
        self.author.setEnabled(True)
        self.modificar.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.confirm.setEnabled(False)
        self.deleteCancel.setEnabled(False)
        self.confirm.hide()
        self.deleteCancel.hide()

    @pyqtSlot()
    def check_disable(self):
        if not self.titulo.text():
            self.search.setEnabled(False)
        else:
            self.search.setEnabled(True)

