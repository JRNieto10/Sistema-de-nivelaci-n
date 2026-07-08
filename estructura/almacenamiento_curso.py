import json
import os
from datetime import datetime

class AlmacenamientoCursos:
    def __init__(self):
        self.base_path = "Datos"
    
    def _get_carrera_path(self, carrera_nombre):
        carrera_path = os.path.join(self.base_path, carrera_nombre)
        if not os.path.exists(carrera_path):
            os.makedirs(carrera_path)
        return carrera_path
    
    def _get_curso_path(self, carrera_nombre, curso_nombre):
        carrera_path = self._get_carrera_path(carrera_nombre)
        curso_path = os.path.join(carrera_path, curso_nombre)
        if not os.path.exists(curso_path):
            os.makedirs(curso_path)
        return curso_path
    
    def guardar_curso(self, carrera_nombre, curso_nombre, materias_con_docentes):
        curso_path = self._get_curso_path(carrera_nombre, curso_nombre)
        
        datos_curso = {
            "curso": curso_nombre,
            "carrera": carrera_nombre,
            "fecha_creacion": datetime.now().isoformat(),
            "materias": []
        }
        
        for materia_nombre, docentes in materias_con_docentes.items():
            datos_materia = {
                "nombre": materia_nombre,
                "docentes": []
            }
            for docente in docentes:
                if isinstance(docente, dict):
                    datos_materia["docentes"].append(docente)
                else:
                    datos_materia["docentes"].append({
                        "nombre": docente.nombre if hasattr(docente, 'nombre') else str(docente),
                        "apellido": docente.apellido if hasattr(docente, 'apellido') else "",
                        "cedula": docente.cedula if hasattr(docente, 'cedula') else "",
                        "correo": docente.correo if hasattr(docente, 'correo') else ""
                    })
            datos_curso["materias"].append(datos_materia)
        
        archivo = os.path.join(curso_path, "estructura.json")
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos_curso, f, ensure_ascii=False, indent=4)
        
        return archivo
    
    def cargar_curso(self, carrera_nombre, curso_nombre):
        curso_path = self._get_curso_path(carrera_nombre, curso_nombre)
        archivo = os.path.join(curso_path, "estructura.json")
        
        if not os.path.exists(archivo):
            return None
        
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos
        except Exception as e:
            return None
    
    def guardar_paralelos(self, carrera_nombre, curso_nombre, paralelos, materias_del_curso=None):
        curso_path = self._get_curso_path(carrera_nombre, curso_nombre)
        
        # Si no se pasan materias, intentar cargar desde estructura.json
        if materias_del_curso is None:
            estructura_path = os.path.join(curso_path, "estructura.json")
            if os.path.exists(estructura_path):
                try:
                    with open(estructura_path, 'r', encoding='utf-8') as f:
                        estructura = json.load(f)
                        materias_del_curso = estructura.get("materias", [])
                except:
                    materias_del_curso = []
            else:
                materias_del_curso = []
        
        # Procesar paralelos para incluir materias
        paralelos_procesados = []
        for paralelo in paralelos:
            paralelo_data = paralelo.copy()
            # Si el paralelo no tiene materias, asignar las del curso
            if not paralelo_data.get("materias"):
                paralelo_data["materias"] = materias_del_curso
            paralelos_procesados.append(paralelo_data)
        
        datos_paralelos = {
            "curso": curso_nombre,
            "carrera": carrera_nombre,
            "fecha_creacion": datetime.now().isoformat(),
            "materias_del_curso": materias_del_curso,
            "paralelos": paralelos_procesados
        }
        
        archivo = os.path.join(curso_path, "paralelos.json")
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos_paralelos, f, ensure_ascii=False, indent=4)
        
        return archivo
    
    def cargar_paralelos(self, carrera_nombre, curso_nombre):
        curso_path = self._get_curso_path(carrera_nombre, curso_nombre)
        archivo = os.path.join(curso_path, "paralelos.json")
        
        if not os.path.exists(archivo):
            return None
        
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def listar_cursos(self, carrera_nombre):
        carrera_path = self._get_carrera_path(carrera_nombre)
        
        if not os.path.exists(carrera_path):
            return []
        
        cursos = []
        for item in os.listdir(carrera_path):
            item_path = os.path.join(carrera_path, item)
            if os.path.isdir(item_path):
                estructura = os.path.join(item_path, "estructura.json")
                if os.path.exists(estructura):
                    cursos.append(item)
        
        return cursos
    
    def listar_carreras(self):
        if not os.path.exists(self.base_path):
            return []
        
        carreras = []
        for item in os.listdir(self.base_path):
            item_path = os.path.join(self.base_path, item)
            if os.path.isdir(item_path):
                carreras.append(item)
        
        return carreras