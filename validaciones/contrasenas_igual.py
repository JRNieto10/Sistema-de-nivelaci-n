contraseña1 = "3242334"
contraseña2 = "3242334"


class ValidarContraseñas:
    def __init__(self, contraseña1, contraseña2):
        self.contraseña1 = contraseña1
        self.contraseña2 = contraseña2

    def validar(self):
        if self.contraseña1 == self.contraseña2:
            return True
        else:
            return False