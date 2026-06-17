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

    
    def inciar_sesion(self):
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


    

    