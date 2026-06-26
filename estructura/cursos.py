class Curso:
    def __init__(self, nombre_curso):
        self.nombre_curso = nombre_curso
        self.materias = {}

    def agregar_materia(self, asignatura, horas_requeridas=1):
        if asignatura not in self.materias:
            self.materias[asignatura] = {
                "docentes": [],
                "horas_requeridas": horas_requeridas
            }
            print(f"Materia '{asignatura}' agregada ({horas_requeridas} hora/semana)")
        else:
            print(f"La materia '{asignatura}' ya existe")

    def agregar_docente(self, docente, asignatura):
        if asignatura in self.materias:
            self.materias[asignatura]["docentes"].append(docente)
            print(f"Docente '{docente}' asignado a '{asignatura}'")
        else:
            print(f"Primero debe agregar la materia '{asignatura}'")

    def obtener_docentes_por_materia(self, asignatura):
        return self.materias[asignatura]["docentes"] if asignatura in self.materias else []
    
    def obtener_materias_por_docente(self, docente):
        materias_docente = []
        for materia, info in self.materias.items():
            if docente in info["docentes"]:
                materias_docente.append(materia)
        return materias_docente

    def __str__(self):
        return f"Curso: {self.nombre_curso} - Materias: {list(self.materias.keys())}"