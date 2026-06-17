from abc import ABC, abstractmethod

class Usuarios(ABC):
    def __init__(self,nombre,apellido,correo,contrasena,rol):
        self.nombre = nombre
        self.apellido = apellido
        self._correo = correo
        self.__contrasena = contrasena
        self.rol = rol

    @property
    def contrasena(self):
        return self.__contrasena
    
    @contrasena.setter
    def contrasena(self,contrasena_n):
        self.__contrasena = contrasena_n

    @property
    def correo(self):
        return self._correo
    
    @correo.setter
    def correo(self,correo_n):
        self._correo = correo_n

    
    def iniciar_sesion(self):
        print(f"El {self.rol} {self.nombre} ha iniciado sesion")

    def cerrar_sesion(self):
        print(f"El {self.rol} {self.nombre} ha cerrado sesion ")

    @abstractmethod
    def actualizar_datos(self):
        print(f"El {self.rol} {self.nombre} ha actualizado sus datos ")


    @abstractmethod
    def cambiar_contraseña(self):
        print(f"El {self.rol} {self.nombre} ha cambiado su contraseña ")

    def crear_usuario(self):
        perfil= {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo" : self.correo,
            "contraseña" : self.contrasena
            }
        print(f"El {self.rol} {self.nombre} ha creado su usuario de manera exitosa")
        return perfil


class Docente(Usuarios):
    def __init__(self,nombre,apellido,correo,contrasena,rol):
        super().__init__(nombre,apellido,correo,contrasena,rol)


    def actualizar_datos(self):
        return super().actualizar_datos()

    def cambiar_contraseña(self):
        return super().cambiar_contraseña()


class Estudiante(Usuarios):
    def __init__(self,nombre,apellido,correo,contrasena,rol):
        super().__init__(nombre,apellido,correo,contrasena,rol)


    def actualizar_datos(self):
        return super().actualizar_datos()

    def cambiar_contraseña(self):
        return super().cambiar_contraseña()
   

class Personal(Usuarios):
    def __init__(self,nombre,apellido,correo,contrasena,rol):
        super().__init__(nombre,apellido,correo,contrasena,rol)
    


    def actualizar_datos(self):
        return super().actualizar_datos()

    def cambiar_contraseña(self):
        return super().cambiar_contraseña()

class FabricaUsuarios:
    def __init__(self):
        pass

    def crear_usuario(self,nombre,apellido,correo,contrasena,rol):
        if rol == "Docente":
            return Docente(nombre,apellido,correo,contrasena,rol)
        elif rol == "Estudiante":
            return Estudiante(nombre,apellido,correo,contrasena,rol)
        elif rol == "Personal":
            return Personal(nombre,apellido,correo,contrasena,rol)
        else:
            print("Rol no válido")



factory = FabricaUsuarios()

usuario = factory.crear_usuario("Marcos","Solorzano","ADADASDA","123456","Estudiante")
usuario_2 = factory.crear_usuario("Marcos","Solorzano","ADADASDA","123456","Docente")
usuario_3 = factory.crear_usuario("Marcos","Solorzano","ADADASDA","123456","Personal")
usuario.iniciar_sesion()
usuario_2.iniciar_sesion()
usuario_3.iniciar_sesion()