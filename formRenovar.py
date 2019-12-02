from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QFrame, QLabel, QComboBox, QLineEdit, QPushButton, QWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime
from Prompt import ErrorPrompt, InfoPrompt
import sys
import os

class form_renovar(QWidget):

    def __init__(self, username, codigo):
        # Inicialización de la ventana
        super().__init__()
        self.setWindowTitle("Renovar Contraseña")
        self.setWindowIcon(QIcon("static/icono_CEIC.png"))
        self.setStyleSheet('background-color: rgb(236, 240, 241)')
        self.setFixedSize(380, 220)

        paleta = QPalette()
        paleta.setColor(QPalette.Background, QColor(243, 243, 243))
        self.setPalette(paleta)

        self.fuente = QFont()
        self.fuente.setPointSize(10)
        self.fuente.setFamily("Bahnschrift Light")

        self.fuenteCode = QFont()
        self.fuenteCode.setPointSize(15)
        self.fuenteCode.setFamily("Bahnschrift Light")

        self.labelInfo = QLabel("Se envió un codigo de verificación al correo\n              de la cuenta del Usuario\n", self)
        self.labelInfo.move(25, 40)
        self.labelInfo.setFont(self.fuente)
        self.labelInfo.setStyleSheet("text-align: justify; color: #575757;")

        self.code = QLineEdit(self)
        self.code.setFrame(False)
        self.code.setTextMargins(8, 0, 4, 1)
        self.code.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.code.setFixedWidth(238)
        self.code.setFixedHeight(50)
        self.code.move(72, 120)
        self.code.setFont(self.fuenteCode)

        self.repeat_password = QLineEdit(self)
        self.repeat_password.setFrame(False)
        self.repeat_password.setTextMargins(8, 0, 4, 1)
        self.repeat_password.setStyleSheet("QLineEdit\n{\n border: 1px solid #C9C9C9;\n border-radius: 3px;\n background-color: white;\n}")
        self.repeat_password.setFixedWidth(238)
        self.repeat_password.setFixedHeight(40)
        self.repeat_password.setPlaceholderText("Repetir Contraseña")
        self.repeat_password.move(72, 300)
        self.repeat_password.setFont(self.fuenteCode)

        # Conexion
        self.code.returnPressed.connect(lambda: self.changePasswordForm(username, codigo))


    # Funcion para mostrar form de cambio de contraseña
    def changePasswordForm(self, username, codigo):

        if(self.code.text() != codigo):
            ErrorPrompt("Error", "Código Erroneo!")
            return
            
        self.labelInfo.setText("Ingrese la Nueva Contraseña")
        self.labelInfo.move(77, 20)

        self.code.setText("")
        self.code.setPlaceholderText("Nueva Contraseña")
        self.code.setEchoMode(QLineEdit.Password)
        self.code.setFixedHeight(40)
        self.code.move(72, 90)

        self.repeat_password.setText("")
        self.repeat_password.setPlaceholderText("Repetir Contraseña")
        self.repeat_password.setEchoMode(QLineEdit.Password)
        self.repeat_password.setFixedHeight(40)
        self.repeat_password.move(72, 140)

        # Conexion
        self.code.returnPressed.connect(lambda: self.changePassword(username))
        self.repeat_password.returnPressed.connect(lambda: self.changePassword(username))


    # Funcion para cambiar la password del usuario
    def changePassword(self, username):

        if(self.code.text() != self.repeat_password.text()):
            ErrorPrompt("Error", "Las contraseñas no coinciden!")
            return

        self.query = QSqlQuery()
        success = self.query.exec_("UPDATE CEIC_User SET password_ = crypt('"+ str(self.code.text()) + "', gen_salt('bf', 8)) WHERE username = '" + username + "';")

        if(success):
            InfoPrompt("Success", "La contraseña ha sido modificada!")
        else:
            ErrorPrompt("Error", "Error Desconocido")
        self.close()

