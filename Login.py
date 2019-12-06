from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime
from Prompt import ErrorPrompt
from Menu import Ui_MainWindow
from formRenovar import form_renovar
from passlib.hash import bcrypt
import random
import string
import sys
import os


# ===================== CLASE ventanaLogin =========================

class ventanaLogin(QMainWindow):
    def __init__(self, parent=None):
        super(ventanaLogin, self).__init__(parent)
        
        self.setWindowTitle("CEIC Libros")
        self.setWindowIcon(QIcon("static/icono_CEIC.png"))
        self.setIconSize(QSize(200,200))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(400, 320)

        paleta = QPalette()
        paleta.setColor(QPalette.Background, QColor(243, 243, 243))
        self.setPalette(paleta)

        self.fuente = QFont()
        self.fuente.setPointSize(10)
        self.fuente.setFamily("Bahnschrift Light")

        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")                         
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")                               # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
        self.db.open()

        self.initUI()

    def initUI(self):

      # ==================== FRAME ENCABEZADO ====================

        paleta = QPalette()
        paleta.setColor(QPalette.Background, QColor(70,130,180))

        frame = QFrame(self)
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setAutoFillBackground(True)
        frame.setPalette(paleta)
        frame.setFixedWidth(400)
        frame.setFixedHeight(84)
        frame.move(0, 0)

        labelIcono = QLabel(frame)
        labelIcono.setFixedWidth(110)
        labelIcono.setFixedHeight(90)
        labelIcono.setPixmap(QPixmap("static/icono_CEIC.png").scaled(110, 90, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
        labelIcono.move(65, -6)

        fuenteTitulo = QFont()
        fuenteTitulo.setPointSize(30)
        fuenteTitulo.setBold(True)

        labelTitulo = QLabel("<font color='Black'>Libros</font>", frame)
        labelTitulo.setFont(fuenteTitulo)
        labelTitulo.move(185, 16)

      # ===================== WIDGETS LOGIN ======================

        labelUsuario = QLabel("Usuario", self)
        labelUsuario.move(60, 120)
        labelUsuario.setFont(self.fuente)

        frameUsuario = QFrame(self)
        frameUsuario.setFrameShape(QFrame.StyledPanel)
        frameUsuario.setFixedWidth(280)
        frameUsuario.setFixedHeight(28)
        frameUsuario.move(60, 146)

        imagenUsuario = QLabel(frameUsuario)
        imagenUsuario.setPixmap(QPixmap("static/usuario.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagenUsuario.move(10, 4)

        self.username = QLineEdit(frameUsuario)
        self.username.setFrame(False)
        self.username.setTextMargins(8, 0, 4, 1)
        self.username.setFixedWidth(238)
        self.username.setFixedHeight(26)
        self.username.move(40, 1)
        self.username.setFont(self.fuente)

        # ========================================================

        labelContrasenia = QLabel("Contraseña", self)
        labelContrasenia.move(60, 174)
        labelContrasenia.setFont(self.fuente)

        frameContrasenia = QFrame(self)
        frameContrasenia.setFrameShape(QFrame.StyledPanel)
        frameContrasenia.setFixedWidth(280)
        frameContrasenia.setFixedHeight(28)
        frameContrasenia.move(60, 200)

        imagenContrasenia = QLabel(frameContrasenia)
        imagenContrasenia.setPixmap(QPixmap("static/contraseña.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagenContrasenia.move(10, 4)

        self.password = QLineEdit(frameContrasenia)
        self.password.setFrame(False)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setTextMargins(8, 0, 4, 1)
        self.password.setFixedWidth(238)
        self.password.setFixedHeight(26)
        self.password.move(40, 1)
        self.password.setFont(self.fuente)

        self.renovar_password = QPushButton("¿Olvidaste tu contraseña?" , self)
        self.renovar_password.setFixedWidth(200)
        self.renovar_password.setStyleSheet("QPushButton {border: 0px; background-color: rgb(243, 243, 243); color: blue; font-size: 15px;}\n"
        "QPushButton:hover {color: #00008B}")
        self.renovar_password.move(105, 230)

      # ================== WIDGETS QPUSHBUTTON ===================

        buttonLogin = QPushButton("Iniciar sesión", self)
        buttonLogin.setFixedWidth(135)
        buttonLogin.setFixedHeight(28)
        buttonLogin.move(60, 270)
        buttonLogin.setFont(self.fuente)

        buttonCancelar = QPushButton("Cancelar", self)
        buttonCancelar.setFixedWidth(135)
        buttonCancelar.setFixedHeight(28)
        buttonCancelar.move(205, 270)
        buttonCancelar.setFont(self.fuente)

      # ==================== SEÑALES BOTONES =====================

        buttonLogin.clicked.connect(self.Login)
        buttonCancelar.clicked.connect(self.close)
        self.renovar_password.clicked.connect(self.renovarPassword)

  # ======================= FUNCIONES ============================

    def Login(self):
        inputUsername = self.username.text()
        inputPassword = self.password.text()
        perm_mask = -1

        self.query = QSqlQuery()
        # Obtenemos el rol del usuario
        self.query.exec_("SELECT permission_mask, password_ FROM CEIC_User WHERE username='" + inputUsername + "';")

        if (self.query.first()):
          # SI SE REINICIA LA BASE DE DATOS COMENTAR LAS 3 LINEAS SIGUIENTES PARA QUE DEJE INGRESAR EN SISTEMA Y AGREGAR UN USUARIO ADMINISTRADOR
          if(not bcrypt.verify(inputPassword, self.query.value(1))):
            ErrorPrompt("Error de Login", "Nombre de usuario o contraseña incorrectos!")
            return


          perm_mask = self.query.value(0)
          # Hace update del last_login del user
          update_last_login = "UPDATE CEIC_User SET last_login='"+str(datetime.now())+"' WHERE username='"+inputUsername+"';"
          self.query.exec_(update_last_login)

          # Cerramos el Login
          self.close()

          # Abrimos el MainWindow
          # Inicializamos la main_window
          self.main_window = QMainWindow()
          self.ui = Ui_MainWindow()
          self.ui.setupUi(self.main_window, str(inputUsername), int(1), aplicacion)
          self.main_window.show()

        else:
            ErrorPrompt("Error", "Nombre de usuario o contraseña incorrectos!")
    

    # Funcion utilizada para llamar al form de Renovacion de contraseña
    def renovarPassword(self):

      self.query = QSqlQuery()
      self.query.exec_("SELECT email FROM CEIC_User WHERE username = '" + self.username.text() + "';")
      if(not self.query.first()):
        ErrorPrompt("Error", "No existe ese Nombre de usuario!")
        return

      # Enviamos el codigo
      # code = ''.join(choices(string.ascii_uppercase + string.digits, k=13))
      code = "bc1hjk57899il"
      with open("RenovarContraseña.log", "a") as f:
          f.write(str(self.query.value(0)) + " | " + code + "\n")
      f.close()

      # Mostramos el form
      self.form = form_renovar(self.username.text(), code)
      self.form.show()


# ================================================================

if __name__ == '__main__':
    
    aplicacion = QApplication(sys.argv)
    
    ventana = ventanaLogin()
    ventana.show()
    
    sys.exit(aplicacion.exec_())