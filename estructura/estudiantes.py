from .clases_abstractas import Usuarios

class Estudiante(Usuarios):
    def __init__(self,nombre,cedula,apellido,correo,contrasena,rol):
        super().__init__(nombre,cedula,apellido,correo,contrasena,rol)

    def iniciar_sesion(self):
        return super().iniciar_sesion()

    def cerrar_sesion(self):
        return super().cerrar_sesion()

    def actualizar_datos(self):
        print(f"El estudiante {self.nombre} ha actualizado sus datos")

    def cambiar_contraseña(self):
        print(f"El estudiante {self.nombre} ha cambiado su contraseña")