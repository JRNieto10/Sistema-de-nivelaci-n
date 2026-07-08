# carrera.py
class Carrera:
    def __init__(self, id, area, nombre, modalidad):
        self.id = id
        self.area = area
        self.nombre = nombre
        self.modalidad = modalidad
        self.asignaturas = []

    def retirarse(self):
        print(f"El estudiante se ha retirado de la carrera {self.nombre}")

    def matricularse(self):
        print(f"El estudiante se ha matriculado en la carrera {self.nombre}")