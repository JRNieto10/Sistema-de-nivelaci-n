from abc import ABC, abstractmethod

class ManejadorNotificacion(ABC):
    def __init__(self):
        self._siguiente = None

    def set_siguiente(self, manejador):
        self._siguiente = manejador
        return manejador

    @abstractmethod
    def manejar(self, notificacion):
        if self._siguiente:
            return self._siguiente.manejar(notificacion)
        return False

class ManejadorCorreo(ManejadorNotificacion):
    def manejar(self, notificacion):
        if notificacion.get('tipo') == 'correo':
            print(f"Enviando correo a {notificacion.get('destinatario')}: {notificacion.get('mensaje')}")
            return True
        return super().manejar(notificacion)

class sistemaNoti:
    def __init__(self):
        self._cadena = self._configurar_cadena()

    def _configurar_cadena(self):
        correo = ManejadorCorreo()
        return correo

    def enviar(self, notificacion):
        return self._cadena.manejar(notificacion)

sistema = sistemaNoti()


notificacion_correo = {
    "tipo": "correo",
    "destinatario": "estudiante",
    "mensaje": "Su tutoria ha sido programada correctamente"
}

sistema.enviar(notificacion_correo)