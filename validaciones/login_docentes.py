docentes = [
    {
        "cedula": "111111111",
        "nombre": "pepito",
        "apellido": "garcia",
        "correo": "pepito@uleam.edu",
        "contrasena": "pepito123",
        "rol": "docente",
        "fecha_registro": "2026-06-26T19:07:21.272519"
    },
    {
        "cedula": "222222222",
        "nombre": "juanito",
        "apellido": "lopez1",
        "correo": "juanito@uleam.edu",
        "contrasena": "juanito123",
        "rol": "docente",
        "fecha_registro": "2026-06-26T19:07:21.273263"
    },
    {
        "cedula": "333333333",
        "nombre": "changuin",
        "apellido": "lopez2",
        "correo": "changuin@uleam.edu",
        "contrasena": "changuin123",
        "rol": "docente",
        "fecha_registro": "2026-06-26T19:07:21.294666"
    },
    {
        "cedula": "444444444",
        "nombre": "mari",
        "apellido": "fernandez",
        "correo": "mari@uleam.edu",
        "contrasena": "mari123",
        "rol": "docente",
        "fecha_registro": "2026-06-26T19:07:21.295670"
    },
    {
        "cedula": "666666666",
        "nombre": "carlitos",
        "apellido": "sanchez",
        "correo": "carlitos@uleam.edu",
        "contrasena": "carlitos123",
        "rol": "docente",
        "fecha_registro": "2026-06-26T19:07:21.309361"
    }
]


class login_docentes:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena

    def validar_login(self):
        for docente in docentes:
            if docente["cedula"] == self.cedula and docente["contrasena"] == self.contrasena:
                return True
        return False