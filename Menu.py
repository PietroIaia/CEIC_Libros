from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
from gestionEstudiantes import *
from gestionUsuarios import *
from gestionLibros import *
from prestamos import prestamos
from multas import multas
from verificarAutor import verificarAutor
from AgregarLibro import AgregarLibro
from Inventario import Inventario
from AgregarEstudiante import AgregarEstudiante
from AgregarUsuario import AgregarUsuario
from About import About
from Politica import Politica
from Prompt import ErrorPrompt
from sanciones import sanciones
from inicio import Inicio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime 
import smtplib
import ssl

class Ui_MainWindow(object):


    def setupUi(self, main_window, username, perm_mask, app):

        main_window.setObjectName("main_window")
        main_window.setFixedSize(1031, 748)
        main_window.setWindowIcon(QtGui.QIcon("static/icono_CEIC.png"))
        main_window.setStyleSheet("background-color: rgb(235, 235, 235);\n""")


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
        self.setButtonStyleSheet(1, "#6aadc6", "#74b7d0")
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
        self.setButtonStyleSheet(2, "#60a3bc", "#6aadc6")
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
        self.setButtonStyleSheet(3, "#60a3bc", "#6aadc6")
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
        self.setButtonStyleSheet(4, "#5699b2", "#60a3bc")
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
        self.setButtonStyleSheet(5, "#5699b2", "#60a3bc")
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
        self.setButtonStyleSheet(6, "#4c8fa8", "#5699b2")
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
        self.setButtonStyleSheet(7, "#4c8fa8", "#5699b2")
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
        self.setButtonStyleSheet(8, "#42859e", "#4c8fa8")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("static/about-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_8.setIcon(icon6)
        self.push_button_8.setIconSize(QtCore.QSize(45, 45))
        self.push_button_8.setFlat(True)
        self.push_button_8.setObjectName("push_button_8")

        # Button (push_button_9): Gestión de libros
        self.push_button_9 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_9.setGeometry(QtCore.QRect(190, 70, 191, 60))
        self.push_button_9.setFont(font)
        self.push_button_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(9, "#6aadc6", "#74b7d0")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("static/books-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_9.setIcon(icon7)
        self.push_button_9.setIconSize(QtCore.QSize(45, 40))
        self.push_button_9.setFlat(True)
        self.push_button_9.setObjectName("push_button_9")

        # Button (push_button_10): Agregar libro
        self.push_button_10 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_10.setGeometry(QtCore.QRect(190, 130, 191, 60))
        self.push_button_10.setFont(font)
        self.push_button_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(10, "#6aadc6", "#74b7d0")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("static/add-book-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_10.setIcon(icon8)
        self.push_button_10.setIconSize(QtCore.QSize(35, 35))
        self.push_button_10.setFlat(True)
        self.push_button_10.setObjectName("push_button_10")

        # Button (push_button_11): Inventario
        self.push_button_11 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_11.setGeometry(QtCore.QRect(190, 190, 191, 60))
        self.push_button_11.setFont(font)
        self.push_button_11.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(11, "#6aadc6", "#74b7d0")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("static/library-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_11.setIcon(icon9)
        self.push_button_11.setIconSize(QtCore.QSize(40, 40))
        self.push_button_11.setFlat(True)
        self.push_button_11.setObjectName("push_button_11")

        # Button (push_button_12): Gestión de estudiantes
        self.push_button_12 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_12.setGeometry(QtCore.QRect(190, 130, 191, 60))
        self.push_button_12.setFont(font)
        self.push_button_12.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(12, "#60a3bc", "#6aadc6")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("static/students-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_12.setIcon(icon10)
        self.push_button_12.setIconSize(QtCore.QSize(50, 50))
        self.push_button_12.setFlat(True)
        self.push_button_12.setObjectName("push_button_12")

        # Button (push_button_13): Agregar estudiante
        self.push_button_13 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_13.setGeometry(QtCore.QRect(190, 190, 191, 60))
        self.push_button_13.setFont(font)
        self.push_button_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(13, "#5699b2", "#60a3bc")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("static/add-user-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_13.setIcon(icon11)
        self.push_button_13.setIconSize(QtCore.QSize(40, 40))
        self.push_button_13.setFlat(True)
        self.push_button_13.setObjectName("push_button_13")

        # Button (push_button_14): Gestión de usuarios
        self.push_button_14 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_14.setGeometry(QtCore.QRect(190, 370, 191, 60))
        self.push_button_14.setFont(font)
        self.push_button_14.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(14, "#4c8fa8", "#5699b2")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("static/students-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_14.setIcon(icon12)
        self.push_button_14.setIconSize(QtCore.QSize(50, 50))
        self.push_button_14.setFlat(True)
        self.push_button_14.setObjectName("push_button_14")

        # Button (push_button_15): Agregar usuario
        self.push_button_15 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_15.setGeometry(QtCore.QRect(190, 430, 191, 60))
        self.push_button_15.setFont(font)
        self.push_button_15.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setButtonStyleSheet(15, "#42859e", "#4c8fa8")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("static/add-ceic-user-CAD3C8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_15.setIcon(icon13)
        self.push_button_15.setIconSize(QtCore.QSize(32, 32))
        self.push_button_15.setFlat(True)
        self.push_button_15.setObjectName("push_button_15")

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

        # Menú lateral: grid_frame
        self.grid_frame = QtWidgets.QFrame(self.centralwidget)
        self.grid_frame.setGeometry(QtCore.QRect(0, 0, 191, 748))
        self.grid_frame.setAutoFillBackground(False)
        self.grid_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 \
                                      rgba(14, 8, 73, 255), stop:0.0795455 rgba(22, 17, 73, 255), stop:0.409091 \
                                      rgba(22, 45, 97, 255), stop:1 rgba(77, 174, 193, 255));")
        self.grid_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.grid_frame.setObjectName("grid_frame")
        self.grid_layout = QtWidgets.QGridLayout(self.grid_frame)
        self.grid_layout.setObjectName("grid_layout")

        # Menú de libros: verticalFrame_1
        self.verticalFrame_1 = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame_1.setGeometry(QtCore.QRect(180, 60, 201, 201))
        self.verticalFrame_1.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 \
                                            rgba(43, 95, 135, 255), stop:0.727273 rgba(61, 136, 165, 255), stop:0.982955 \
                                            rgba(68, 170, 185, 255));\n"
                                            "border-radius: 10px;")
        self.verticalFrame_1.setObjectName("verticalFrame_1")

        # Menú de estudiantes: verticalFrame_2
        self.verticalFrame_2 = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame_2.setGeometry(QtCore.QRect(180, 120, 201, 141))
        self.verticalFrame_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.107955 \
                                            rgba(43, 95, 135, 255), stop:1 rgba(61, 136, 165, 255)); border-radius: 10px;")
        self.verticalFrame_2.setObjectName("verticalFrame_2")

        # Menú de usuarios: verticalFrame_3 (Administración)
        self.verticalFrame_3 = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame_3.setGeometry(QtCore.QRect(180, 360, 201, 141))
        self.verticalFrame_3.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.210227 \
                                            rgba(20, 39, 90, 255), stop:0.681818 rgba(21, 49, 97, 255), stop:1 \
                                            rgba(23, 76, 115, 255)); border-radius: 10px;")
        self.verticalFrame_3.setObjectName("verticalFrame_3")


        ################# Stacked Widget

        self.generateLog()
        self.sendNotification()

        self.stacked_widget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_widget.setGeometry(QtCore.QRect(190, -1, 841, 724))
        self.stacked_widget.setObjectName("stacked_widget")
        self.stacked_widget.setStyleSheet("background-color: rgb(236, 240, 241)")
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
        # Index : 5
        self.ventana_agregar_libro =  AgregarLibro()
        self.stacked_widget.addWidget(self.ventana_agregar_libro)
        # Index : 6
        self.ventana_inventario = Inventario()
        self.stacked_widget.addWidget(self.ventana_inventario)
        # Index : 7
        self.ventana_author_search = AuthorSearch()
        self.stacked_widget.addWidget(self.ventana_author_search)
        # Index : 8
        self.ventana_agregar_estudiante = AgregarEstudiante()
        self.stacked_widget.addWidget(self.ventana_agregar_estudiante)
        # Index : 9
        self.ventana_agregar_usuario = AgregarUsuario()
        self.stacked_widget.addWidget(self.ventana_agregar_usuario)
        # Index : 10
        self.ventana_agregar_autor = verificarAutor()
        self.stacked_widget.addWidget(self.ventana_agregar_autor)
        # Index : 11
        self.ventana_sanciones = sanciones(username, perm_mask)
        self.stacked_widget.addWidget(self.ventana_sanciones)
        # Index : 12
        self.ventana_inicio = Inicio()
        self.stacked_widget.addWidget(self.ventana_inicio)
        # Index : 13
        self.ventana_about = About()
        self.stacked_widget.addWidget(self.ventana_about)
        # Index : 14
        self.ventana_politica = Politica()
        self.stacked_widget.addWidget(self.ventana_politica)

        # La aplicacion inicia en el Modulod de Inicio
        self.stacked_widget.setCurrentIndex(12)

        # Elementos de la pantalla
        self.stacked_widget.raise_()
        self.verticalFrame_1.raise_()
        self.verticalFrame_2.raise_()
        self.verticalFrame_3.raise_()
        self.grid_frame.raise_()
        self.push_button_1.raise_()
        self.push_button_2.raise_()
        self.push_button_3.raise_()
        self.push_button_4.raise_()
        self.push_button_5.raise_()
        self.push_button_6.raise_()
        self.push_button_7.raise_()
        self.push_button_8.raise_()
        self.push_button_9.raise_()
        self.push_button_10.raise_()
        self.push_button_11.raise_()
        self.push_button_12.raise_()
        self.push_button_13.raise_()
        self.push_button_14.raise_()
        self.push_button_15.raise_()
        self.push_button_22.raise_()

        # Esconder los menú
        self.hide_books_menu()
        self.hide_students_menu()
        self.hide_users_menu()

        main_window.setCentralWidget(self.centralwidget)
        self.retranslateUi(main_window, app)
        QtCore.QMetaObject.connectSlotsByName(main_window)


        ###################### Conexiones de Botones
        self.push_button_2.clicked.connect(self.books_menu)
        self.push_button_3.clicked.connect(self.students_menu)
        self.push_button_7.clicked.connect(self.users_menu)

        self.push_button_9.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.push_button_12.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.push_button_4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.push_button_5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.push_button_14.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.push_button_22.clicked.connect(lambda: sys.exit(app.exec_()))

        self.push_button_10.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.push_button_11.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))
        self.ventana_gestion_libros.author.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))
        self.ventana_author_search.back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.push_button_13.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8))
        self.push_button_15.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))

        self.ventana_agregar_autor.seguir.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ventana_agregar_autor.cancelar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.ventana_agregar_libro.agregarAutor.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(10))
        self.push_button_6.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(11))
        self.ventana_agregar_autor.seguir.clicked.connect(lambda:self.ventana_agregar_libro.authorsInput.clear())
        self.ventana_agregar_autor.seguir.clicked.connect(lambda: self.ventana_agregar_libro.mostrarAutores())
        self.push_button_1.clicked.connect(self.actInicio)
        
        self.push_button_8.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(13))
        self.ventana_about.politica_prestamos.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(14))
        self.ventana_politica.entendido.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(13))

        ##################### Esconde los menú
        for i in range(16):
            if i == 0 or i == 2 or i == 3 or i == 7:
                continue
            button = getattr(self, 'push_button_%s' %i)
            button.clicked.connect(self.hide_books_menu)
            button.clicked.connect(self.hide_students_menu)
            button.clicked.connect(self.hide_users_menu)


        ##################### Permisos
        if(perm_mask == 0):
            self.push_button_7.setEnabled(False)
            self.push_button_7.setStyleSheet("QPushButton\n"
                                            "{\n"
                                            "    color: #B5B5B5\n"
                                            "}")
    
    # Actualiza ventana de inicio
    def actInicio(self):
        self.stacked_widget.setCurrentIndex(12)
        self.ventana_inicio.updateActiveLoanTable()
        self.ventana_inicio.updateDebtTabla()

    # StyleSheet para los botones del menú
    def setButtonStyleSheet(self, button_id, hex1, hex2):
        button = getattr(self, 'push_button_%s' %button_id)
        button.setStyleSheet("QPushButton:hover#push_button_"+str(button_id)+"\n"
                "{\n"
                "    border-radius: 0px;\n"
                "    background-color: " + hex1 + ";\n"
                "    color: #CAD3C8;\n"
                "}\n"
                "\n"
                "QPushButton:pressed#push_button_"+str(button_id)+"\n"
                "{\n"
                "    border-radius: 0px;\n"
                "    background-color: " + hex2 + ";\n"
                "    color: #CAD3C8;\n"
                "}\n"
                "QPushButton\n"
                "{\n"
                "    color: #CAD3C8;\n"
                "}")

    def retranslateUi(self, main_window, app):
        _translate = app.translate
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
        self.push_button_9.setToolTip(_translate("main_window", "Gestión de Libros"))
        self.push_button_9.setText(_translate("main_window", "Gestión de libros"))
        self.push_button_10.setToolTip(_translate("main_window", "Agregar libro"))
        self.push_button_10.setText(_translate("main_window", "    Agregar libro"))
        self.push_button_11.setToolTip(_translate("main_window", "Inventario"))
        self.push_button_11.setText(_translate("main_window", "         Inventario"))
        self.push_button_12.setToolTip(_translate("main_window", "Gestión de estudiantes"))
        self.push_button_12.setText(_translate("main_window", "            Estudiantes"))
        self.push_button_13.setToolTip(_translate("main_window", "Agregar estudiante"))
        self.push_button_13.setText(_translate("main_window", "Agregar estudiante"))
        self.push_button_14.setToolTip(_translate("main_window", "Gestión de usuarios"))
        self.push_button_14.setText(_translate("main_window", "Gestión de usuarios"))
        self.push_button_15.setToolTip(_translate("main_window", "Agregar usuario"))
        self.push_button_15.setText(_translate("main_window", "     Agregar usuario"))
        self.push_button_1.setToolTip(_translate("main_window", "Inicio"))
        self.push_button_1.setText(_translate("main_window", "                Inicio"))
        self.push_button_22.setToolTip(_translate("main_window", "Cerrar Sesión"))
        self.push_button_22.setText(_translate("main_window", "Cerrar Sesión"))

    # Funciones para el menú de libros
    def show_books_menu(self):
        self.verticalFrame_1.show()
        self.push_button_9.show()
        self.push_button_10.show()
        self.push_button_11.show()

    def hide_books_menu(self):
        self.verticalFrame_1.hide()
        self.push_button_9.hide()
        self.push_button_10.hide()
        self.push_button_11.hide()

    def books_menu(self):
        if self.verticalFrame_1.isHidden():
            self.show_books_menu()
        else:
            self.hide_books_menu()

        if self.verticalFrame_2.isHidden() == False:
            self.hide_students_menu()
        if self.verticalFrame_3.isHidden() == False:
            self.hide_users_menu()

    # Funciones para el menú de estudiantes
    def show_students_menu(self):
        self.verticalFrame_2.show()
        self.push_button_12.show()
        self.push_button_13.show()

    def hide_students_menu(self):
        self.verticalFrame_2.hide()
        self.push_button_12.hide()
        self.push_button_13.hide()

    def students_menu(self):
        if self.verticalFrame_2.isHidden():
            self.show_students_menu()
        else:
            self.hide_students_menu()

        if self.verticalFrame_1.isHidden() == False:
            self.hide_books_menu()
        if self.verticalFrame_3.isHidden() == False:
            self.hide_users_menu()

    # Funciones para el menú de usuarios
    def show_users_menu(self):
        self.verticalFrame_3.show()
        self.push_button_14.show()
        self.push_button_15.show()

    def hide_users_menu(self):
        self.verticalFrame_3.hide()
        self.push_button_14.hide()
        self.push_button_15.hide()

    def users_menu(self):
        if self.verticalFrame_3.isHidden():
            self.show_users_menu()
        else:
            self.hide_users_menu()

        if self.verticalFrame_1.isHidden() == False:
            self.hide_books_menu()
        if self.verticalFrame_2.isHidden() == False:
            self.hide_students_menu()

    def generateLog(self):

        orig_stdout = sys.stdout
        with open('Estado.log', 'w') as f:
            sys.stdout = f

            print("------------------------------------")
            print("ESTADO DEL SISTEMA")
            print("------------------------------------")
            print("\n")

            self.queryStudents = QSqlQuery()
            self.queryStudents.exec_("SELECT carnet FROM Loan GROUP BY Carnet")
            if not self.queryStudents.first():
                print("------------------------------------")
                print("No hay préstamos activos")
                print("------------------------------------")
                print("\n")
            else:
                while True:
                    carnet = str(self.queryStudents.value(0))
                    print("------------------------------------")
                    print(carnet)
                    print("------------------------------------")
                    print("\n")

                    print("INFORMACIÓN DEL ESTUDIANTE")
                    self.queryStudentInfo = QSqlQuery()
                    self.queryStudentInfo.exec_("SELECT first_name, last_name, email, phone, days_blocked, book_debt FROM Estudiante WHERE carnet = \'" + carnet + "\'")
                    self.queryStudentInfo.first()
                    print("Nombre: " + str(self.queryStudentInfo.value(0)))
                    print("Apellido: " + str(self.queryStudentInfo.value(1)))
                    print("Email: " + str(self.queryStudentInfo.value(2)))
                    print("Tlf: " + str(self.queryStudentInfo.value(3)))
                    print("Dias de sanción: " + str(self.queryStudentInfo.value(4)))
                    print("Deuda: " + str(self.queryStudentInfo.value(5)) + "\n")

                    print("INFORMACIÓN DEL PRÉSTAMO\n")
                    print("LIBROS\n")
                    self.queryBooksLoaned = QSqlQuery()
                    self.queryBooksLoaned.exec_("SELECT * FROM Loan WHERE carnet = \'" + carnet + "\'")
                    while self.queryBooksLoaned.next():
                        book_id = int(self.queryBooksLoaned.value(1))
                        print("Código del libro: " + str(book_id))
                        print("Código del ejemplar: " + str(self.queryBooksLoaned.value(2)))
                        self.queryBookTitle = QSqlQuery()
                        self.queryBookTitle.exec_("SELECT title FROM Book WHERE book_id = " + str(book_id))
                        self.queryBookTitle.first()
                        print("Título: " + str(self.queryBookTitle.value(0)) + "\n")

                    self.queryBooksLoaned.previous()
                    print("Usuario que lo(s) prestó: " + str(self.queryBooksLoaned.value(3)))
                    auxiliar = QDateTime.toString(self.queryBooksLoaned.value(5)).split()
                    inicio = str(auxiliar[0]+' '+auxiliar[2]+' '+auxiliar[1]+' '+auxiliar[4]+' '+auxiliar[3])
                    print("Fecha de préstamo: " + inicio)
                    auxiliar = QDateTime.toString(self.queryBooksLoaned.value(6)).split()
                    dev_esperada = str(auxiliar[0]+' '+auxiliar[2]+' '+auxiliar[1]+' '+auxiliar[4]+' '+auxiliar[3])
                    print("Fecha esperada de devolución: " + dev_esperada)
                    startTimeAux = QDateTime.toSecsSinceEpoch(self.queryBooksLoaned.value(5))
                    returnTimeAux = QDateTime.toSecsSinceEpoch(self.queryBooksLoaned.value(6))
                    aux = int((int(returnTimeAux) - int(startTimeAux))/86400)
                    print("Dias restantes: " + str(aux))
                    print("\n")

                    if not self.queryStudents.next():
                        break
            
            sys.stdout = orig_stdout
        f.close()

    def sendNotification(self):

        self.queryDay = QSqlQuery()
        self.queryDay.exec_("SELECT last_sent FROM Last_notification")
        self.queryDay.first()
        mailSent = False
        if QDate.currentDate() != self.queryDay.value(0):
            self.queryStudents = QSqlQuery()
            self.queryStudents.exec_("SELECT carnet FROM Loan GROUP BY Carnet")
            if self.queryStudents.first() is None:
                return
            else:
                while True:
                    message = ""
                    carnet = str(self.queryStudents.value(0))
                    self.queryStudentInfo = QSqlQuery()
                    self.queryStudentInfo.exec_("SELECT first_name, last_name, email, days_blocked, book_debt FROM Estudiante WHERE carnet = \'" + carnet + "\'")
                    self.queryStudentInfo.first()
                    if(not self.queryStudentInfo.first()):
                        break
                    message = "Hola " + str(self.queryStudentInfo.value(0)) + " " + str(self.queryStudentInfo.value(1)) + "\n\n"
                    address = str(self.queryStudentInfo.value(2))
                    message += "Se te recuerda que posees un préstamo de libros del CEIC. Estos son: \n\n"

                    self.queryBooksLoaned = QSqlQuery()
                    self.queryBooksLoaned.exec_("SELECT * FROM Loan WHERE carnet = \'" + carnet + "\'")
                    if(self.queryBooksLoaned.first()):
                        while self.queryBooksLoaned.next():
                            book_id = int(self.queryBooksLoaned.value(1))
                            message = message + "Código del libro: " + str(book_id) + "\n"
                            message = message + "Código del ejemplar: " + str(self.queryBooksLoaned.value(2)) + "\n"
                            self.queryBookTitle = QSqlQuery()
                            self.queryBookTitle.exec_("SELECT title FROM Book WHERE book_id = " + str(book_id))
                            self.queryBookTitle.first()
                            message = message + "Título: " + str(self.queryBookTitle.value(0)) + "\n"

                        message += "\n"
                        self.queryBooksLoaned.previous()
                        message = message + "Usuario que lo(s) prestó: " + str(self.queryBooksLoaned.value(3)) + "\n"
                        auxiliar = QDateTime.toString(self.queryBooksLoaned.value(5)).split()
                        inicio = str(auxiliar[0]+' '+auxiliar[2]+' '+auxiliar[1]+' '+auxiliar[4]+' '+auxiliar[3])
                        message = message + "Fecha de préstamo: " + inicio + "\n"
                        auxiliar = QDateTime.toString(self.queryBooksLoaned.value(6)).split()
                        dev_esperada = str(auxiliar[0]+' '+auxiliar[2]+' '+auxiliar[1]+' '+auxiliar[4]+' '+auxiliar[3])
                        message = message + "Fecha esperada de devolución: " + dev_esperada + "\n"

                        message = message + "Dias de sanción: " + str(self.queryStudentInfo.value(3)) + "\n"
                        message = message + "Deuda: " + str(self.queryStudentInfo.value(4)) + "\n"

                        message += "Si estás a un día de la fecha de devolución o en la fecha de devolución, puedes pasar a renovar tu préstamo\n\n"
                        message += "Atentamente,\n"
                        message += "Junta directiva del CEIC"

                        startTimeAux = QDateTime.toSecsSinceEpoch(self.queryBooksLoaned.value(5))
                        returnTimeAux = QDateTime.toSecsSinceEpoch(self.queryBooksLoaned.value(6))
                        aux = int((int(returnTimeAux) - int(startTimeAux))/86400)
                        if aux <= 1:
                            mailSent = True
                            self.emailStudent(address, message)
                        if not self.queryStudents.next():
                            break
        
        if(mailSent):
            self.updateQuery = QSqlQuery()
            self.updateQuery.exec_("UPDATE Last_notification SET last_sent = current_date")

    def emailStudent(self, receiver, text):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "CEICLibrosPrueba@gmail.com" 
        receiver_email = receiver
        password = "the_stepbro"
        msg = MIMEMultipart()
        msg['Subject'] = "Notificación"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        content = text
        content = MIMEText(content)
        msg.attach(content)

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, content.as_string().encode("utf8"))
        except:
            ErrorPrompt("Error", "No se pudo mandar email de notificación. Vuelva a intentar más tarde")
