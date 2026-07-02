from estructura.facade_json import Facada_json

class Visualizador_Horarios:
    def __init__(self,rol):
        self.rol = rol.lower()
        self.ruta_horarios = f"Poo/Datos/horarios_{rol}.json"
        self.json = Facada_json(self.ruta_horarios)

    def cargar_horarios_docentes(self):
        return self.json.repo.leer_todo()
    
    def obtener_horario_docente(self, cedula):
        horarios = self.cargar_horarios_docentes()
        for item in horarios:
            if item[self.rol]["cedula"] == cedula:
                return item["horario"]
        return None
    
    def mostrar_horario_docente(self, cedula):
        horario = self.obtener_horario_docente(cedula)
        if not horario:
            print(f"No se encontro horario para el docente con cedula {cedula}")
            return
        
        print(f"\nHorario del {self.rol}")
        print("=" * 40)
        for paralelo, info in horario.items():
            print(f"\nParalelo: {paralelo} ({info['jornada']} - Aula: {info['aula']})")
            for materia_info in info["materias"]:
                print(f"    [{materia_info['dia']}] {materia_info['hora']} - {materia_info['materia']}")