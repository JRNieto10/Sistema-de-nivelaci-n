from .paralelo import Paralelo
from .generador_horario import GeneradorHorario


class Gestor_curso:
    def __init__(self):
        self.paralelos = []
        self.creacion_completada = False

        self.aulas_disponibles = ["101", "102", "103", "204", "306", "303"]
        self.jornadas = ["Matutina", "Vespertina", "Nocturna"]

        self.horarios_por_jornada = {
            "Matutina": ["07:00", "08:00", "09:00", "10:00", "11:00"],
            "Vespertina": ["13:00", "14:00", "15:00", "16:00", "17:00"],
            "Nocturna": ["18:00", "19:00", "20:00", "21:00"]
        }

        self.generador_horario = GeneradorHorario(self.horarios_por_jornada)

    def crear_cursos(self, nombre_curso_base, cantidad_paralelos, curso):
        if self.creacion_completada:
            raise RuntimeError("Los cursos ya han sido creados")

        if not hasattr(curso, 'materias'):
            raise TypeError("El parametro 'curso' debe ser un objeto de la clase Curso")

        docentes_unicos = set()
        for materia, info in curso.materias.items():
            for docente in info["docentes"]:
                docentes_unicos.add(docente)

        docentes_lista = list(docentes_unicos)
        cantidad_docentes = len(docentes_lista)

        print(f"\nCreando {cantidad_paralelos} paralelo(s) para {cantidad_docentes} docente(s)")
        print("-" * 40)

        paralelos_creados = []

        for i in range(cantidad_paralelos):
            jornada = self._asignar_jornada(i, cantidad_docentes)
            aula = self.aulas_disponibles[i % len(self.aulas_disponibles)]

            letra_paralelo = chr(65 + i)
            nombre_paralelo = f"{nombre_curso_base} {letra_paralelo}"

            nuevo_paralelo = Paralelo(
                id=f"{nombre_curso_base}_{letra_paralelo}",
                nombre=nombre_paralelo,
                jornada=jornada,
                aula=aula
            )

            nuevo_paralelo.horario = self.generador_horario.generar(
                nuevo_paralelo,
                curso,
                docentes_lista,
                i
            )

            paralelos_creados.append(nuevo_paralelo)
            print(f"Creado: {nuevo_paralelo}")

        self.paralelos = paralelos_creados
        self.creacion_completada = True
        return paralelos_creados

    def _asignar_jornada(self, indice, cantidad_docentes):
        if cantidad_docentes == 1:
            return "Matutina"
        if cantidad_docentes == 2:
            return "Matutina" if indice == 0 else "Vespertina"
        return self.jornadas[indice % len(self.jornadas)]

    def obtener_horario_por_docente(self, nombre_docente):
        horario_docente = {}

        for paralelo in self.paralelos:
            for materia, info in paralelo.horario.items():
                if info["docente"] == nombre_docente:
                    if paralelo.nombre not in horario_docente:
                        horario_docente[paralelo.nombre] = {
                            "jornada": paralelo.jornada,
                            "aula": paralelo.aula,
                            "materias": []
                        }
                    horario_docente[paralelo.nombre]["materias"].append({
                        "materia": materia,
                        "hora": info["hora"]
                    })

        return horario_docente

    def mostrar_horario_docente(self, nombre_docente):
        horario = self.obtener_horario_por_docente(nombre_docente)

        if not horario:
            print(f"No se encontro al docente {nombre_docente}")
            return

        print(f"\nHorario del docente: {nombre_docente}")
        print("=" * 40)

        for paralelo, info in horario.items():
            print(f"\nParalelo: {paralelo} ({info['jornada']} - Aula: {info['aula']})")
            for materia_info in info["materias"]:
                print(f"    {materia_info['hora']} - {materia_info['materia']}")