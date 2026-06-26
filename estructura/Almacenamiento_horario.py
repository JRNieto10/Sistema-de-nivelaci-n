import json

class GuardarHorarios:
    def __init__(self):
        self.ruta_paralelos = "Datos/paralelos.json"
    
    def guardar_paralelos(self, paralelos):
        datos = []
        nombres_existentes = set()
        
        for paralelo in paralelos:
            if paralelo.nombre not in nombres_existentes:
                datos.append({
                    "id": paralelo.id,
                    "nombre": paralelo.nombre,
                    "jornada": paralelo.jornada,
                    "aula": paralelo.aula,
                    "horario": paralelo.horario
                })
                nombres_existentes.add(paralelo.nombre)
        
        with open(self.ruta_paralelos, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    
    def cargar_paralelos(self):
        try:
            with open(self.ruta_paralelos, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def obtener_horario_paralelo(self, nombre_paralelo):
        paralelos = self.cargar_paralelos()
        for paralelo in paralelos:
            if paralelo["nombre"] == nombre_paralelo:
                return paralelo["horario"]
        return None
    
    def mostrar_horario_paralelo(self, nombre_paralelo):
        horario = self.obtener_horario_paralelo(nombre_paralelo)
        
        if not horario:
            print(f"No se encontro el paralelo {nombre_paralelo}")
            return
        
        print(f"\nHorario del {nombre_paralelo}")
        print("")
        
        for materia, info in horario.items():
            print(f"    {info['hora']} - {materia} ({info['docente']})")