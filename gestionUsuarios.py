#CEIC Libros
#Gestion de usuarios
#Desarrollado por Forward

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Tables import UserTable
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from validationFunctionsUsuarios import verification
from AgregarUsuario import AgregarUsuario
from PyQt5.QtCore import *
import sys
import re

class gestionUsuarios(QWidget):

    def __init__(self):

        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de Usuarios")
        self.setStyleSheet('background-color: LightSkyBlue')

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.instFont = QFont("Serif", 12)

        #Título
        self.title = QLabel("Gestión de Usuarios")
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Instrucciones
        self.instrucciones = QLabel("Ingrese el username del usuario a consultar, ingresar o modificar")
        self.instrucciones.setStyleSheet('background-color: white')
        self.instrucciones.setFont(self.instFont)
        self.instrucciones.setFrameShape(QFrame.StyledPanel)
        self.instrucciones.setFrameShadow(QFrame.Plain)
        self.instrucciones.setLineWidth(0)

        #Tabla donde aparecerán los datos
        self.table = UserTable() #Tablas

        #Botones de agregar, modificar, cancelar y confirmar (Acciones)
        self.modificar = QPushButton("Modificar")
        self.guardar = QPushButton("Guardar modificación")
        self.cancel = QPushButton("Cancelar modificación")
        self.eliminar = QPushButton("Eliminar Usuario")
        self.confirm = QPushButton("Confirmar eliminación")
        self.deleteCancel = QPushButton("Cancelar eliminación")
        self.confirm.hide()
        self.deleteCancel.hide()

        #Colores de los botones
        self.modificar.setStyleSheet('background-color: PowderBlue')
        self.cancel.setStyleSheet('background-color: PowderBlue')
        self.guardar.setStyleSheet('background-color: PowderBlue')
        self.eliminar.setStyleSheet('background-color: PowderBlue')
        self.confirm.setStyleSheet('background-color: Red; color: white')
        self.deleteCancel.setStyleSheet('background-color: Red; color: white')
        
        #Configuración del layout
        self.actionsLayout = QVBoxLayout()
        self.actionsLayout.addWidget(self.modificar)
        self.actionsLayout.addWidget(self.guardar)
        self.actionsLayout.addWidget(self.cancel)
        self.actionsLayout.addWidget(self.eliminar)
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

        #username de usuario
        self.currentUser = "" #GUarda el valor del username del usuario actualmente mostrado en pantalla
        self.UserLabel = QLabel("Nombre de usuario: ")
        self.User = QLineEdit(self)
        self.User.setStyleSheet('background-color: white')
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(self.UserLabel)
        self.infoLayout.addWidget(self.User)

        #botones de consulta y agregar
        self.search = QPushButton("Consultar")
        self.nuevo = QPushButton("Agregar nuevo usuario")
        self.search.setStyleSheet('background-color: PowderBlue')
        self.nuevo.setStyleSheet('background-color: PowderBlue')
        self.searchLayout = QVBoxLayout()
        self.searchLayout.addLayout(self.infoLayout)
        self.searchLayout.addWidget(self.search)
        self.searchLayout.addWidget(self.nuevo)

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
        self.modificar.clicked.connect(self.update)
        self.cancel.clicked.connect(self.cancelUpdate)
        self.guardar.clicked.connect(self.saveUpdate)
        self.eliminar.clicked.connect(self.deleteRequest)
        self.confirm.clicked.connect(self.deleteConfirm)
        self.deleteCancel.clicked.connect(self.cancelDelete)
        self.nuevo.clicked.connect(self.addUser)
        self.User.textChanged[str].connect(self.check_disable)


    def consulta(self):
        inputUser = self.User.text()
        queryText = "SELECT * FROM CEIC_User WHERE username = '" + inputUser + "';"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            self.currentUser = inputUser
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
            for i in range(self.table.rowCount()):
                if (i < 6):
                    self.table.item(i, 0).setText(str(self.query.value(i)))
                else:
                    auxiliar = QDateTime.toString(self.query.value(i)).split()
                    self.table.item(i, 0).setText(str(auxiliar[0]+' '+auxiliar[2]+' '+auxiliar[1]+' '+auxiliar[4]+' '+auxiliar[3]))

            self.modificar.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("Error", "El usuario no existe, ingrese otro nombre de usuario ")

    def consultaAux(self,inputUser):
        queryText = "SELECT * FROM CEIC_User WHERE username = '" + inputUser + "';"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            self.currentUser = inputUser
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
            for i in range(self.table.rowCount()):
                if (i < 6):
                    self.table.item(i, 0).setText(str(self.query.value(i)))
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
        self.search.setEnabled(False)
        self.nuevo.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.modificar.setEnabled(False)
        self.guardar.setEnabled(True)
        self.cancel.setEnabled(True)
        InfoPrompt("Modificación activada", "Se ha activado el modo modificación")

    @pyqtSlot()
    def saveUpdate(self):
        fields = self.table.getFields()
        correct = verification(fields, 6)

        if not correct:
            return

        values = self.table.getValues()
        valorUser = self.table.item(0, 0).text()
        puede = 1
        puede2 = 1
        if valorUser != self.User.text():
            puede2 = 0
        queryText2 = "SELECT * FROM CEIC_User WHERE username = '" + valorUser + "';"
        self.query2 = QSqlQuery()
        self.query2.exec_(queryText2)

        if self.query2.first():
            puede = 0;

        if puede ==1 or (puede == 0 and puede2 == 1):
            queryText = "UPDATE CEIC_User SET " + values + " WHERE username = \'" + self.table.item(0, 0).text() + "\' returning username"
            self.query = QSqlQuery()
            self.query.exec_(queryText)

            if self.query.first():
                InfoPrompt("Actualización completada", "La información del usuario ha sido actualizada exitosamente")
                self.search.setEnabled(True)
                self.nuevo.setEnabled(True)
                self.eliminar.setEnabled(True)
                self.modificar.setEnabled(True)
                self.guardar.setEnabled(False)
                self.cancel.setEnabled(False)
                self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            else:
                ErrorPrompt("Error", "Alguno de los siguientes campos no fue llenado correctamente: Nombre de usuario, permisos o correo")
        else:
            ErrorPrompt("Error", "El nombre de usuario coincide con uno ya existente, por favor ingrese otro nombre")

    @pyqtSlot()
    def cancelUpdate(self):
        InfoPrompt("Modificación cancelada", "Los cambios hechos no fueron guardados")
        self.consultaAux(self.currentUser)
        self.search.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.modificar.setEnabled(True)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot()
    def deleteRequest(self):
        ConfirmPrompt("Eliminación de usuario", "Se ha solicitado eliminar usuario. Marque el botón de confirmar eliminación para eliminar el usuario o el boton de cancelar eliminacion para regresar")
        self.search.setEnabled(False)
        self.nuevo.setEnabled(False)
        self.modificar.setEnabled(False)
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
        self.nuevo.setEnabled(True)
        self.modificar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.confirm.hide()
        self.deleteCancel.hide()
        for i in range(self.table.rowCount()):
                if (i < 6):
                    self.table.item(i, 0).setText(str(""))
                else:
                    self.table.item(i, 0).setText(str(""))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.User.clear()

    @pyqtSlot()
    def cancelDelete(self):
        self.search.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.modificar.setEnabled(True)
        self.confirm.setEnabled(False)
        self.deleteCancel.setEnabled(False)
        self.confirm.hide()
        self.deleteCancel.hide()

    @pyqtSlot()
    def addUser(self):
        self.form = AgregarUsuario()
        self.form.show()
        

    @pyqtSlot()
    def check_disable(self):
        if not self.User.text():
            self.search.setEnabled(False)
            self.modificar.setEnabled(False)
            self.guardar.setEnabled(False)
            self.eliminar.setEnabled(False)
        else:
            self.search.setEnabled(True)
                

#if __name__ == '__main__':
#    app = QApplication(sys.argv)

#    estudiante = gestionUsuarios()
#    estudiante.show()
#    sys.exit(app.exec_())