class Calificaciones:
    def __init__(self,nota,fecha):
        self.nota = nota
        self.fecha = fecha

    def asignar_nota(self):
        return self.nota

    def aprobar(self):
        return self.nota >= 7