#CEIC Libros
#Ventana para agregar usuarios
#Desarrollado por Forward

# Importamos las librerias a utilizar
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from validationFunctionsUsuarios import verification
from Prompt import InfoPrompt, ErrorPrompt
import sys
import datetime 

class AgregarUsuario(QWidget):

    def __init__(self):
        #Inicialización de la ventana
        super().__init__()
        self.setGeometry(200, 100, 600, 500)
        self.setMinimumSize(QSize(600, 500))
        self.setMaximumSize(QSize(600, 500))
        self.setWindowTitle("Gestión de usuarios")
        self.setStyleSheet('background-color: LightSkyBlue')

        #Base de datos
        self.db = QSqlDatabase.database('qt_sql_default_connection')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")                                          # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
        self.db.open()

        #Creación de fonts para las letras
        self.titleFont = QFont("Serif", 20)

        #Título
        self.title = QLabel("Agregar nuevo usuario")
        self.title.setStyleSheet('color: white')
        self.title.setFont(self.titleFont)

        #Aquí vienen los campos
        self.userLabel = QLabel("Nombre de usuario")
        self.userInput = QLineEdit(self)
        self.contraseñaLabel = QLabel("Contraseña")
        self.contraseñaInput = QLineEdit(self)
        self.nombreLabel = QLabel("Nombre")
        self.nombreInput = QLineEdit(self)
        self.apellidoLabel = QLabel("Apellido")
        self.apellidoInput = QLineEdit(self)
        self.emailLabel = QLabel("Correo electronico")
        self.emailInput = QLineEdit(self)
        self.permisosLabel = QLabel("Permisos")
        self.permisosInput = QSpinBox(self)

        #CSS
        self.userInput.setStyleSheet('background-color: white')
        self.contraseñaInput.setStyleSheet('background-color: white')
        self.nombreInput.setStyleSheet('background-color: white')
        self.apellidoInput.setStyleSheet('background-color: white')
        self.emailInput.setStyleSheet('background-color: white')
        self.permisosInput.setStyleSheet('background-color: white')

        #Botones
        self.agregar = QPushButton("Agregar")
        self.cancelar = QPushButton("Cancelar")

        #LAyout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.userLabel)
        self.layout.addWidget(self.userInput)
        self.layout.addWidget(self.contraseñaLabel)
        self.layout.addWidget(self.contraseñaInput)
        self.layout.addWidget(self.nombreLabel)
        self.layout.addWidget(self.nombreInput)
        self.layout.addWidget(self.apellidoLabel)
        self.layout.addWidget(self.apellidoInput)
        self.layout.addWidget(self.emailLabel)
        self.layout.addWidget(self.emailInput)
        self.layout.addWidget(self.permisosLabel)
        self.layout.addWidget(self.permisosInput)
        self.layout.addWidget(self.agregar)
        self.layout.addWidget(self.cancelar)

        self.setLayout(self.layout)

        self.agregar.clicked.connect(self.agregarUsuario)
        self.cancelar.clicked.connect(self.closeWindow)


    @pyqtSlot()
    def agregarUsuario(self):
        fields = [self.userInput.text(), self.contraseñaInput.text(), self.nombreInput.text(), self.apellidoInput.text(),\
            self.emailInput.text(), self.permisosInput.text()]

        correct = verification(fields, 6)

        if not correct:
            return

        ultima_conexion = str(datetime.datetime.now())
        fecha_de_creacion = str(datetime.datetime.now())

        puede = 1
        queryText2 = "SELECT * FROM CEIC_User WHERE username = '" + fields[0] + "';"
        self.query2 = QSqlQuery()
        self.query2.exec_(queryText2)

        if self.query2.first():
            puede = 0;

        if puede == 1:
            self.query = QSqlQuery()
            self.query.prepare("INSERT INTO CEIC_User (username, password_, first_name, last_name, email, permission_mask, last_login, creation_date) VALUES(:username, crypt(:password, gen_salt('bf', 8)), \
                :fname, :lname, :email, :permisos, :last_login, :creation_date ) RETURNING username")
            self.query.bindValue(0, fields[0])
            self.query.bindValue(1, fields[1])
            self.query.bindValue(2, fields[2])
            self.query.bindValue(3, fields[3])
            self.query.bindValue(4, fields[4])
            self.query.bindValue(5, fields[5])
            self.query.bindValue(":last_login", ultima_conexion)
            self.query.bindValue(":creation_date", fecha_de_creacion)

            self.query.exec_()

            if self.query.first():
                InfoPrompt("Éxito", "La información del usuario ha sido agregada exitosamente")
                self.close()
            else:
                ErrorPrompt("Fracaso", "El usuario no fue agregado al sistema")
        else:
            ErrorPrompt("Error", "El nombre de usuario coincide con uno ya existente, por favor ingrese otro nombre")

    @pyqtSlot()
    def closeWindow(self):
        self.close()




#if __name__ == '__main__':
#    app = QApplication(sys.argv)

#    form = AgregarEstudiante()
#    form.show()
#    sys.exit(app.exec_())