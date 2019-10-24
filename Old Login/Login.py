from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys

class LoginView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(300, 300, 450, 450)
        self.setWindowTitle('CEIC Libros - Log in')

        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaCEIC")
        self.db.setUserName("postgres")
        self.db.setPassword("Tranc0nReloj-7aha")
        self.db.open()

        #Esta es el logo del CEIC
        self.logo = QPixmap('LogoCEIC.png')
        self.logo = self.logo.scaled(250, 250)#, Qt.KeepAspectRatio)
        self.logoLabel = QLabel(self)
        self.logoLabel.setStyleSheet('color: white')
        self.logoLabel.setPixmap(self.logo)
        self.logoLabel.setAlignment(Qt.AlignCenter)
        self.imageLayout = QHBoxLayout()
        self.imageLayout.addWidget(self.logoLabel)

        self.softwareName = QLabel('CEIC Libros')
        self.softwareName.setAlignment(Qt.AlignCenter)

        #Aquí pongo el usuario
        self.userLabel = QLabel('Usuario       ')
        self.username = QLineEdit(self)
        self.userLayout = QHBoxLayout()
        self.userLayout.addWidget(self.userLabel)
        self.userLayout.addWidget(self.username)

        #Aquí pongo lo relacionado con el password
        self.passwordLabel = QLabel('Contraseña')
        self.password = QLineEdit(self)
        self.passwordLayout = QHBoxLayout()
        self.passwordLayout.addWidget(self.passwordLabel)
        self.passwordLayout.addWidget(self.password)

        #Botón de aceptar
        self.accept = QPushButton("Aceptar")

        #Layout de la parte donde el usuario rellena la información
        self.formLayout = QVBoxLayout()
        self.formLayout.addWidget(self.softwareName)
        self.formLayout.addLayout(self.userLayout)
        self.formLayout.addLayout(self.passwordLayout)
        self.formLayout.addWidget(self.accept)

        #Todo en el mismo layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.imageLayout)
        self.layout.addLayout(self.formLayout)

        #Muestro el layout
        self.setLayout(self.layout)

        self.accept.clicked.connect(self.acceptInfo)
        self.username.textChanged[str].connect(self.check_disable) #Avisa cuando algo dentro del recambio cambia
        self.password.textChanged[str].connect(self.check_disable)

    @pyqtSlot()
    def acceptInfo(self):
        inputUsername = self.username.text()
        inputPassword = self.password.text()

        condition = "username = \'" + inputUsername + "\' AND password_ = crypt(\'" + inputPassword + "\', password_);"

        self.query = QSqlQuery()
        self.query.exec_("SELECT permission_mask FROM CEIC_User WHERE " + condition)
        #print("SELECT permission_mask FROM CEIC_User WHERE " + condition)
        if self.query.first():
            if self.query.value(0) == 1:
                print("Es un administrador")
            else:
                print("Solo es un usuario")
        else:
            print("No es nadie")

    @pyqtSlot()
    def check_disable(self):
        if not self.username.text() or not self.password.text():
            self.accept.setEnabled(False)
        else:
            self.accept.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginView()
    form.show()
    sys.exit(app.exec_())

