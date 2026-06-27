import json
with open('Datos/estudiantes.json', 'r', encoding='utf-8') as archivo:
    personal = json.load(archivo)

class login_personal:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena

    def validar_login(self):
        for persona in personal:
            if persona["cedula"] == self.cedula and persona["contrasena"] == self.contrasena:
                return True
        return False