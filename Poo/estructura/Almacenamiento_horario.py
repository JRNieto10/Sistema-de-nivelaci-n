from estructura.facade_json import Facada_json

class GuardarHorarios:
    def __init__(self):
        self.ruta_paralelos = "Poo/Datos/paralelos.json"
        self.json = Facada_json()
    
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
        


        exito = self.json.guardar_datos(self.ruta_paralelos, 'id', datos)

        if exito:
            print("¡Archivo JSON actualizado con éxito!")
        else:
            print("No se agregaron nuevos datos (todos los IDs ya existían en el archivo).")
    
    def cargar_paralelos(self):
        return self.json.cargar_datos(self.ruta_paralelos)
    
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
        
        print(f"\nHorario del {nombre_paralelo}\n")
        for materia, info in horario.items():
            print(f"    {info['hora']} - {materia} ({info['docente']})")