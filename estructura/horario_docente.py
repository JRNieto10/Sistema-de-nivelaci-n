class HorarioDocente:

    def __init__(self, nombre_docente, gestor):
        self.nombre_docente = nombre_docente
        self.horario = gestor.obtener_horario_por_docente(nombre_docente)
    
    def mostrar(self):
        if not self.horario:
            print(f"NO existe horario para el docente: {self.nombre_docente}")
            return
        
        print("Horario:")
        for paralelo, info in self.horario.items():
            print()
            print()
            print(f" {paralelo} ({info['jornada']} - Aula: {info['aula']})")
            for materia_info in info["materias"]:
                print(f"   {materia_info['hora']} - {materia_info['materia']}")