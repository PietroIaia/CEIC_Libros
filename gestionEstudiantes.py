#CEIC Libros
#Tabla de estudiantes
#Autor: Diego Peña, 15-11095
#Fecha de inicio: 19-10-19, Apróx a las 10:00 am hora de Venezuela
#Última modifcación: 21-10-19, 11:00 am, Hora de Venezuela

#Actualización: La interfaz está prácticamente lista, consulta funciona bien, actualización va por la mitad
#To do:
#- Terminar modificación
#- Hacer eliminación y agregar
#- Color a las casillas de multa si la multa existe

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from StudentTable import StudentTable
from Prompt import ErrorPrompt, InfoPrompt
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
        self.title.setStyleSheet('background-color: DodgerBlue')
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
        #self.tableConfig()

        #Botones de agregar, modificar
        self.modificar = QPushButton("Modificar")
        self.guardar = QPushButton("Guardar Modificación")
        self.eliminar = QPushButton("Eliminar estudiante")
        self.modificar.setStyleSheet('background-color: PowderBlue')
        self.guardar.setStyleSheet('background-color: PowderBlue')
        self.eliminar.setStyleSheet('background-color: PowderBlue')
        self.actionsLayout = QVBoxLayout()
        self.actionsLayout.addWidget(self.modificar)
        self.actionsLayout.addWidget(self.guardar)
        self.actionsLayout.addWidget(self.eliminar)
        self.actionsLayout.addStretch()
        self.modificar.setEnabled(False)
        self.guardar.setEnabled(False)
        self.eliminar.setEnabled(False)

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

        #botones
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
        self.guardar.clicked.connect(self.saveUpdate)
        self.carnet.textChanged[str].connect(self.check_disable)

    def consulta(self):
        inputCarnet = self.carnet.text()

        if (self.carnetPattern.match(inputCarnet) is None):
            ErrorPrompt("Error de formato", "Error: Ese no es el formato de un carnet")
            return
            
        queryText = "SELECT * FROM Estudiante WHERE carnet = '" + inputCarnet + "';"
        self.query = QSqlQuery()
        self.query.exec_(queryText)

        if self.query.first():
            self.currentStudent = inputCarnet
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
            for i in range(self.table.rowCount() - 1):
                if (i < 8):
                    self.table.item(i, 0).setText(str(self.query.value(i)))
                else:
                    self.table.item(i, 0).setText(str(round(self.query.value(i), 2)))
            self.table.item(9, 0).setText(str(round(self.query.value(i) / 18500, 2)))
            self.modificar.setEnabled(True)
            self.guardar.setEnabled(True)
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
        InfoPrompt("Modificación activada", "Se ha activado el modo modificación")

    @pyqtSlot()
    def saveUpdate(self):
        correct = self.table.verification(self.carnetPattern)

        if not correct:
            return
            
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