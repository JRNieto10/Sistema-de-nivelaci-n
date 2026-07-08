class sistemaNoti:
    def enviar(self, notificacion):
        if notificacion.get('tipo') == 'correo':
            print(f"Enviando correo a {notificacion.get('destinatario')}: {notificacion.get('mensaje')}")
            return True
        elif notificacion.get('tipo') == 'sms':
            print(f"Enviando SMS a {notificacion.get('telefono')}: {notificacion.get('mensaje')}")
            return True
        else:
            print(f"Tipo de notificación no soportado: {notificacion.get('tipo')}")
            return False

sistema = sistemaNoti()

notificacion_correo = {
    "tipo": "correo",
    "destinatario": "estudiante",
    "mensaje": "Su tutoria ha sido programada correctamente"
}

sistema.enviar(notificacion_correo)