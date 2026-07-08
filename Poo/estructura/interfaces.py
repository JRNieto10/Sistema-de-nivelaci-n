from abc import ABC, abstractmethod

class ActualizadorDatos(ABC):
    @abstractmethod
    def actualizar_datos_usuario(self, usuario_objetivo, nuevos_datos):
        pass

    @abstractmethod
    def crear_carrera(self, id_carrera, nombre, duracion):
        pass