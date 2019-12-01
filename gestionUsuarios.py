#CEIC Libros
#Gestion de usuarios
#Desarrollado por Forward

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtCore, QtGui, QtWidgets
from Tables import UserTable
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from validationFunctions import verification_users, check_username
from AgregarUsuario import AgregarUsuario
from PyQt5.QtCore import *
import sys
import re

class gestionUsuarios(QWidget):

    def __init__(self, loggedUser):

        # Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de Usuarios")
        self.setStyleSheet('background-color: rgb(236, 240, 241)')
        self.old_perm_mask = ""

        # Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.titleFont.setBold(True)
        self.instFont = QFont("Serif", 12)
        self.buttonFont = QFont("Arial", 11)
        self.buttonFont.setBold(True)

        # Título
        self.title = QtWidgets.QLabel(self)
        self.title.setText("Gestión de Usuarios")
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
        self.table = UserTable() #Tablas

        # Botones de modificar, eliminar, cancelar y confirmar
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
        icon2.addPixmap(QtGui.QPixmap("static/delete-ceic-user-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eliminar.setIcon(icon2)
        self.eliminar.setIconSize(QtCore.QSize(25, 25))
        self.eliminar.setFlat(True)

        # Texto de los botones
        self.modificar.setText("      Modificar")
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

        # Ponemos la tabla y los botones en un mismo LAyout
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.table)
        self.tableLayout.addLayout(self.actionsLayout)
        self.setLayout(self.tableLayout)

        # Username de usuario
        self.currentUser = ""   # Guarda el valor del username del usuario actualmente mostrado en pantalla
        
        self.UserLabel = QtWidgets.QLabel(self)
        self.UserLabelFont = QFont("Arial", 12)
        self.UserLabelFont.setBold(True)
        self.UserLabel.setFont(self.UserLabelFont)
        self.UserLabel.setText("Usuario ")
        self.UserLabel.setStyleSheet('color: rgb(72, 84, 96)')
        self.UserLabel.setGeometry(10, 645, 500, 30)
        
        # Edit para ingresar el username del usuario
        self.User = QLineEdit(self)
        self.User.setStyleSheet('background-color: white; \n border-radius: 10px; border: 1px solid rgb(190, 198, 206); font: 12px;')
        self.User.setPlaceholderText(" Ingrese el username del usuario a consultar, modificar o eliminar")
        self.User.setGeometry(85, 645, 565, 30)

        # Botón de consulta
        self.search = QPushButton(self)
        self.set_button_style_sheet("search", "#37A2E4", "#238ED0", "#2D98DA", "15px")
        self.search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search.setText("Consultar")
        self.search.setGeometry(85, 680, 565, 30)
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
        self.guardar.clicked.connect(lambda: self.saveUpdate(loggedUser))
        self.eliminar.clicked.connect(self.deleteRequest)
        self.confirm.clicked.connect(self.deleteConfirm)
        self.deleteCancel.clicked.connect(self.cancelDelete)
        self.User.textChanged[str].connect(self.check_disable)

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

    def consulta(self):
        inputUser = self.User.text()

        if(check_username(inputUser)):
            self.consultaAux(inputUser)
        else:
            ErrorPrompt("Error de usuario", "El username no sigue el patrón correspondiente")

    def consultaAux(self,inputUser):
        queryText = "SELECT username, first_name, last_name, email, permission_mask, last_login,\
            creation_date FROM CEIC_User WHERE username = '" + inputUser + "';"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            self.currentUser = inputUser
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
            for i in range(self.table.rowCount()):
                if (i < 4):
                    self.table.item(i, 0).setText(str(self.query.value(i)))
                elif i == 4:
                    if int(self.query.value(i)) == 0:
                        self.table.cellWidget(i, 0).setCurrentIndex(0)
                    else:
                        self.table.cellWidget(i, 0).setCurrentIndex(1)
                    self.old_perm_mask = str(self.table.cellWidget(4, 0).currentText())
                else:
                    auxiliar = QDateTime.toString(self.query.value(i)).split()
                    self.table.item(i, 0).setText(str(auxiliar[0]+' '+auxiliar[2]+' '+auxiliar[1]+' '+auxiliar[4]+' '+auxiliar[3]))

            self.modificar.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("Error", "El usuario no existe, ingrese otro nombre de usuario ")

    @pyqtSlot()
    def update(self):
        #Permito modificar la tabla
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
        self.table.cellWidget(4, 0).setEnabled(True)
        self.table.item(0, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Username"
        self.table.item(5, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Ultima conexion"
        self.table.item(6, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)                         # No deja modificar la fila "Fecha de creacion"
        self.search.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.modificar.setEnabled(False)
        self.guardar.setEnabled(True)
        self.cancel.setEnabled(True)
        self.guardar.show()
        self.cancel.show()
        InfoPrompt("Modificación activada", "Se ha activado el modo modificación")

    @pyqtSlot()
    def saveUpdate(self, loggedUser):
        fields = self.table.getFields()
        self.query = QSqlQuery()

        if(self.old_perm_mask != fields[4]):
            Input = QInputDialog()
            input_logged_user_password = Input.getText(self, "Ingresar Contraseña", "Contraseña:")
            queryText = "SELECT * FROM CEIC_User WHERE username = '" + loggedUser + "' and password_ = crypt(\'" + input_logged_user_password[0] + "\', password_);"
            self.query.exec_(queryText)
            if(not self.query.first()):
                ErrorPrompt("Error", "Contraseña Inválida!")
                return
            
        correct = verification_users(fields, 5)
        if not correct:
            return

        values = self.table.getValues()
        queryText = "UPDATE CEIC_User SET " + values + " WHERE username = '" + self.table.item(0, 0).text() + "' returning username"
        self.query.exec_(queryText)

        if self.query.first():
            InfoPrompt("Actualización completada", "La información del usuario ha sido actualizada exitosamente")
            self.search.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.modificar.setEnabled(True)
            self.guardar.setEnabled(False)
            self.cancel.setEnabled(False)
            self.guardar.hide()
            self.cancel.hide()
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table.cellWidget(4, 0).setEnabled(False)
        else:
            ErrorPrompt("Error", "La información del usuario no pudo ser modificada")

    @pyqtSlot()
    def cancelUpdate(self):
        InfoPrompt("Modificación cancelada", "Los cambios hechos no fueron guardados")
        self.consultaAux(self.currentUser)
        self.search.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.modificar.setEnabled(True)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.guardar.hide()
        self.cancel.hide()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellWidget(4, 0).setEnabled(False)

    @pyqtSlot()
    def deleteRequest(self):
        ConfirmPrompt("Eliminación de usuario", "Se ha solicitado eliminar usuario. Marque el botón de confirmar eliminación para eliminar el usuario o el botón de cancelar eliminación para regresar")
        self.search.setEnabled(False)
        self.modificar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.confirm.setEnabled(True)
        self.deleteCancel.setEnabled(True)
        self.confirm.show()
        self.deleteCancel.show()

    @pyqtSlot()
    def deleteConfirm(self):
        inputUser = self.User.text()
        queryText = "DELETE FROM CEIC_User WHERE username = '" + inputUser + "';"
        self.query = QSqlQuery()
        self.query.exec_(queryText)
        self.search.setEnabled(True)
        self.modificar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.confirm.hide()
        self.deleteCancel.hide()
        self.table.clear()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellWidget(4, 0).setEnabled(False)
        self.User.clear()

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
        if not self.User.text():
            self.search.setEnabled(False)
        else:
            self.search.setEnabled(True)