from estructura.Almacenamieto import *

class Autenticacion:
    def __init__(self,almacenamiento : Almacenamiento_Usuarios):
        self.almacenamiento = almacenamiento
        self.usuario_actual= None

    def iniciar_sesion(self,correo,contrasena):
        usuario = self.almacenamiento.verificar_credenciales(correo,contrasena)
        if usuario:
            self.usuario_actual = usuario
            print(f"El {usuario["rol"]} {usuario["nombre"]} ha iniciado sesion correctamente")
            return True
        print("Credenciales incorrectas")
        return False

    def cerrar_sesion(self):
        if self.usuario_actual:
            print(f"El {self.usuario_actual["rol"]} {self.usuario_actual["nombre"]} ha cerrado sesion ")
            self.usuario_actual = None
        else:
            print("No hay sesiones activas")