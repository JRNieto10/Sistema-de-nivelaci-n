from abc import ABC, abstractmethod


class HorarioBase(ABC):
    """Contrato comun para cualquier clase que muestre un horario."""

    @abstractmethod
    def mostrar(self):
        pass