class ValidarContraseñas:
    def __init__(self, contraseña1, contraseña2):
        self.contraseña1 = contraseña1
        self.contraseña2 = contraseña2

    def validar(self):
        return self.contraseña1 == self.contraseña2