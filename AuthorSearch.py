from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
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

        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 0, 600, 600)
        self.setWindowTitle("Búsqueda por autor")
        self.setStyleSheet('background-color: LightSkyBlue')

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)
        self.instFont = QFont("Serif", 12)

        #Título
        self.title = QLabel("Búsqueda por autor")
        self.title.setStyleSheet('background-color: DodgerBlue')
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Instrucciones
        self.instrucciones = QLabel("Seleccione el autor cuyos libros desea conocer")
        self.instrucciones.setStyleSheet('background-color: white')
        self.instrucciones.setFont(self.instFont)
        self.instrucciones.setFrameShape(QFrame.StyledPanel)
        self.instrucciones.setFrameShadow(QFrame.Plain)
        self.instrucciones.setLineWidth(0)

        self.table = AuthorSearchTable()

        #Menú de autores
        self.authorLabel = QLabel("Autor: ")
        self.authorList = QComboBox()
        self.setAuthorList()
        self.authorList.setStyleSheet('background-color: white')
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(self.authorLabel)
        self.infoLayout.addWidget(self.authorList)

        #botones de consulta y agregar
        self.search = QPushButton("Consultar")
        #self.nuevo = QPushButton("Agregar nuevo autor")
        self.search.setStyleSheet('background-color: PowderBlue')
        #self.nuevo.setStyleSheet('background-color: PowderBlue')
        self.searchLayout = QVBoxLayout()
        self.searchLayout.addLayout(self.infoLayout)
        self.searchLayout.addWidget(self.search)
        #self.searchLayout.addWidget(self.nuevo)

        #Layout final
        self.textLayout = QVBoxLayout()
        self.textLayout.addWidget(self.title)
        self.textLayout.addWidget(self.instrucciones)
        self.textLayout.addStretch()
        self.textLayout.addWidget(self.table)
        self.textLayout.addStretch()
        self.textLayout.addLayout(self.searchLayout)

        self.setLayout(self.textLayout)

        self.search.clicked.connect(self.consulta)

    #Busca los autores registrados en la base de datos y los despliega en el menú
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
        queryText = "SELECT b.title, b.book_id \
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
            self.table.item(i, 0).setText(str(self.query.value(0)))
            self.table.item(i, 1).setText(str(self.query.value(1)))
            i += 1
            #self.table.resizeColumnsToContents()




if __name__ == '__main__':
   app = QApplication(sys.argv)

   estudiante = AuthorSearch()
   estudiante.show()
   sys.exit(app.exec_())