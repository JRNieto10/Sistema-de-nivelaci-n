from .asignatura import Asignatura


class Curso:
    def __init__(self, nombre_curso):
        self.nombre_curso = nombre_curso
        self.materias = {}

    def agregar_materia(self, nombre_asignatura, horas_requeridas=1):
        if nombre_asignatura not in self.materias:
            asignatura = Asignatura(
                nombre=nombre_asignatura,
                codigo=None,
                creditos=horas_requeridas,
                horas=1,
                modalidad=None
            )
            self.materias[nombre_asignatura] = {
                "asignatura": asignatura,
                "docentes": [],
                "horas_requeridas": horas_requeridas
            }
            print(f"Materia '{nombre_asignatura}' agregada ({horas_requeridas} hora/semana)")
        else:
            print(f"La materia '{nombre_asignatura}' ya existe")

    def agregar_docente(self, docente, nombre_asignatura):
        if nombre_asignatura in self.materias:
            self.materias[nombre_asignatura]["docentes"].append(docente)
            print(f"Docente '{docente}' asignado a '{nombre_asignatura}'")
        else:
            print(f"Primero debe agregar la materia '{nombre_asignatura}'")

    def obtener_docentes_por_materia(self, nombre_asignatura):
        return self.materias[nombre_asignatura]["docentes"] if nombre_asignatura in self.materias else []

    def obtener_materias_por_docente(self, docente):
        materias_docente = []
        for materia, info in self.materias.items():
            if docente in info["docentes"]:
                materias_docente.append(materia)
        return materias_docente

    def __str__(self):
        return f"Curso: {self.nombre_curso} - Materias: {list(self.materias.keys())}"