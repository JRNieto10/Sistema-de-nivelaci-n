personal = [
    {
        "cedula": "123456789",
        "nombre": "josue",
        "apellido": "apellido",
        "correo": "josue@uleam.edu",
        "contrasena": "admin123",
        "rol": "administrativo",
        "fecha_registro": "2026-06-26T19:07:21.010544"
    },
    {
        "cedula": "987654321",
        "nombre": "david",
        "apellido": "apellido",
        "correo": "david@uleam.edu",
        "contrasena": "admin321",
        "rol": "administrativo",
        "fecha_registro": "2026-06-26T19:07:21.011729"
    },
    {
        "cedula": "555555555",
        "nombre": "jessica",
        "apellido": "apellido",
        "correo": "jessica@uleam.edu",
        "contrasena": "admin132",
        "rol": "administrativo",
        "fecha_registro": "2026-06-26T19:07:21.136878"
    }
]


class login_personal:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena

    def validar_login(self):
        for persona in personal:
            if persona["cedula"] == self.cedula and persona["contrasena"] == self.contrasena:
                return True
        return False