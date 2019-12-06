#CEIC Libros
#Tabla de estudiantes
#Desarrollado por Forward
#Responsable del módulo: Diego Peña, 15-11095
#Fecha de inicio: 21-10-19, Apróx 8:20 am, Hora de Venezuela
#Última modifcación: 22-10-19, 19:13, Hora de Venezuela

#Actualización: Clear está listo

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor, QKeySequence
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Prompt import ErrorPrompt


###################################################
#                 Tabla de Estudiantes            #
###################################################
class StudentTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1) #Columnas
        self.setRowCount(10)
        self.setHorizontalHeaderLabels(["Información del estudiante"])
        self.setVerticalHeaderLabels(["Carnet", "Nombre", "Apellido", "CI", "Tlf.", "email", "Días Sancionado", "Libros prestados actualmente", "Deuda Bs.", "Deuda USD."]) #Header
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)

        self.fontData = QFont("Helvetica", 12)

        for i in range(0, 10):
            self.verticalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
            self.item(i, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.item(i, 0).setFont(self.fontData)

    def getQTableWidgetSize(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

    def setTableColors(self):
        for i in range(self.rowCount()):
            self.setItem(i, 0, QTableWidgetItem())
            if (i % 2 == 0):
                self.item(i, 0).setBackground(QColor(234, 235, 235))
            else:
                self.item(i, 0).setBackground(QColor(244, 245, 245))

    def clear(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setText("")
            if (i % 2 == 0):
                self.item(i, 0).setBackground(QColor(234, 235, 235))
            else:
                self.item(i, 0).setBackground(QColor(244, 245, 245))

    def getFields(self):
        fields = []
        for i in range(10):
            fields.append(self.item(i, 0).text())

        return fields

    def getValues(self):
        updateRequest = "carnet = \'" + self.item(0, 0).text() + "\', "
        updateRequest += "first_name = \'" + self.item(1, 0).text() + "\', "
        updateRequest += "last_name = \'" + self.item(2, 0).text() + "\', "
        updateRequest += "CI = " + self.item(3,0).text() + ", "
        updateRequest += "phone = " + self.item(4,0).text() + ", "
        updateRequest += "email = \'" + self.item(5,0).text() + "\', "
        updateRequest += "days_blocked = " + self.item(6,0).text() + ", "
        updateRequest += "current_Books = " + self.item(7,0).text() + ", "
        updateRequest += "book_debt = " + self.item(8,0).text()

        return updateRequest


###################################################
#                 Tabla de Libros                 #
###################################################
class BooksTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1) #Columnas
        self.setRowCount(7)
        self.setHorizontalHeaderLabels(["Información del Libro"])
        self.setVerticalHeaderLabels(["ID", "Título", "Autores", "ISBN", "Cantidad", "Cantidad prestada", "Duración del préstamo\n(en días)"]) #Header
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver;")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)

        self.fontData = QFont("Helvetica", 12)

        for i in range(0, 7):
            self.verticalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
            self.item(i, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.item(i, 0).setFont(self.fontData)
    
    def getQTableWidgetSize(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

    def setTableColors(self):
        for i in range(self.rowCount()):
            self.setItem(i, 0, QTableWidgetItem())
            if (i % 2 == 0):
                self.item(i, 0).setBackground(QColor(234, 235, 235))
            else:
                self.item(i, 0).setBackground(QColor(244, 245, 245))

    def clear(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setText("")
            if (i % 2 == 0):
                self.item(i, 0).setBackground(QColor(234, 235, 235))
            else:
                self.item(i, 0).setBackground(QColor(244, 245, 245))

    def getFields(self):
        fields = []
        for i in range(7):
            fields.append(self.item(i, 0).text())

        return fields

    def getValues(self):
        updateRequest = "book_id = \'" + self.item(0, 0).text() + "\', "
        updateRequest += "title = \'" + self.item(1, 0).text() + "\', "
        updateRequest += "authors = \'" + self.item(2, 0).text() + "\', "
        updateRequest += "isbn = \'" + self.item(3,0).text() + "\', "
        updateRequest += "quantity = \'" + self.item(4,0).text() + "\', "
        updateRequest += "quantity_lent = \'" + self.item(5,0).text() + "\', "
        updateRequest += "loan_duration = \'" + self.item(6,0).text() +"\'"

        return updateRequest


###################################################
#                 Tabla de Usuarios               #
###################################################
class UserTable(QTableWidget):
    def __init__(self):
        super().__init__()
        # Creamos el ComboBox para los permisos
        comboBox = QComboBox()
        comboBox.insertItem(0, "Usuario")
        comboBox.insertItem(1, "Administrador")
        comboBox.insertItem(2, "")                                     #El segundo item es el default
        comboBox.setCurrentIndex(2)
        comboBox.model().item(2).setEnabled(False)                     #Lo ponemos disabled para que el usuario no pueda clickearlo
        # Creamos la tabla
        self.setColumnCount(1) #Columnas
        self.setRowCount(7)
        self.setHorizontalHeaderLabels(["Información del usuario"])
        self.setVerticalHeaderLabels(['Nombre de usuario', 'Nombre', 'Apellido', 'Email', 'Permisos', 'Última conexión', 'Fecha de creación']) #Header
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setCellWidget(4, 0, comboBox)
        self.setTableColors()
        self.cellWidget(4, 0).setEnabled(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)

        self.fontData = QFont("Helvetica", 12)

        for i in range(0, 7):
            self.verticalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
            self.item(i, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.item(i, 0).setFont(self.fontData)

    def getQTableWidgetSize(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

    def setTableColors(self):
        for i in range(self.rowCount()):
            self.setItem(i, 0, QTableWidgetItem())
            if (i % 2 == 0):
                self.item(i, 0).setBackground(QColor(234, 235, 235))
            else:
                self.item(i, 0).setBackground(QColor(244, 245, 245))
        self.cellWidget(4, 0).setStyleSheet('background-color: rgb(234, 235, 235); border: 0px')

    def clear(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setText("")
            if (i % 2 == 0):
                self.item(i, 0).setBackground(QColor(234, 235, 235))
            else:
                self.item(i, 0).setBackground(QColor(244, 245, 245))
        self.cellWidget(4, 0).setCurrentIndex(2)

    def getFields(self):
        fields = []
        for i in range(7):
            if(i == 4):
                fields.append(str(self.cellWidget(4, 0).currentText()))
            else:
                fields.append(self.item(i, 0).text())

        return fields

    def getValues(self):
        updateRequest = "username = \'" + self.item(0, 0).text() + "\', "
        updateRequest += "first_name = \'" + self.item(1, 0).text() + "\', "
        updateRequest += "last_name = \'" + self.item(2,0).text() + "\', "
        updateRequest += "email = \'" + self.item(3,0).text() + "\', "
        if (str(self.cellWidget(4, 0).currentText()) == "Administrador"):
            updateRequest += "permission_mask = 1"
        else:
            updateRequest += "permission_mask = 0"

        return updateRequest

###################################################
#           Tabla de Libros en prestamo           #
###################################################
class Books_Loan_Table(QTableWidget):
    def __init__(self, place):
        super().__init__(place)
        self.setColumnCount(3) #Columnas
        self.setRowCount(7)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) #Ajuste de tamaño
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(61)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalHeaderLabels(["ID", "Título", ""])
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 390)
        self.setColumnWidth(2, 10)
        self.setStyleSheet("background-color:  Silver")
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        for i in range(self.rowCount()):
            self.setCellWidget(i, 2, QPushButton())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.clear()

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)

        #self.fontData = QFont("Helvetica", 12)

        #for i in range(0, 3):
        #    self.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
        #    self.item(i, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #    self.item(i, 0).setFont(self.fontData)
    
    def getQTableWidgetSize(self):
        w = 0
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        return QSize(w+23, 430)

    def setTableColors(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if(j == 2):
                    self.cellWidget(i, j).setStyleSheet('background-color: rgb(234, 235, 235); border: 0px')
                else:
                    self.setItem(i, j, QTableWidgetItem())
                    self.item(i, j).setBackground(QColor(234, 235, 235))

    def clear(self):
        for i in range(self.rowCount()):
            self.cellWidget(i, 2).setEnabled(False)
            for j in range(self.columnCount()):
                if(j != 2):
                    self.item(i, j).setText("")
                    self.item(i, j).setBackground(QColor(234, 235, 235))
                else:
                    self.cellWidget(i, j).setText("")
                    self.cellWidget(i, 2).setEnabled(False)

    

###################################################
#           Tabla de Prestamos Activos            #
###################################################
class Active_Loan_Table(QTableWidget):
    def __init__(self, place):
        super().__init__(place)
        self.setColumnCount(5) #Columnas
        self.setRowCount(40)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) #Ajuste de tamaño
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(40)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalHeaderLabels(["Carnet", "Nombre", "Apellido", "Tiempo restante", "Libros"])
        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 115)
        self.setColumnWidth(4, 238)
        self.setStyleSheet("background-color:  Silver")
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.clear()

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)
    
    def getQTableWidgetSize(self):
        w = 0
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        return QSize(w+23, 170)

    def setTableColors(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem())
                self.item(i, j).setBackground(QColor(234, 235, 235))

    def clear(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                self.item(i, j).setBackground(QColor(234, 235, 235))

###################################################
#           Tabla de Transferencias               #
###################################################

class Payments_Table(QTableWidget):
    def __init__(self, place):
        super().__init__(place)
        self.setColumnCount(5) #Columnas
        self.setRowCount(50)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) #Ajuste de tamaño
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(40)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalHeaderLabels(["Usuario", "Cliente", "Monto", "Banco", "Código"])
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 120)
        self.setStyleSheet("background-color:  Silver")
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.clear()

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)
    
    def getQTableWidgetSize(self):
        w = 0
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        return QSize(w+16, 300)

    def setTableColors(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem())
                self.item(i, j).setBackground(QColor(234, 235, 235))

    def clear(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                self.item(i, j).setBackground(QColor(234, 235, 235))

###################################################
#             Tabla de Deudas                     #
###################################################

class Debts_Table(QTableWidget):
    def __init__(self, place):
        super().__init__(place)
        self.setColumnCount(4) #Columnas
        self.setRowCount(50)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) #Ajuste de tamaño
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(30)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalHeaderLabels(["Carnet", "Nombre", "Apellido", "Deuda"])
        self.setColumnWidth(0, 130)
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 130)
        self.setColumnWidth(3, 130)
        self.setStyleSheet("background-color:  Silver")
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.clear()

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)
    
    def getQTableWidgetSize(self):
        w = 0
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        return QSize(w+16, 250)

    def setTableColors(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem())
                self.item(i, j).setBackground(QColor(255, 255, 255))

    def clear(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                self.item(i, j).setBackground(QColor(234, 235, 235))

###################################################
#           Tabla de inventario de libros         #
###################################################
class InventarioBooksTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario de libros") #Título
        self.setColumnCount(2) #Columnas
        self.setHorizontalHeaderLabels(["ID","Título"])
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
    
    def getQTableWidgetSize(self):
        return QSize(800, 570)

    def setTableColors(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setBackground(QColor(235, 235, 235))
            self.item(i, 1).setBackground(QColor(235, 235, 235))

###################################################
#                 Tabla de autores                #
###################################################
class autoresTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario de autores") #Título
        self.setColumnCount(3) #Columnas
        self.setHorizontalHeaderLabels(["Nombre","Apellido","ID"])
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def getQTableWidgetSize(self):
        return QSize(500, 570)

    def setTableColors(self):
        for i in range(self.rowCount()):
            self.item(i, 0).setBackground(QColor(224, 255, 255))
            self.item(i, 1).setBackground(QColor(224, 255, 255))
            self.item(i, 2).setBackground(QColor(224, 255, 255))

    def llenarAutores(self):
        row = 0
        sql = "SELECT * FROM Author ORDER BY last_name"  ## cambiar esto
        queryx = QSqlQuery(sql)
        while queryx.next():
           
            self.insertRow(row)
            IDX = QTableWidgetItem(str(queryx.value(0)))
            IDX2 = QTableWidgetItem(str(queryx.value(1)))
            IDX3 = QTableWidgetItem(str(queryx.value(2)))
            self.setItem(row, 0, IDX)
            self.setItem(row, 1, IDX2)
            self.setItem(row, 2, IDX3)
            row = row + 1

        self.setRowCount(row)
        self.setTableColors()
        header = self.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        #self.db.close()

    def clear(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                self.item(i, j).setBackground(QColor(224, 255, 255))

###################################################
#           Tabla de libros de un autor           #
###################################################

class AuthorSearchTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(4) #Columnas
        self.setRowCount(15)
        self.setHorizontalHeaderLabels(["Título", "Código", "Cant. Disp", "Duración"])
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("background-color:  Silver")
        self.setColumnWidth(0, 500)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)

    def getQTableWidgetSize(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

    def setTableColors(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem())
                self.item(i, j).setBackground(QColor(234, 235, 235))

    def clearTable(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                self.item(i, j).setBackground(QColor(234, 235, 235))

    def keyPressEvent(self, event):
        clipboard = QApplication.clipboard()
        if event.matches(QKeySequence.Copy):
            clipboard.setText("some text")
        if event.matches(QKeySequence.Paste):
            print(clipboard.text())
        QTableWidget.keyPressEvent(self, event)


###################################################
#           Tabla de Sanciones actuales           #
###################################################

class Sanciones_Table(QTableWidget):
    def __init__(self, place):
        super().__init__(place)
        self.setColumnCount(5) #Columnas
        self.setRowCount(50)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) #Ajuste de tamaño
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(40)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalHeaderLabels(["Carnet", "Nombre", "Apellido", "Dias sanción", "Libros por prestamo"])
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 120)
        self.setStyleSheet("background-color:  Silver")
        self.setMaximumSize(self.getQTableWidgetSize())
        self.setMinimumSize(self.getQTableWidgetSize())
        self.setTableColors()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.clear()

        self.fontHeader = QFont("Helvetica", 10)
        self.fontHeader.setBold(True)
        self.horizontalHeader().setFont(self.fontHeader)
        self.verticalHeader().setFont(self.fontHeader)
    
    def getQTableWidgetSize(self):
        w = 0
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        return QSize(w+16, 300)

    def setTableColors(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem())
                self.item(i, j).setBackground(QColor(234, 235, 235))

    def clear(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                self.item(i, j).setBackground(QColor(234, 235, 235))