from .usuarios import Estudiante


class Paralelo:
    def __init__(self, id, paralelo, jornada, horario=None):
        self.id = id
        self.paralelo = paralelo
        self.jornada = jornada
        self.horario = horario
        self.estudiantes = []

    def inscribir_estudiante(self, estudiante: Estudiante, paralelos_del_estudiante=None):
        if not isinstance(estudiante, Estudiante):
            print("Solo se pueden inscribir objetos de tipo Estudiante")
            return False

        # si se pasan los otros paralelos del estudiante, se valida que no choquen horarios
        if self.horario and paralelos_del_estudiante:
            for otro_paralelo in paralelos_del_estudiante:
                if otro_paralelo.horario and self.horario.se_traslapa_con(otro_paralelo.horario):
                    print(f"No se puede inscribir: choca con el horario de '{otro_paralelo.paralelo}'")
                    return False

        self.estudiantes.append(estudiante)
        print(f"Estudiante {estudiante.nombre} {estudiante.apellido} inscrito en {self.paralelo}")
        return True

    def retirar_estudiante(self, estudiante: Estudiante):
        if estudiante in self.estudiantes:
            self.estudiantes.remove(estudiante)
            print(f"Estudiante {estudiante.nombre} {estudiante.apellido} retirado de {self.paralelo}")
            return True
        print(f"Estudiante {estudiante.nombre} {estudiante.apellido} no esta inscrito en {self.paralelo}")
        return False

    def ver_curso(self):
        # resumen rapido del paralelo: nombre, jornada y horario asociado
        info_horario = self.horario.consultar() if self.horario else "sin horario asignado"
        return f"Paralelo {self.paralelo} - Jornada: {self.jornada} - {info_horario}"

    def __str__(self):
        return self.ver_curso()