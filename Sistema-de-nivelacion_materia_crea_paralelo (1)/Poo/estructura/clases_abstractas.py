from abc import ABC, abstractmethod


# Aqui se hizo Abstraccion
# Esta clase representa la idea general de un usuario del sistema.
class Usuarios(ABC):

    # Aqui se hizo Constructor
    def __init__(self, nombre, apellido, correo, contrasena, rol, cedula):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula

        # Aqui se hizo Encapsulamiento
        self._correo = correo
        self.__contrasena = contrasena
        self.rol = rol

    # Aqui se hizo Propiedades get y set
    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, contrasena_n):
        self.__contrasena = contrasena_n

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, correo_n):
        self._correo = correo_n


    # Aqui se hizo Sobrecarga de forma simple en Python
    # El metodo cambia su resultado segun el parametro recibido.
    def nombre_completo(self, formato="normal"):
        if formato == "apellido_primero":
            return f"{self.apellido} {self.nombre}"
        return f"{self.nombre} {self.apellido}"

    # Aqui se hizo Metodo abstracto
    @abstractmethod
    def cambiar_contraseña(self, nueva_contra):
        pass
    
    @abstractmethod
    def opciones_menu(self):
        pass
