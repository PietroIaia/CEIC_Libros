from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from gestionEstudiantes import *
from gestionUsuarios import *
from gestionLibros import *
from prestamos import prestamos
from multas import multas


class Ui_MainWindow(object):

    # Obtenemos el rol del usuario
    global perm_mask
    global username

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 748)
        MainWindow.setWindowIcon(QtGui.QIcon("static/icono_CEIC.png"))
        MainWindow.setMinimumSize(QtCore.QSize(1031, 748))
        MainWindow.setMaximumSize(QtCore.QSize(1031, 748))
        MainWindow.setStyleSheet("background-color: rgb(235, 235, 235);\n""")

        # Conexion a la base de datos
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pruebaceic")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")                                # RECUERDEN CAMBIAR CONTRASEÑA DEPENDIENDO DE LA SUYA!
        self.db.open()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Font: Para los botones
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        # Button (pushButton_1): Inicio
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(0, 10, 191, 60))
        self.pushButton_1.setFont(font)
        self.pushButton_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(1, "#646464", "#6E6E6E")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("static/home-page-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_1.setIcon(icon7)
        self.pushButton_1.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_1.setFlat(True)
        self.pushButton_1.setObjectName("pushButton_1")
        
        # Button (pushButton_2): Gestión de Libros
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 70, 191, 60))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(2, "#646464", "#6E6E6E")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("static/books-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(45, 40))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")

        # Button (pushButton_3): Gestión de Estudiantes
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 130, 191, 60))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(3, "#646464", "#6E6E6E")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("static/students-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")

        # Button (pushButton_4): Préstamos
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 190, 191, 60))
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(4, "#646464", "#6E6E6E")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("static/préstamos-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon2)
        self.pushButton_4.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")

        # Button (pushButton_5): Multas
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 250, 191, 60))
        self.pushButton_5.setFont(font)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(5, "#646464", "#6E6E6E")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("static/fines-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon3)
        self.pushButton_5.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")

        # Button (pushButton_6): Sanciones
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(0, 310, 191, 60))
        self.pushButton_6.setFont(font)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(6, "#646464", "#6E6E6E")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("static/banned-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon4)
        self.pushButton_6.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_6.setFlat(True)
        self.pushButton_6.setObjectName("pushButton_6")

        # Button (pushButton_7): Administracion
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(0, 370, 191, 60))
        self.pushButton_7.setFont(font)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(7, "#646464", "#6E6E6E")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("static/admin-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon5)
        self.pushButton_7.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_7.setFlat(True)
        self.pushButton_7.setObjectName("pushButton_7")

        # Button (pushButton_8): About
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(0, 430, 191, 60))
        self.pushButton_8.setFont(font)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(8, "#646464", "#6E6E6E")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("static/about-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon6)
        self.pushButton_8.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_8.setFlat(True)
        self.pushButton_8.setObjectName("pushButton_8")

        # Button (pushButton_22): Cerrar sesión
        self.pushButton_22 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_22.setGeometry(QtCore.QRect(0, 672, 191, 51))
        self.pushButton_22.setFont(font)
        self.pushButton_22.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_22.setAutoFillBackground(False)
        self.pushButton_22.setStyleSheet("QPushButton:hover#pushButton_22\n"
                                         "{\n"
                                         "    border-radius: 0px;\n"
                                         "    background-color: #C20000;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:pressed#pushButton_22\n"
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
        self.pushButton_22.setFlat(True)
        self.pushButton_22.setObjectName("pushButton_22")

        # Menu lateral: gridFrame
        self.gridFrame = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame.setGeometry(QtCore.QRect(0, 0, 191, 748))
        self.gridFrame.setAutoFillBackground(False)
        self.gridFrame.setStyleSheet("background-color: #FFFFFF")
        self.gridFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout.setObjectName("gridLayout")

        ################# Stacked Widget

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(190, -1, 841, 724))
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setStyleSheet("background-color: LightSkyBlue")
        # Index: 0
        self.ventana_gestion_libros = gestionLibros(perm_mask)
        self.stackedWidget.addWidget(self.ventana_gestion_libros)
        # Index: 1
        self.ventana_gestion_estudiante = gestionEstudiante(perm_mask)
        self.stackedWidget.addWidget(self.ventana_gestion_estudiante)
        # Index: 2
        self.ventana_gestion_usuarios = gestionUsuarios(username)
        self.stackedWidget.addWidget(self.ventana_gestion_usuarios)
        # Index: 3
        self.ventana_prestamos = prestamos(username)
        self.stackedWidget.addWidget(self.ventana_prestamos)
        # Index : 4
        self.ventana_multas = multas(username, perm_mask)
        self.stackedWidget.addWidget(self.ventana_multas)

        # Elementos de la pantalla
        self.gridFrame.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_7.raise_()
        self.pushButton_8.raise_()
        self.pushButton_22.raise_()
        self.stackedWidget.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        ###################### Conexiones de Botones
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButton_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_22.clicked.connect(lambda: sys.exit(app.exec_()))

        ##################### Permisos
        if(perm_mask == 0):
            self.pushButton_7.setEnabled(False)
            self.pushButton_7.setStyleSheet("QPushButton\n"
                                            "{\n"
                                            "    color: #B5B5B5\n"
                                            "}")

    def setButtonStyleSheet(self, buttonId, hex1, hex2):
        button = getattr(self, 'pushButton_%s' %buttonId)
        button.setStyleSheet("QPushButton:hover#pushButton_"+str(buttonId)+"\n"
                "{\n"
                "    border-radius: 0px;\n"
                "    background-color: " + hex1 + ";\n"
                "    color: #E9F2E6;\n"
                "}\n"
                "\n"
                "QPushButton:pressed#pushButton_"+str(buttonId)+"\n"
                "{\n"
                "    border-radius: 0px;\n"
                "    background-color: " + hex2 + ";\n"
                "    color: #E9F2E6;\n"
                "}\n"
                "QPushButton\n"
                "{\n"
                "    color: #666666;\n"
                "}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CEIC Libros"))
        self.pushButton_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Libros</p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "            Libros"))
        self.pushButton_3.setToolTip(_translate("MainWindow", "<html><head/><body><p>Estudiantes</p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "   Estudiantes"))
        self.pushButton_4.setToolTip(_translate("MainWindow", "Préstamos"))
        self.pushButton_4.setText(_translate("MainWindow", "     Préstamos"))
        self.pushButton_5.setToolTip(_translate("MainWindow", "Multas"))
        self.pushButton_5.setText(_translate("MainWindow", "           Multas"))
        self.pushButton_6.setToolTip(_translate("MainWindow", "Sanciones"))
        self.pushButton_6.setText(_translate("MainWindow", "        Sanciones"))
        self.pushButton_7.setToolTip(_translate("MainWindow", "Administración"))
        self.pushButton_7.setText(_translate("MainWindow", "Administración"))
        self.pushButton_8.setToolTip(_translate("MainWindow", "About"))
        self.pushButton_8.setText(_translate("MainWindow", "             About"))
        self.pushButton_1.setToolTip(_translate("MainWindow", "Inicio"))
        self.pushButton_1.setText(_translate("MainWindow", "                Inicio"))
        self.pushButton_22.setToolTip(_translate("MainWindow", "Cerrar Sesión"))
        self.pushButton_22.setText(_translate("MainWindow", "Cerrar Sesión"))

if __name__ == '__main__':
    # Este será el rol del usuario
    perm_mask = int(sys.argv[2])
    username = str(sys.argv[1])
    
    # Inicializamos la MainWindow
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())