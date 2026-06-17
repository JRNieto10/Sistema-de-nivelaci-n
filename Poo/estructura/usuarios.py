from .clases_abstractas import Usuarios


class Docente(Usuarios):
    def __init__(self,nombre,apellido,correo,contrasena,rol):
        super().__init__(nombre,apellido,correo,contrasena,rol)

    def crear_usuario(self):
        return super().crear_usuario()

    def iniciar_sesion(self):
        return super().inciar_sesion()

    def cerrar_sesion(self):
        return super().cerrar_sesion()

    def actualizar_datos(self):
        return super().actualizar_datos()

    def cambiar_contraseña(self):
        return super().cambiar_contraseña()




class Estudiante(Usuarios):
    def __init__(self,nombre,apellido,correo,contrasena,rol):
        super().__init__(nombre,apellido,correo,contrasena,rol)

    def iniciar_sesion(self):
        return super().inciar_sesion()

    def cerrar_sesion(self):
        return super().cerrar_sesion()

    def actualizar_datos(self):
        return super().actualizar_datos()

    def cambiar_contraseña(self):
        return super().cambiar_contraseña()
   

class Personal(Usuarios):
    def __init__(self,nombre,apellido,rol):
        super().__init__(nombre,apellido,rol)
    

    def iniciar_sesion(self):
        return super().inciar_sesion()

    def cerrar_sesion(self):
        return super().cerrar_sesion()

    def actualizar_datos(self):
        return super().actualizar_datos()

    def cambiar_contraseña(self):
        return super().cambiar_contraseña()
