# def validar_nombre(nombre):
#     var = input("Estas seguro que tu nombre es : ",nombre)
#     if var.lower() == "si":
#         return True
#     else:        return False

from estudiantes import Estudiante

def agregar():


        nombre = input("Ingrese el nombre del estudiante: ")
        apellido = input("Ingrese el apellido del estudiante: ")
        correo = input("Ingrese el correo del estudiante: ")
        contrasena = input("Ingrese la contraseña del estudiante: ")
        rol = "estudiante"
        estudiante = Estudiante(nombre,apellido,correo,contrasena,rol)
        return estudiante