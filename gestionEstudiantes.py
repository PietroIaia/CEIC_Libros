from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap#, #QAbstractItemView
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys

class gestionEstudiante(QWidget):

    def __init__(self):

        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Gestión de estudiantes")
        self.setStyleSheet('background-color: DodgerBlue')

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
        self.table = QTableWidget() #Tablas
        self.table.setColumnCount(1) #Columnas
        self.table.setRowCount(9)
        self.table.setHorizontalHeaderLabels(["Información del estudiante"])
        self.table.setVerticalHeaderLabels(["Carnet", "Nombre", "Apellido", "CI", "Tlf.", "email", "Días bloqueado", "Deuda Bs.", "Deuda USD."]) #Header
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setMaximumSize(self.getQTableWidgetSize())
        self.table.setMinimumSize(self.getQTableWidgetSize())
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

        #Ponemos la tabla y los botones en un mismo LAyout
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.table)
        self.tableLayout.addLayout(self.actionsLayout)

        #carnet del estudiante
        self.carnetLabel = QLabel("Número de carnet: ")
        self.carnet = QLineEdit(self)
        #self.carnetLabel.setStyleSheet('background-color: white')
        self.carnet.setStyleSheet('background-color: white')
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(self.carnetLabel)
        self.infoLayout.addWidget(self.carnet)

        #botones
        self.accept = QPushButton("Aceptar")
        self.nuevo = QPushButton("Agregar nuevo estudiante")
        self.accept.setStyleSheet('background-color: PowderBlue')
        self.nuevo.setStyleSheet('background-color: PowderBlue')
        self.searchLayout = QVBoxLayout()
        #self.searchLayout.addWidget(self.boxFrame)
        self.searchLayout.addLayout(self.infoLayout)
        self.searchLayout.addWidget(self.accept)
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

    def getQTableWidgetSize(self):
        w = self.table.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.table.columnCount()):
            w += self.table.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.table.horizontalHeader().height() + 4
        for i in range(self.table.rowCount()):
            h += self.table.rowHeight(i)
        return QSize(w, h)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    estudiante = gestionEstudiante()
    estudiante.show()
    sys.exit(app.exec_())