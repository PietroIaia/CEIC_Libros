from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
from gestionEstudiantes import *
from gestionUsuarios import *
from gestionLibros import *
from prestamos import prestamos
from multas import multas
from Prompt import ErrorPrompt

class Ui_MainWindow(object):

    # Obtenemos el rol del usuario
    global perm_mask
    global username
    global password
    global db

    def setupUi(self, main_window):

        main_window.setObjectName("main_window")
        main_window.resize(1031, 748)
        main_window.setWindowIcon(QtGui.QIcon("static/icono_CEIC.png"))
        main_window.setMinimumSize(QtCore.QSize(1031, 748))
        main_window.setMaximumSize(QtCore.QSize(1031, 748))
        main_window.setStyleSheet("background-color: rgb(235, 235, 235);\n""")

        # Conexion a la base de datos
        self.db = db

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # Font: Para los botones
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        # Button (push_button_1): Inicio
        self.push_button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_1.setGeometry(QtCore.QRect(0, 10, 191, 60))
        self.push_button_1.setFont(font)
        self.push_button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(1, "#646464", "#6E6E6E")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("static/home-page-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_1.setIcon(icon7)
        self.push_button_1.setIconSize(QtCore.QSize(50, 50))
        self.push_button_1.setFlat(True)
        self.push_button_1.setObjectName("push_button_1")
        
        # Button (push_button_2): Gestión de Libros
        self.push_button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_2.setGeometry(QtCore.QRect(0, 70, 191, 60))
        self.push_button_2.setFont(font)
        self.push_button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(2, "#646464", "#6E6E6E")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("static/books-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_2.setIcon(icon)
        self.push_button_2.setIconSize(QtCore.QSize(45, 40))
        self.push_button_2.setFlat(True)
        self.push_button_2.setObjectName("push_button_2")

        # Button (push_button_3): Gestión de Estudiantes
        self.push_button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_3.setGeometry(QtCore.QRect(0, 130, 191, 60))
        self.push_button_3.setFont(font)
        self.push_button_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(3, "#646464", "#6E6E6E")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("static/students-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_3.setIcon(icon1)
        self.push_button_3.setIconSize(QtCore.QSize(50, 50))
        self.push_button_3.setFlat(True)
        self.push_button_3.setObjectName("push_button_3")

        # Button (push_button_4): Préstamos
        self.push_button_4 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_4.setGeometry(QtCore.QRect(0, 190, 191, 60))
        self.push_button_4.setFont(font)
        self.push_button_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(4, "#646464", "#6E6E6E")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("static/préstamos-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_4.setIcon(icon2)
        self.push_button_4.setIconSize(QtCore.QSize(45, 45))
        self.push_button_4.setFlat(True)
        self.push_button_4.setObjectName("push_button_4")

        # Button (push_button_5): Multas
        self.push_button_5 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_5.setGeometry(QtCore.QRect(0, 250, 191, 60))
        self.push_button_5.setFont(font)
        self.push_button_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(5, "#646464", "#6E6E6E")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("static/fines-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_5.setIcon(icon3)
        self.push_button_5.setIconSize(QtCore.QSize(50, 50))
        self.push_button_5.setFlat(True)
        self.push_button_5.setObjectName("push_button_5")

        # Button (push_button_6): Sanciones
        self.push_button_6 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_6.setGeometry(QtCore.QRect(0, 310, 191, 60))
        self.push_button_6.setFont(font)
        self.push_button_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(6, "#646464", "#6E6E6E")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("static/banned-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_6.setIcon(icon4)
        self.push_button_6.setIconSize(QtCore.QSize(45, 45))
        self.push_button_6.setFlat(True)
        self.push_button_6.setObjectName("push_button_6")

        # Button (push_button_7): Administracion
        self.push_button_7 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_7.setGeometry(QtCore.QRect(0, 370, 191, 60))
        self.push_button_7.setFont(font)
        self.push_button_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(7, "#646464", "#6E6E6E")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("static/admin-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_7.setIcon(icon5)
        self.push_button_7.setIconSize(QtCore.QSize(40, 40))
        self.push_button_7.setFlat(True)
        self.push_button_7.setObjectName("push_button_7")

        # Button (push_button_8): About
        self.push_button_8 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_8.setGeometry(QtCore.QRect(0, 430, 191, 60))
        self.push_button_8.setFont(font)
        self.push_button_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(8, "#646464", "#6E6E6E")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("static/about-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_8.setIcon(icon6)
        self.push_button_8.setIconSize(QtCore.QSize(45, 45))
        self.push_button_8.setFlat(True)
        self.push_button_8.setObjectName("push_button_8")

        # Button (push_button_22): Cerrar sesión
        self.push_button_22 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_22.setGeometry(QtCore.QRect(0, 672, 191, 51))
        self.push_button_22.setFont(font)
        self.push_button_22.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.push_button_22.setAutoFillBackground(False)
        self.push_button_22.setStyleSheet("QPushButton:hover#push_button_22\n"
                                         "{\n"
                                         "    border-radius: 0px;\n"
                                         "    background-color: #C20000;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:pressed#push_button_22\n"
                                         "{\n"
                                         "    border-radius: 0px;\n"
                                         "    background-color: #C20000;\n"    
                                         "}\n"
                                         "\n"
                                         "QPushButton\n"
                                         "{\n"
                                         "    border-radius: 0px;\n"
                                         "    background-color: #F10000;\n"
                                         "    color: #FFFFFF;             "
                                         "}")
        self.push_button_22.setFlat(True)
        self.push_button_22.setObjectName("push_button_22")

        # Menu lateral: grid_frame
        self.grid_frame = QtWidgets.QFrame(self.centralwidget)
        self.grid_frame.setGeometry(QtCore.QRect(0, 0, 191, 748))
        self.grid_frame.setAutoFillBackground(False)
        self.grid_frame.setStyleSheet("background-color: #FFFFFF")
        self.grid_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.grid_frame.setObjectName("grid_frame")
        self.grid_layout = QtWidgets.QGridLayout(self.grid_frame)
        self.grid_layout.setObjectName("grid_layout")

        ################# Stacked Widget

        self.stacked_widget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_widget.setGeometry(QtCore.QRect(190, -1, 841, 724))
        self.stacked_widget.setObjectName("stacked_widget")
        self.stacked_widget.setStyleSheet("background-color: LightSkyBlue")
        # Index: 0
        self.ventana_gestion_libros = gestionLibros(perm_mask)
        self.stacked_widget.addWidget(self.ventana_gestion_libros)
        # Index: 1
        self.ventana_gestion_estudiante = gestionEstudiante(perm_mask)
        self.stacked_widget.addWidget(self.ventana_gestion_estudiante)
        # Index: 2
        self.ventana_gestion_usuarios = gestionUsuarios(username)
        self.stacked_widget.addWidget(self.ventana_gestion_usuarios)
        # Index: 3
        self.ventana_prestamos = prestamos(username)
        self.stacked_widget.addWidget(self.ventana_prestamos)
        # Index : 4
        self.ventana_multas = multas(username, perm_mask)
        self.stacked_widget.addWidget(self.ventana_multas)

        # Elementos de la pantalla
        self.grid_frame.raise_()
        self.push_button_1.raise_()
        self.push_button_2.raise_()
        self.push_button_3.raise_()
        self.push_button_4.raise_()
        self.push_button_5.raise_()
        self.push_button_6.raise_()
        self.push_button_7.raise_()
        self.push_button_8.raise_()
        self.push_button_22.raise_()
        self.stacked_widget.raise_()

        main_window.setCentralWidget(self.centralwidget)
        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)


        ###################### Conexiones de Botones
        self.push_button_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.push_button_3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.push_button_4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.push_button_5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.push_button_7.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.push_button_22.clicked.connect(lambda: sys.exit(app.exec_()))

        ##################### Permisos
        if(perm_mask == 0):
            self.push_button_7.setEnabled(False)
            self.push_button_7.setStyleSheet("QPushButton\n"
                                            "{\n"
                                            "    color: #B5B5B5\n"
                                            "}")

    def setButtonStyleSheet(self, button_id, hex1, hex2):
        button = getattr(self, 'push_button_%s' %button_id)
        button.setStyleSheet("QPushButton:hover#push_button_"+str(button_id)+"\n"
                "{\n"
                "    border-radius: 0px;\n"
                "    background-color: " + hex1 + ";\n"
                "    color: #E9F2E6;\n"
                "}\n"
                "\n"
                "QPushButton:pressed#push_button_"+str(button_id)+"\n"
                "{\n"
                "    border-radius: 0px;\n"
                "    background-color: " + hex2 + ";\n"
                "    color: #E9F2E6;\n"
                "}\n"
                "QPushButton\n"
                "{\n"
                "    color: #666666;\n"
                "}")

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "CEIC Libros"))
        self.push_button_2.setToolTip(_translate("main_window", "<html><head/><body><p>Libros</p></body></html>"))
        self.push_button_2.setText(_translate("main_window", "            Libros"))
        self.push_button_3.setToolTip(_translate("main_window", "<html><head/><body><p>Estudiantes</p></body></html>"))
        self.push_button_3.setText(_translate("main_window", "   Estudiantes"))
        self.push_button_4.setToolTip(_translate("main_window", "Préstamos"))
        self.push_button_4.setText(_translate("main_window", "     Préstamos"))
        self.push_button_5.setToolTip(_translate("main_window", "Multas"))
        self.push_button_5.setText(_translate("main_window", "           Multas"))
        self.push_button_6.setToolTip(_translate("main_window", "Sanciones"))
        self.push_button_6.setText(_translate("main_window", "        Sanciones"))
        self.push_button_7.setToolTip(_translate("main_window", "Administración"))
        self.push_button_7.setText(_translate("main_window", "Administración"))
        self.push_button_8.setToolTip(_translate("main_window", "About"))
        self.push_button_8.setText(_translate("main_window", "             About"))
        self.push_button_1.setToolTip(_translate("main_window", "Inicio"))
        self.push_button_1.setText(_translate("main_window", "                Inicio"))
        self.push_button_22.setToolTip(_translate("main_window", "Cerrar Sesión"))
        self.push_button_22.setText(_translate("main_window", "Cerrar Sesión"))

if __name__ == '__main__':

    # Base de datos
    db = QSqlDatabase.addDatabase("QPSQL")
    db.setHostName("localhost")
    db.setDatabaseName("pruebaceic")                         
    db.setUserName("postgres")
    db.setPassword("postgres")                 # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
    db.open()

    # Verificacion de que se han pasado los parámetros de entrada
    if len(sys.argv) < 3:
        sys.exit()
    
    # Datos del usuario
    username = str(sys.argv[1])
    password = str(sys.argv[2])

    # Creación de la aplicación
    app = QtWidgets.QApplication([])

    # Se chequea que el 'username' del usuario coincide con el 'password'
    condition = "username = \'" + username + "\' AND password_ = crypt(\'" + password + "\', password_);"
    query = QSqlQuery()
    query.exec_("SELECT username, permission_mask FROM CEIC_User WHERE " + condition)

    if query.first():
        if query.value(1) == 1:
            perm_mask = 1   # El usuario existe, es administrador
        else:
            perm_mask = 0   # El usuario existe, es usuario regular
    else:
        ErrorPrompt("Error de Login", "Nombre de usuario o contraseña incorrectos!")
        sys.exit()

    # Inicializamos la main_window
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())