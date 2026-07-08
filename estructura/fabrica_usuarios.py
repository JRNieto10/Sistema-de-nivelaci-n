from .estudiantes import Estudiante
from .docentes import Docente
from .personal_administrativo import Personal

class FabricaUsuarios:
    def __init__(self):
        pass

    def crear_usuario(self,user):
        if user["rol"] == "docente":
            return Docente(user["nombre"],user["cedula"],user["apellido"],user["correo"],user["contrasena"],user["rol"])
        elif user["rol"] == "estudiante":
            return Estudiante(user["nombre"],user["cedula"],user["apellido"],user["correo"],user["contrasena"],user["rol"])
        elif user["rol"] == "personal" or user["rol"] == "administrador":
            return Personal(user["nombre"],user["cedula"],user["apellido"],user["correo"],user["contrasena"],user["rol"])
        else:
            raise ValueError(f"El rol '{user['rol']}' no existe en el sistema.")