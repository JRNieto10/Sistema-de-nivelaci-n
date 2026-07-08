# paralelo.py
from .Almacenamiento_horario import GuardarHorarios

class Paralelo:
    def __init__(self, nombre, id=1, curso=None):
        self.nombre = nombre
        self.id = id
        self.curso = curso
        self.estudiantes = []
        self.horario = None
        self.gestor_horarios = GuardarHorarios()

    def inscribir_estudiante(self, estudiante):
        if estudiante not in self.estudiantes:
            self.estudiantes.append(estudiante)
            nombre_est = estudiante.nombre if hasattr(estudiante, 'nombre') else str(estudiante)
            print(f"Estudiante {nombre_est} inscrito en {self.nombre}")
            return True
        return False

    def retirar_estudiante(self, estudiante):
        if estudiante in self.estudiantes:
            self.estudiantes.remove(estudiante)
            nombre_est = estudiante.nombre if hasattr(estudiante, 'nombre') else str(estudiante)
            print(f"Estudiante {nombre_est} retirado de {self.nombre}")
            return True
        return False