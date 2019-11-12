from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime
from Prompt import ErrorPrompt
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

        # ========================================================

        labelContrasenia = QLabel("Contraseña", self)
        labelContrasenia.move(60, 174)

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

      # ================== WIDGETS QPUSHBUTTON ===================

        buttonLogin = QPushButton("Iniciar sesión", self)
        buttonLogin.setFixedWidth(135)
        buttonLogin.setFixedHeight(28)
        buttonLogin.move(60, 256)

        buttonCancelar = QPushButton("Cancelar", self)
        buttonCancelar.setFixedWidth(135)
        buttonCancelar.setFixedHeight(28)
        buttonCancelar.move(205, 256)

      # ==================== SEÑALES BOTONES =====================

        buttonLogin.clicked.connect(self.Login)
        buttonCancelar.clicked.connect(self.close)

  # ======================= FUNCIONES ============================

    def Login(self):
        inputUsername = self.username.text()
        inputPassword = self.password.text()
        perm_mask = -1

        condition = "username = \'" + inputUsername + "\' AND password_ = crypt(\'" + inputPassword + "\', password_);"

        self.query = QSqlQuery()
        # Obtenemos el rol del usuario
        self.query.exec_("SELECT permission_mask FROM CEIC_User WHERE " + condition)

        if self.query.first():
            # Si es Admin
            if self.query.value(0) == 1:
                perm_mask = 1
            # Si es User
            else:
                perm_mask = 0

            # Hace update del last_login del user
            update_last_login = "UPDATE CEIC_User SET last_login='"+str(datetime.now())+"' WHERE username='"+inputUsername+"';"
            self.query.exec_(update_last_login)

            # Cerramos el Login
            self.close()
            # Abrimos el MainWindow
            os.system("py Menu.py " + str(inputUsername) + " " + str(perm_mask))

        else:
            ErrorPrompt("Error de Login", "Nombre de usuario o contraseña incorrectos!")


# ================================================================

if __name__ == '__main__':
    
    aplicacion = QApplication(sys.argv)

    fuente = QFont()
    fuente.setPointSize(10)
    fuente.setFamily("Bahnschrift Light")

    aplicacion.setFont(fuente)
    
    ventana = ventanaLogin()
    ventana.show()
    
    sys.exit(aplicacion.exec_())