from .Almacenamiento_horario import GuardarHorarios

class Paralelo:
    def __init__(self, nombre, id=1, curso=None):
        self.nombre = nombre
        self.id = id
        self.curso = curso
        self.estudiantes = []
        self.horario = None
        self.gestor_horarios = GuardarHorarios()  # Añadir referencia

    def inscribir_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)
        print(f"Estudiante {estudiante.nombre if hasattr(estudiante, 'nombre') else estudiante} inscrito en {self.nombre}")
        # Guardar automáticamente
        self.gestor_horarios.guardar_paralelo(self)
        
    def retirar_estudiante(self, estudiante):
        if estudiante in self.estudiantes:
            self.estudiantes.remove(estudiante)
            nombre_est = estudiante.nombre if hasattr(estudiante, 'nombre') else str(estudiante)
            print(f"Estudiante {nombre_est} retirado de {self.nombre}")
            return True
        return False