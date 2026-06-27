import json
with open('Datos/docentes.json', 'r', encoding='utf-8') as archivo:
    docentes = json.load(archivo)

class login_docentes:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena

    def validar_login(self):
        for docente in docentes:
            if docente["cedula"] == self.cedula and docente["contrasena"] == self.contrasena:
                return True
        return False