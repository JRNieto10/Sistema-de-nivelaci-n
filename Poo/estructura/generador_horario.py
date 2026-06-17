class GeneradorHorario:
    """Se encarga solo de calcular el horario de un paralelo (SRP)."""

    def __init__(self, horarios_por_jornada):
        self.horarios_por_jornada = horarios_por_jornada

    def generar(self, paralelo, curso, docentes_lista, indice_paralelo):
        horario = {}
        horarios_usados = set()

        materias = list(curso.materias.keys())
        horas_disponibles = self.horarios_por_jornada[paralelo.jornada].copy()

        for indic, materia in enumerate(materias):
            docentes_materia = curso.materias[materia]["docentes"]

            if docentes_materia:
                docente_asignado = docentes_materia[indice_paralelo % len(docentes_materia)]
            else:
                docente_asignado = "no tiene docente"

            hora_indice = (indice_paralelo + indic) % len(horas_disponibles)
            hora_asignada = horas_disponibles[hora_indice]

            while hora_asignada in horarios_usados:
                hora_indice = (hora_indice + 1) % len(horas_disponibles)
                hora_asignada = horas_disponibles[hora_indice]

            horarios_usados.add(hora_asignada)

            horario[materia] = {
                "docente": docente_asignado,
                "hora": hora_asignada
            }

        return horario