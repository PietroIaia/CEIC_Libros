#CEIC Libros
#Tabla de estudiantes
#Desarrollado por Forward
##Responsable del módulo: Diego Peña, 15-11095
#Fecha de inicio: 21-10-19, Apróx 9:00 am, Hora de Venezuela
#Última modifcación: 21-10-19, 22:00, Hora de Venezuela

#actualización: Estos son los prompts de error e información que puede desplegar el sistema
#to do: De momento nada

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class Prompt(QMessageBox):

    def  __init__(self, title, message):
        super().__init__()
        self.msg = QMessageBox()
        self.msg.setText(message)
        self.msg.setWindowTitle(title)
        self.msg.setWindowIcon(QIcon("static/icono_CEIC.png"))

class ErrorPrompt(Prompt):

    def __init__(self, title, message):
        super().__init__(title, message)
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Close)
        self.msg.exec_()

class InfoPrompt(Prompt):

    def __init__(self, title, message):
        super().__init__(title, message)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

class ConfirmPrompt(Prompt):

    def __init__(self, title, message):
        super().__init__(title, message)
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
        
