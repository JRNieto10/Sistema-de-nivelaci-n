class Carrera:
    def __init__(self,id,area,nombre,jornada,modalidad):
        self.id = id
        self.area = area
        self.nombre = nombre
        self.jornada = jornada
        self.modalidad = modalidad

    def retirarse(self):
        print(f"El estudiante se ha retirado de la carrera {self.nombre}")

    def matricularse(self):
        print(f"El estudiante se ha matriculado en la carrera {self.nombre}")