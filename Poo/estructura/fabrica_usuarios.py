from .usuarios import *

class FabricaUsuarios:
    def __init__(self):
        pass

    def crear_usuario(self,user):
        if user["rol"] == "Docente":
            return Docente(user["nombre"],user["apellido"],user["correo"],user["contraseña"],user["rol"])
        elif user["rol"] == "Estudiante":
            return Estudiante(user["nombre"],user["apellido"],user["correo"],user["contraseña"],user["rol"])
        elif user["rol"] == "Personal":
            return Personal(user["nombre"],user["apellido"],user["correo"],user["contraseña"],user["rol"])
        else:
            raise ValueError(f"El rol '{user["rol"]}' no existe en el sistema.")