from abc import ABC, abstractmethod


# Aqui se hizo Polimorfismo con interfaces
# Esta interfaz obliga a que el administrador pueda actualizar datos.
class ActualizadorDatos(ABC):

    @abstractmethod
    def actualizar_datos_usuario(self, usuario_objetivo, nuevos_datos):
        pass

    @abstractmethod
    def crear_carrera(self, id_carrera, nombre, duracion):
        pass
