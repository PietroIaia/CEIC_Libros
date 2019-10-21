#CEIC Libros
#Tabla de estudiantes
#Autor: Diego Peña, 15-11095
#Fecha de inicio: 21-10-19, Apróx 9:00 am, Hora de Venezuela
#Última modifcación: 21-10-19, 11:03 am, Hora de Venezuela

#actualización: Estos son los prompts de error e información que puede desplegar el sistema
#to do: De momento nada

from PyQt5.QtWidgets import *

class Prompt(QMessageBox):

    def  __init__(self, title, message):
        super().__init__()
        self.msg = QMessageBox()
        self.msg.setText(message)
        self.msg.setWindowTitle(title)

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
