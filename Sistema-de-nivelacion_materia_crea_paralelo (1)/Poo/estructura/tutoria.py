# Aqui se implementa el Modelo (MVC)
# estructura/tutoria.py
class Tutoria:
    """Tutoría programada por un Docente para estudiantes de una materia."""

    def __init__(self, id_tutoria, fecha, tema, docente_cedula, materia="", paralelo_id="", estudiantes=None, obligatorios=None):
        # Aqui se hizo Constructor
        self.id = id_tutoria
        self.fecha = fecha
        self.tema = tema
        self.docente_cedula = docente_cedula
        self.materia = materia
        self.paralelo_id = paralelo_id
        self.estudiantes = estudiantes if estudiantes else []
        self.obligatorios = obligatorios if obligatorios else []
        self.estado = "Programada"

    def programar(self):
        self.estado = "Programada"
        print(f"Tutoria {self.id} programada para {self.fecha}")

    def cancelar(self):
        self.estado = "Cancelada"
        print(f"Tutoria {self.id} cancelada")

    def agregar_estudiante(self, cedula_estudiante):
        if cedula_estudiante not in self.estudiantes:
            self.estudiantes.append(cedula_estudiante)
            return True
        return False

    def agregar_obligatorio(self, cedula_estudiante):
        if cedula_estudiante not in self.obligatorios:
            self.obligatorios.append(cedula_estudiante)
            return True
        return False

    def estud_asistentes(self):
        print(self.estudiantes)
        return self.estudiantes

    def __str__(self):
        return f"Tutoria {self.id} - {self.tema} ({self.fecha}) - {self.materia} - {self.estado}"
