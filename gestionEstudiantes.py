#CEIC Libros
#Tabla de estudiantes
#Desarrollado por Forward
#Responsable del módulo: Diego Peña, 15-11095
#Fecha de inicio: 19-10-19, Apróx a las 10:00 am hora de Venezuela
#Última modifcación: 22-10-19, 19:14 pm, Hora de Venezuela

#Actualización: Lo fundamental está listo y la interfaz es 100% funcional, estable y presentable
#To do:
#- Color a las casillas de multa si la multa existe

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from Tables import StudentTable
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from validationFunctions import verification_estudiantes
from AgregarEstudiante import AgregarEstudiante
import sys
import re

class gestionEstudiante(QWidget):

    def __init__(self, perm_mask):

        # Inicialización de la ventana
        super().__init__()
        self.permission = perm_mask
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de Estudiantes")
        self.setStyleSheet('background-color: rgb(236, 240, 241)')

        # Regex del carnet
        self.carnetPattern = re.compile(r"\d\d\-\d{5}")

        # Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.titleFont.setBold(True)
        self.instFont = QFont("Serif", 12)
        self.buttonFont = QFont("Arial", 11)
        self.buttonFont.setBold(True)

        # Título
        self.title = QtWidgets.QLabel(self)
        self.title.setText("Gestión de Estudiantes")
        self.title.setStyleSheet('color: rgb(30, 39, 46)')
        self.title.setFont(self.titleFont)
        self.title.setGeometry(10, 15, 350, 50)

        # Línea debajo del título
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 55, 820, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Tabla donde aparecerán los datos
        self.table = StudentTable()

        # Botones de agregar, modificar, cancelar y confirmar (Acciones)
        self.modificar = QPushButton(self)
        self.guardar = QPushButton(self)
        self.cancel = QPushButton(self)
        self.eliminar = QPushButton(self)
        self.confirm = QPushButton(self)
        self.deleteCancel = QPushButton(self)

        # Se esconden los botones
        self.confirm.hide()
        self.deleteCancel.hide()
        self.guardar.hide()
        self.cancel.hide()

        # Ícono para el botón modificar
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("static/edit-ceic-user-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modificar.setIcon(icon1)
        self.modificar.setIconSize(QtCore.QSize(40, 30))
        self.modificar.setFlat(True)

        # Ícono para el botón eliminar
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("static/delete-user-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eliminar.setIcon(icon2)
        self.eliminar.setIconSize(QtCore.QSize(31, 31))
        self.eliminar.setFlat(True)

        # Texto de los botones
        self.modificar.setText("       Modificar")
        self.guardar.setText("Guardar")
        self.cancel.setText("Cancelar")
        self.eliminar.setText("         Eliminar")
        self.confirm.setText("Confirmar")
        self.deleteCancel.setText("Cancelar")

        # CSS de los botones
        self.set_button_style_sheet("modificar", "#2D98DA", "#238ED0", "#C8C8C8", "17px")
        self.set_button_style_sheet("cancel", "#55c1ff", "#41acee", "#4bb6f8", "15px")
        self.set_button_style_sheet("guardar", "#55c1ff", "#41acee", "#4bb6f8", "15px")
        self.set_button_style_sheet("eliminar", "#C20000", "#CC0000", "#C8C8C8", "17px")
        self.set_button_style_sheet("confirm", "#b80000", "#CC0000", "#D60000", "15px")
        self.set_button_style_sheet("deleteCancel", "#b80000", "#CC0000", "#D60000", "15px")

        # Cursor para los botones
        self.modificar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.guardar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.eliminar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteCancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Posición para los botones
        self.modificar.setGeometry(657, 150, 180, 35)
        self.guardar.setGeometry(657, 535, 180, 30)
        self.cancel.setGeometry(657, 570, 180, 30)
        self.eliminar.setGeometry(657, 190, 180, 35)
        self.confirm.setGeometry(657, 535, 180, 30)
        self.deleteCancel.setGeometry(657, 570, 180, 30)

        # Font de los botones
        self.modificar.setFont(self.buttonFont)
        self.cancel.setFont(self.buttonFont)
        self.guardar.setFont(self.buttonFont)
        self.eliminar.setFont(self.buttonFont)
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

        # Ponemos la tabla y los botones en un mismo layout
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.table)
        self.tableLayout.addLayout(self.actionsLayout)
        self.setLayout(self.tableLayout)

        # Carnet del estudiante
        self.currentStudent = "" # Guarda el valor del carnet del estudiante actualmente mostrado en pantalla

        self.carnetLabel = QtWidgets.QLabel(self)
        self.carnetLabelFont = QFont("Arial", 12)
        self.carnetLabelFont.setBold(True)
        self.carnetLabel.setFont(self.carnetLabelFont)
        self.carnetLabel.setText("Carnet ")
        self.carnetLabel.setStyleSheet('color: rgb(72, 84, 96)')
        self.carnetLabel.setGeometry(10, 645, 500, 30)

        # Edit para ingresar el carnet del estudiante
        self.carnet = QLineEdit(self)
        self.carnet.setStyleSheet('background-color: white; \n border-radius: 10px; border: 1px solid rgb(190, 198, 206); font: 12px;')
        self.carnet.setPlaceholderText(" Ingrese el carnet del estudiante a consultar, modificar o eliminar")
        self.carnet.setGeometry(70, 645, 585, 30)

        # Botón de consulta
        self.search = QPushButton(self)
        self.set_button_style_sheet("search", "#37A2E4", "#238ED0", "#2D98DA", "15px")
        self.search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search.setText("Consultar")
        self.search.setGeometry(70, 680, 585, 30)
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
        self.modificar.clicked.connect(self.update)
        self.cancel.clicked.connect(self.cancelUpdate)
        self.guardar.clicked.connect(self.saveUpdate)
        self.eliminar.clicked.connect(self.deleteRequest)
        self.confirm.clicked.connect(self.confirmDelete)
        self.deleteCancel.clicked.connect(self.cancelDelete)
        self.carnet.textChanged[str].connect(self.check_disable)

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
        inputCarnet = self.carnet.text()

        if (self.carnetPattern.match(inputCarnet) is None):
            ErrorPrompt("Error de formato", "Error: Ese no es el formato de un carnet")
            return

        self.consultaAux(inputCarnet)

    def consultaAux(self, carnetBuscado):
        queryText = "SELECT carnet, first_name, last_name, CI, phone, email, days_blocked, current_books, book_debt FROM Estudiante WHERE carnet = '" + carnetBuscado + "';"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            self.currentStudent = carnetBuscado
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
            for i in range(self.table.rowCount() - 1):
                if (i < 8):
                    self.table.item(i, 0).setText(str(self.query.value(i)))
                else:
                    self.table.item(i, 0).setText(str(round(self.query.value(i), 2)))
            self.table.item(9, 0).setText(str(round(self.query.value(i) / 18500, 2)))
            self.table.item(9, 0).setFlags(Qt.ItemIsEnabled)
            self.modificar.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("ENE Piso 3", "Error ENE_Piso3: Estudiante Not Found")

    @pyqtSlot()
    def update(self):
        #Permito modificar la tabla
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
        self.table.item(0, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Carnet"
        self.table.item(6, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Dias bloqueado"
        self.table.item(7, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Libros prestdos actaulmente"
        self.table.item(8, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Deuda Bs."
        self.table.item(9, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Deuda USD."
        self.search.setEnabled(False)
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
        correct = verification_estudiantes(fields, 10)

        if not correct:
            return

        values = self.table.getValues()
        queryText = "UPDATE Estudiante SET " + values + " WHERE carnet = \'" + self.table.item(0, 0).text() + "\' returning carnet"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            InfoPrompt("Actualización completada", "La información del estudiante ha sido actualizada exitosamente")
            self.table.item(9, 0).setText(str(round(float(self.table.item(8, 0).text()) / 18500, 2)))
            self.search.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.modificar.setEnabled(True)
            self.guardar.setEnabled(False)
            self.cancel.setEnabled(False)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("Error", "Alguno de los siguientes campos fue mal llenado: Carnet, CI o Libros prestados actualmente")

        self.guardar.hide()
        self.cancel.hide()

    @pyqtSlot()
    def cancelUpdate(self):
        InfoPrompt("Modificación cancelada", "Los cambios hechos no fueron guardados")
        self.consultaAux(self.currentStudent)
        self.search.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.modificar.setEnabled(True)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.guardar.hide()
        self.cancel.hide()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot()
    def deleteRequest(self):
        if (self.permission != 1):
            ErrorPrompt("Se necesitan permisos adicionales", "Usted no dispone de los permisos necesarios para esta acción")
            return
    
        ConfirmPrompt("Eliminación de estudiante", "Se ha solicitado eliminar estudiante. Marque botón de eliminación para\
            confirmar")
        self.search.setEnabled(False)
        self.modificar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.confirm.setEnabled(True)
        self.deleteCancel.setEnabled(True)
        self.confirm.show()
        self.deleteCancel.show()

    @pyqtSlot()
    def confirmDelete(self):
        if (int(self.table.item(7, 0).text()) != 0):
            ErrorPrompt("Error en la eliminación", "El estudiante posee libros sin devolver, no se puede eliminar")
        else:
            queryText = "DELETE FROM Estudiante WHERE carnet = \'" + self.table.item(0, 0).text() + "\' RETURNING carnet"
            self.query = QSqlQuery()
            self.query.exec_(queryText)

            if self.query.first():
                InfoPrompt("Eliminación exitosa", "El estudiante ha sido eliminado del sistema")
                self.search.setEnabled(True)
                self.confirm.setEnabled(False)
                self.deleteCancel.setEnabled(False)
                self.confirm.hide()
                self.deleteCancel.hide()
                self.table.clear()
                self.carnet.setText("")
            else:
                ErrorPrompt("Error en la eliminación", "El estudiante no pudo ser eliminado")
                self.confirm.hide()
                self.deleteCancel.hide()

    @pyqtSlot()
    def cancelDelete(self):
        self.search.setEnabled(True)
        self.modificar.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.confirm.setEnabled(False)
        self.deleteCancel.setEnabled(False)
        self.confirm.hide()
        self.deleteCancel.hide()

    @pyqtSlot()
    def check_disable(self):
        if not self.carnet.text():
            self.search.setEnabled(False)
        else:
            self.search.setEnabled(True)