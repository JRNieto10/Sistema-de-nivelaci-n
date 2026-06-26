class HorarioParalelo:
    def __init__(self, paralelo):
        self.paralelo = paralelo
        self.horario = paralelo.horario
    
    def mostrar(self):
        print()
        print(f" Horario de {self.paralelo.nombre} ({self.paralelo.jornada})")
        print(f"aula: {self.paralelo.aula}")
        for materia, info in self.horario.items():
            print(f"   {info['hora']} - {materia} - Docente: {info['docente']}")
    
    def obtener_materia_por_hora(self, hora):
        for materia, info in self.horario.items():
            if info["hora"] == hora:
                return materia, info["docente"]
        return None, None