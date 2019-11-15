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

        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de Libros")
        self.setStyleSheet('background-color: LightSkyBlue')

        #Regex del Titulo
        self.libroPattern = re.compile(r"[a-zA-Z]")

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.instFont = QFont("Serif", 12)

        #Título
        self.title = QLabel("Gestión de Libros")
        self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Instrucciones
        self.instrucciones = QLabel("Ingrese el Título del libro a consultar, ingresar o modificar")
        self.instrucciones.setStyleSheet('background-color: white')
        self.instrucciones.setFont(self.instFont)
        self.instrucciones.setFrameShape(QFrame.StyledPanel)
        self.instrucciones.setFrameShadow(QFrame.Plain)
        self.instrucciones.setLineWidth(0)

        #Tabla donde aparecerán los datos
        self.table = BooksTable() #Tablas

        #Botones de agregar, modificar, cancelar y confirmar (Acciones)
        self.modificar = QPushButton("Modificar")
        self.guardar = QPushButton("Guardar modificación")
        self.cancel = QPushButton("Cancelar modificación")
        self.eliminar = QPushButton("Eliminar Libro")
        self.inventario = QPushButton("Ver inventario")
        self.author = QPushButton("Buscar por autor")
        self.confirm = QPushButton("Confirmar eliminación")
        self.deleteCancel = QPushButton("Cancelar eliminación")
        self.confirm.hide()
        self.deleteCancel.hide()

        #Colores de los botones
        self.modificar.setStyleSheet('background-color: PowderBlue')
        self.cancel.setStyleSheet('background-color: PowderBlue')
        self.guardar.setStyleSheet('background-color: PowderBlue')
        self.eliminar.setStyleSheet('background-color: PowderBlue')
        self.inventario.setStyleSheet('background-color: Blue;')
        self.author.setStyleSheet('background-color: Blue')
        self.confirm.setStyleSheet('background-color: Red; color: white')
        self.deleteCancel.setStyleSheet('background-color: Red; color: white')
        
        #Configuración del layout
        self.actionsLayout = QVBoxLayout()
        self.actionsLayout.addWidget(self.modificar)
        self.actionsLayout.addWidget(self.guardar)
        self.actionsLayout.addWidget(self.cancel)
        self.actionsLayout.addWidget(self.eliminar)
        self.actionsLayout.addWidget(self.inventario)
        self.actionsLayout.addWidget(self.author)
        self.actionsLayout.addWidget(self.confirm)
        self.actionsLayout.addWidget(self.deleteCancel)
        self.actionsLayout.addStretch()

        #Desactivar botones
        self.modificar.setEnabled(False)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.confirm.setEnabled(False)
        self.deleteCancel.setEnabled(False)

        #Ponemos la tabla y los botones en un mismo LAyout
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.table)
        self.tableLayout.addLayout(self.actionsLayout)

        #Titulo del libro
        self.currentStudent = "" #Guarda el valor del titulo del libro actualmente mostrado en pantalla
        self.tituloLabel = QLabel("Título del libro: ")
        self.titulo = QLineEdit(self)
        self.titulo.setStyleSheet('background-color: white')
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(self.tituloLabel)
        self.infoLayout.addWidget(self.titulo)

        #botones de consulta y agregar
        self.search = QPushButton("Consultar")
        self.nuevo = QPushButton("Agregar nuevo Libro")
        self.search.setStyleSheet('background-color: PowderBlue')
        self.nuevo.setStyleSheet('background-color: PowderBlue')
        self.searchLayout = QVBoxLayout()
        self.searchLayout.addLayout(self.infoLayout)
        self.searchLayout.addWidget(self.search)
        self.searchLayout.addWidget(self.nuevo)
        self.search.setEnabled(False)

        #Layout del texto
        self.textLayout = QVBoxLayout()
        self.textLayout.addWidget(self.title)
        self.textLayout.addWidget(self.instrucciones)
        self.textLayout.addStretch()
        self.textLayout.addLayout(self.tableLayout)
        self.textLayout.addStretch()
        self.textLayout.addLayout(self.searchLayout)
    
        self.setLayout(self.textLayout)

        self.search.clicked.connect(self.consulta)
        self.modificar.clicked.connect(lambda: self.update(perm_mask))
        self.cancel.clicked.connect(self.cancelUpdate)
        self.guardar.clicked.connect(self.saveUpdate)
        self.inventario.clicked.connect(self.inventarioLibros)
        self.author.clicked.connect(self.searchAuthor)
        self.eliminar.clicked.connect(self.deleteRequest)
        self.confirm.clicked.connect(self.confirmDelete)
        self.deleteCancel.clicked.connect(self.cancelDelete)
        self.nuevo.clicked.connect(self.addBook)
        self.titulo.textChanged[str].connect(self.check_disable)

        # Guarda la cantidad de copias que tiene el libro, si se llega a modificar, la usaremos para ver cuantas copias hay que agregar al sistema
        self.noCopy = 0

    @pyqtSlot()
    def consulta(self):
        inputTitulo = self.titulo.text()

        if (self.libroPattern.match(inputTitulo) is None):
            ErrorPrompt("Error de formato", "Error: Ese no es el formato del Título de un Libro")
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
            ErrorPrompt("Error de búsqueda", "Error Libro no encontrado")

    @pyqtSlot()
    def update(self, perm_mask):
        #Permito modificar la tabla
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
        self.table.item(0, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "ID"
        self.table.item(5, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Cantidad prestada"
        if(perm_mask == 0):
            self.table.item(6, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                     # No deja modificar la fila "Duracion de prestamo" si el usuario no es Admin
        self.search.setEnabled(False)
        self.nuevo.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.modificar.setEnabled(False)
        self.inventario.setEnabled(False)
        self.guardar.setEnabled(True)
        self.cancel.setEnabled(True)
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
            InfoPrompt("Actualización completada", "La información del Libro ha sido actualizada exitosamente")
            self.search.setEnabled(True)
            self.nuevo.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.modificar.setEnabled(True)
            self.inventario.setEnabled(True)
            self.guardar.setEnabled(False)
            self.cancel.setEnabled(False)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("Error", "La información del libro no pudo ser modificada")

    @pyqtSlot()
    def cancelUpdate(self):
        InfoPrompt("Modificación cancelada", "Los cambios hechos no fueron guardados")
        self.consultaAux(self.currentBook)
        self.search.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.modificar.setEnabled(True)
        self.inventario.setEnabled(True)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot()
    def deleteRequest(self):
        ConfirmPrompt("Eliminación de Libro", "Se ha solicitado eliminar el Libro. Marque botón de eliminación para confirmar")
        self.search.setEnabled(False)
        self.nuevo.setEnabled(False)
        self.modificar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.inventario.setEnabled(False)
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
                self.nuevo.setEnabled(True)
                self.inventario.setEnabled(True)
                self.confirm.setEnabled(False)
                self.deleteCancel.setEnabled(False)
                self.confirm.hide()
                self.deleteCancel.hide()
                self.table.clear()
                self.titulo.setText("")
            else:
                ErrorPrompt("Error en la eliminación", "El libro no pudo ser eliminado")

    @pyqtSlot()
    def cancelDelete(self):
        self.search.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.modificar.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.inventario.setEnabled(True)
        self.confirm.setEnabled(False)
        self.deleteCancel.setEnabled(False)
        self.confirm.hide()
        self.deleteCancel.hide()

    @pyqtSlot()
    def addBook(self):
        self.form = verificarAutor()
        self.form.show()

    @pyqtSlot()
    def check_disable(self):
        if not self.titulo.text():
            self.search.setEnabled(False)
        else:
            self.search.setEnabled(True)

    @pyqtSlot()
    def inventarioLibros(self):
        self.table2 = InventarioBooksTable() #Tablas
        row = 0
        sql = "SELECT book_id, title FROM Book ORDER BY title"
        queryx = QSqlQuery(sql)
        while queryx.next():
           
            self.table2.insertRow(row)
            IDX = QTableWidgetItem(str(queryx.value(0)))
            titulox = QTableWidgetItem(str(queryx.value(1)))
            self.table2.setItem(row, 0, IDX)
            self.table2.setItem(row, 1, titulox)
            row = row + 1

        self.table2.setRowCount(row)
        self.table2.setTableColors()
        header = self.table2.horizontalHeader()       
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table2.show()

    @pyqtSlot()
    def searchAuthor(self):
        self.byAuthor = AuthorSearch()
        self.byAuthor.show()



        
