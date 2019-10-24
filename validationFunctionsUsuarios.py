#CEIC Libros
#Funciones de validacion
#Desarrollado por Forward

#Importamos los otros codigos a usar
from Prompt import ErrorPrompt, InfoPrompt
import re

# Funcion para verificar si una frase coincide con un Regex
def checkPattern(name, pattern, title, message):
    if pattern.match(name) is None:
        ErrorPrompt(title, message)
        return False
    else:
        return True
# Funcion para verificar si la longitud del nombre de usuario es correcta
def checkUsername(username):
    if len(username) < 33:
        return True
    else:
        ErrorPrompt("Error", "Nombre de usuario invalido, verifique la longitud del mismo")
        return False

# Funcion para verificar si el nombre y el apellido del usuario estan escrito correctamente
def checkName(name, firstOrLast):
    if firstOrLast == 2: #Estamos validando un nombre
        pattern = re.compile(r"^[a-zA-ZñÑáÁéÉíÍóÓúÚ]+$")
        ubicacion = "Caracter inválido en el nombre"
    else: #Estamos validando un apellido
        pattern = re.compile(r"^[a-zA-ZñÑáÁéÉíÍóÓúÚ][a-zA-ZñÑáÁéÉíÍóÓúÚ ]+$")
        ubicacion = "Caracter inválido en el apellido"
    return checkPattern(name, pattern, "Caracter inválido", ubicacion)

# Funcion para verificar la contraseña
#def checkContraseña(contraseña):
#    return True

# Funcion para verificar si el permiso del usuario esta en el rango [0,1]
def checkPermisos(permisos):
    if permisos != "Usuario" and permisos != "Administrador":
        ErrorPrompt("Error", "Solo existen dos roles, Usuario y Administrador")
        return False
    else:
        return True

# Funcion para verificar si el correo del usuario esta escrito correctamente
def checkEmail(address):
    pattern = re.compile(r"[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+")
    return checkPattern(address, pattern, "Email inválido", "Dirección de correo inválida")

# Funcion que realiza la verificacion de todos los campos de la informacion de usuario a modificar o agregar
def verification(fields, checkUntil):
    correct = True
    for i in range(checkUntil):
        if i == 0:
            correct = checkUsername(fields[i])
        elif i == 1 or i == 2:
            correct = checkName(fields[i], i)
        elif i == 4:
            correct = checkPermisos(fields[i])
            print(fields[i])
        elif i == 3:
            correct = checkEmail(fields[i])

        if not correct:
            return False

    return True

