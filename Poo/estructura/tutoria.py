class Tutoria:
    def __init__(self,id,fecha,tema,**estudiantes):
        self.id = id
        self.fecha= fecha
        self.tema = tema
        self.estudiantes = estudiantes

    def programar(self):
        pass

    def cancelar(self):
        pass
    
    def estud_asistentes(self):
        print(self.estudiantes)



    