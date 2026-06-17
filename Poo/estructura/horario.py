class Horario:
    def __init__(self, dia, hora_inicio, hora_fin, aula):
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.aula = aula

    def consultar(self):
        # devuelve un resumen del horario, util para mostrarlo o compararlo
        return f"{self.dia} {self.hora_inicio}-{self.hora_fin} (Aula {self.aula})"

    def se_traslapa_con(self, otro_horario):
        # dos horarios chocan si son el mismo dia y sus rangos de hora se cruzan
        if self.dia != otro_horario.dia:
            return False
        return self.hora_inicio < otro_horario.hora_fin and otro_horario.hora_inicio < self.hora_fin

    def __str__(self):
        return self.consultar()