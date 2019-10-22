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
from StudentTable import StudentTable
from Prompt import ErrorPrompt, InfoPrompt, ConfirmPrompt
from validationFunctions import verification
from AgregarEstudiante import AgregarEstudiante
import sys
import re

class gestionEstudiante(QWidget):

    def __init__(self):

        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de estudiantes")
        self.setStyleSheet('background-color: LightSkyBlue')

        #Base de datos
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaCEIC")
        self.db.setUserName("postgres")
        self.db.setPassword("Tranc0nReloj-7aha")
        self.db.open()

        #Regex del carnet
        self.carnetPattern = re.compile(r"\d{2}\-\d{5}")

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.instFont = QFont("Serif", 12)

        #Título
        self.title = QLabel("Gestión de estudiantes")
        #self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Instrucciones
        self.instrucciones = QLabel("Ingrese el carnet del estudiante a consultar, ingresar o modificar")
        self.instrucciones.setStyleSheet('background-color: white')
        self.instrucciones.setFont(self.instFont)
        self.instrucciones.setFrameShape(QFrame.StyledPanel)
        self.instrucciones.setFrameShadow(QFrame.Plain)
        self.instrucciones.setLineWidth(0)

        #Tabla donde aparecerán los datos
        self.table = StudentTable() #Tablas

        #Botones de agregar, modificar, cancelar y confirmar (Acciones)
        self.modificar = QPushButton("Modificar")
        self.guardar = QPushButton("Guardar modificación")
        self.cancel = QPushButton("Cancelar modificación")
        self.eliminar = QPushButton("Eliminar estudiante")
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

        #carnet del estudiante
        self.currentStudent = "" #GUarda el valor del carnet del estudiante actualmente mostrado en pantalla
        self.carnetLabel = QLabel("Número de carnet: ")
        self.carnet = QLineEdit(self)
        self.carnet.setStyleSheet('background-color: white')
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(self.carnetLabel)
        self.infoLayout.addWidget(self.carnet)

        #botones de consulta y agregar
        self.search = QPushButton("Consultar")
        self.nuevo = QPushButton("Agregar nuevo estudiante")
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
        self.confirm.clicked.connect(self.confirmDelete)
        self.deleteCancel.clicked.connect(self.cancelDelete)
        self.nuevo.clicked.connect(self.addStudent)
        self.carnet.textChanged[str].connect(self.check_disable)

    @pyqtSlot()
    def consulta(self):
        inputCarnet = self.carnet.text()

        if (self.carnetPattern.match(inputCarnet) is None):
            ErrorPrompt("Error de formato", "Error: Ese no es el formato de un carnet")
            return

        self.consultaAux(inputCarnet)

    def consultaAux(self, carnetBuscado):
        queryText = "SELECT * FROM Estudiante WHERE carnet = '" + carnetBuscado + "';"
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
        correct = verification(fields, 10)

        if not correct:
            return

        values = self.table.getValues()
        #queryText = "UPDATE Estudiante SET carnet = :car, first_name = :fn, last_name = :ln, CI = :ci, phone = :num, \
        #    email = :mail, days_blocked"
        queryText = "UPDATE Estudiante SET " + values + " WHERE carnet = \'" + self.table.item(0, 0).text() + "\' returning carnet"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            InfoPrompt("Actualización completada", "La información del estudiante ha sido actualizada exitosamente")
            self.table.item(9, 0).setText(str(round(float(self.table.item(8, 0).text()) / 18500, 2)))
            self.search.setEnabled(True)
            self.nuevo.setEnabled(True)
            self.eliminar.setEnabled(True)
            self.modificar.setEnabled(True)
            self.guardar.setEnabled(False)
            self.cancel.setEnabled(False)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            ErrorPrompt("Error", "Alguno de los siguientes campos fue mal llenado: Carnet, CI o Libros prestados actualmente")

    @pyqtSlot()
    def cancelUpdate(self):
        InfoPrompt("Modificación cancelada", "Los cambios hechos no fueron guardados")
        self.consultaAux(self.currentStudent)
        self.search.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.modificar.setEnabled(True)
        self.guardar.setEnabled(False)
        self.cancel.setEnabled(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot()
    def deleteRequest(self):
        ConfirmPrompt("Eliminación de estudiante", "Se ha solicitado eliminar estudiante. Marque botón deeliminación para\
            confirmar")
        self.search.setEnabled(False)
        self.nuevo.setEnabled(False)
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
                self.nuevo.setEnabled(True)
                self.confirm.setEnabled(False)
                self.deleteCancel.setEnabled(False)
                self.confirm.hide()
                self.deleteCancel.hide()
                self.table.clear()
                self.carnet.setText("")
            else:
                ErrorPrompt("Error en la eliminación", "El estudiante posee libros sin devolver, no se puede eliminar")

    @pyqtSlot()
    def cancelDelete(self):
        self.search.setEnabled(True)
        self.nuevo.setEnabled(True)
        self.modificar.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.confirm.setEnabled(False)
        self.deleteCancel.setEnabled(False)
        self.confirm.hide()
        self.deleteCancel.hide()

    @pyqtSlot()
    def addStudent(self):
        self.form = AgregarEstudiante()
        self.form.show()

    @pyqtSlot()
    def check_disable(self):
        if not self.carnet.text():
            self.search.setEnabled(False)
            self.modificar.setEnabled(False)
            self.guardar.setEnabled(False)
            self.eliminar.setEnabled(False)
        else:
            self.search.setEnabled(True)
                

if __name__ == '__main__':
    app = QApplication(sys.argv)

    estudiante = gestionEstudiante()
    estudiante.show()
    sys.exit(app.exec_())