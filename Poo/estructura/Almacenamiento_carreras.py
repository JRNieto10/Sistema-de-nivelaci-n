from estructura.facade_json import Facada_json

class Almacenamiento_Carreras:
    def __init__(self): # <--- DEBE ESTAR ASÍ, SIN ARGUMENTOS EXTRAS
        self.ruta = "Datos/carreras.json"
        self.json = Facada_json(self.ruta)
        
# estructura/Almacenamiento_carreras.py

    def guardar_carrera(self, carrera_objeto):
        carrera_dict = {
            # Cambia id_xcarrera por id_carrera
            "id": carrera_objeto.id_carrera, 
            "nombre": carrera_objeto.nombre,
            "duracion": carrera_objeto.duracion
        }
        return self.json.guardar_datos('id', carrera_dict)
