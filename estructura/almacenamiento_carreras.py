# almacenamiento_carreras.py
import json
import os
from estructura.carrera import Carrera
from estructura.asignatura import Asignatura

class AlmacenamientoCarreras:
    def __init__(self):
        self.ruta_carreras = "Datos/carreras/"
        self._crear_directorios()
    
    def _crear_directorios(self):
        if not os.path.exists(self.ruta_carreras):
            os.makedirs(self.ruta_carreras)
    
    def guardar_carrera(self, carrera):
        try:
            nombre_archivo = f"{carrera.id}.json"
            ruta_completa = os.path.join(self.ruta_carreras, nombre_archivo)
            
            datos_carrera = {
                "id": carrera.id,
                "area": carrera.area,
                "nombre": carrera.nombre,
                "modalidad": carrera.modalidad,
                "asignaturas": []
            }
            
            if hasattr(carrera, 'asignaturas') and carrera.asignaturas:
                for asig in carrera.asignaturas:
                    if hasattr(asig, '__dict__'):
                        asignatura_dict = {
                            "nombre": asig.nombre,
                            "codigo": asig.codigo,
                            "creditos": asig.creditos,
                            "horas": asig.horas,
                            "modalidad": asig.modalidad
                        }
                        datos_carrera["asignaturas"].append(asignatura_dict)
                    elif isinstance(asig, dict):
                        datos_carrera["asignaturas"].append(asig)
                    else:
                        datos_carrera["asignaturas"].append(str(asig))
            
            with open(ruta_completa, "w", encoding="utf-8") as archivo:
                json.dump(datos_carrera, archivo, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            return False
    
    def cargar_carrera(self, id_carrera):
        try:
            nombre_archivo = f"{id_carrera}.json"
            ruta_completa = os.path.join(self.ruta_carreras, nombre_archivo)
            
            if not os.path.exists(ruta_completa):
                return None
            
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            
            carrera = Carrera(
                datos["id"],
                datos["area"],
                datos["nombre"],
                datos["modalidad"]
            )
            
            if "asignaturas" in datos:
                for asig_dict in datos["asignaturas"]:
                    asignatura = Asignatura(
                        asig_dict["nombre"],
                        asig_dict["codigo"],
                        asig_dict["creditos"],
                        asig_dict["horas"],
                        asig_dict["modalidad"]
                    )
                    carrera.asignaturas.append(asignatura)
            
            return carrera
        except Exception as e:
            return None
    
    def cargar_todas_carreras(self):
        carreras = []
        try:
            if not os.path.exists(self.ruta_carreras):
                return carreras
            
            for archivo in os.listdir(self.ruta_carreras):
                if archivo.endswith('.json'):
                    id_carrera = archivo.replace('.json', '')
                    carrera = self.cargar_carrera(id_carrera)
                    if carrera:
                        carreras.append(carrera)
            
            return carreras
        except Exception as e:
            return carreras
    
    def eliminar_carrera(self, id_carrera):
        try:
            nombre_archivo = f"{id_carrera}.json"
            ruta_completa = os.path.join(self.ruta_carreras, nombre_archivo)
            
            if os.path.exists(ruta_completa):
                os.remove(ruta_completa)
                return True
            return False
        except Exception as e:
            return False
    
    def agregar_asignatura_a_carrera(self, id_carrera, asignatura):
        try:
            carrera = self.cargar_carrera(id_carrera)
            if not carrera:
                return False
            
            carrera.asignaturas.append(asignatura)
            return self.guardar_carrera(carrera)
        except Exception as e:
            return False
    
    def obtener_asignaturas_carrera(self, id_carrera):
        try:
            carrera = self.cargar_carrera(id_carrera)
            if carrera:
                return carrera.asignaturas
            return []
        except Exception as e:
            return []