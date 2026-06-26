class Tutoria:
    def __init__(self,id,fecha,tema,estudiantes=None):
        self.id = id
        self.fecha= fecha
        self.tema = tema
        self.estudiantes = estudiantes if estudiantes else []

    def programar(self):
        print(f"Tutoria {self.id} programada para {self.fecha}")

    def cancelar(self):
        print(f"Tutoria {self.id} cancelada")
    
    def estud_asistentes(self):
        print(self.estudiantes)