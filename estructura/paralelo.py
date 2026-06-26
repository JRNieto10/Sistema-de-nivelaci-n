class Paralelo:
    def __init__(self, id, nombre, jornada, aula, horario=None):
        self.id = id
        self.nombre = nombre
        self.jornada = jornada
        self.aula = aula
        self.horario = horario if horario else {}
        self.estudiantes = []

    def inscribir_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)
        print(f"Estudiante {estudiante} inscrito en {self.nombre}")

    def retirar_estudiante(self, estudiante):
        if estudiante in self.estudiantes:
            self.estudiantes.remove(estudiante)
            print(f"Estudiante {estudiante} retirado de {self.nombre}")
            return True
        return False

    def __str__(self):
        return f"Paralelo {self.nombre} - Jornada: {self.jornada} - Aula: {self.aula}"
    
    def mostrar_horario(self):
        print(f"\nHorario de {self.nombre} ({self.jornada})")
        print("-" * 30)
        for materia, info in self.horario.items():
            print(f"   {materia}: {info['hora']} - Docente: {info['docente']}")