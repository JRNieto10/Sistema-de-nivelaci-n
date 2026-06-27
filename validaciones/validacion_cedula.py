class validacion_cedula:
    def __init__(self, cedula):
        self.cedula = cedula

    def validar_cedula(self):
        if len(self.cedula) != 10 or not self.cedula.isdigit():
            return False

        total = 0
        for i in range(9):
            digit = int(self.cedula[i])
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(self.cedula[9])

