import json

with open('Datos/estudiantes.json', 'r', encoding='utf-8') as archivo:
    estudiantes  = json.load(archivo)
class login_estudiantes:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena

    def validar_login(self):
        for estudiante in estudiantes:
            if estudiante["cedula"] == self.cedula and estudiante["contrasena"] == self.contrasena:
                return True
        return False