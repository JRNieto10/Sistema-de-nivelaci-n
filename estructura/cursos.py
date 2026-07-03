class Curso:
    def __init__(self, nombre_curso):
        self.nombre = nombre_curso
        self.materias = {}

    def agregar_materia(self, asignatura, horas_requeridas=1):
        # asignatura es un objeto Asignatura
        if asignatura.nombre not in self.materias:
            self.materias[asignatura.nombre] = {
                "docentes": [],
                "horas_requeridas": horas_requeridas
            }
            print(f"Materia '{asignatura.nombre}' agregada ({horas_requeridas} hora/semana)")
        else:
            print(f"La materia '{asignatura.nombre}' ya existe")

    def agregar_docente(self, docente, asignatura):
        # asignatura puede ser un objeto Asignatura o un string
        nombre_asignatura = asignatura.nombre if hasattr(asignatura, 'nombre') else asignatura
        
        if nombre_asignatura in self.materias:
            # Verificar si el docente ya está asignado
            if docente.nombre not in self.materias[nombre_asignatura]["docentes"]:
                self.materias[nombre_asignatura]["docentes"].append(docente.nombre)
                print(f"Docente '{docente.nombre}' asignado a '{nombre_asignatura}'")
            else:
                print(f"El docente '{docente.nombre}' ya está en '{nombre_asignatura}'")
        else:
            print(f"Primero debe agregar la materia '{nombre_asignatura}'")
    def obtener_docentes_por_materia(self, asignatura):
        return self.materias[asignatura.nombre]["docentes"] if asignatura.nombre in self.materias else []
    
    def obtener_materias_por_docente(self, docente):
        materias_docente = []
        for materia, info in self.materias.items():
            if docente in info["docentes"]:
                materias_docente.append(materia)
        return materias_docente

    def __str__(self):
        return f"Curso: {self.nombre} - Materias: {list(self.materias.keys())}"  # ← CAMBIAR