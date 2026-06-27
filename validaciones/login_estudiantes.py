estudiantes = [
    {
        "cedula": "888888888",
        "nombre": "laura",
        "apellido": "torres",
        "correo": "laura@uleam.edu",
        "contrasena": "laura123",
        "rol": "estudiante",
        "fecha_registro": "2026-06-26T19:07:21.310537"
    },
    {
        "cedula": "999999999",
        "nombre": "jorge",
        "apellido": "flores",
        "correo": "jorge@uleam.edu",
        "contrasena": "jorge123",
        "rol": "estudiante",
        "fecha_registro": "2026-06-26T19:07:21.311399"
    },
    {
        "cedula": "101010101",
        "nombre": "marta",
        "apellido": "diaz",
        "correo": "marta@uleam.edu",
        "contrasena": "marta123",
        "rol": "estudiante",
        "fecha_registro": "2026-06-26T19:07:21.312268"
    },
    {
        "cedula": "121212121",
        "nombre": "roberto",
        "apellido": "vega",
        "correo": "roberto@uleam.edu",
        "contrasena": "roberto123",
        "rol": "estudiante",
        "fecha_registro": "2026-06-26T19:07:21.313271"
    }
]


class login_estudiantes:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena

    def validar_login(self):
        for estudiante in estudiantes:
            if estudiante["cedula"] == self.cedula and estudiante["contrasena"] == self.contrasena:
                return True
        return False