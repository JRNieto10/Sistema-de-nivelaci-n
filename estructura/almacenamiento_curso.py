import json
import os
from datetime import datetime

class AlmacenamientoCursos:
    def __init__(self):
        self.base_path = "Datos"
    
    def _get_carrera_path(self, carrera_nombre):
        """Obtiene la ruta de la carpeta de la carrera"""
        carrera_path = os.path.join(self.base_path, carrera_nombre)
        if not os.path.exists(carrera_path):
            os.makedirs(carrera_path)
        return carrera_path
    
    def _get_curso_path(self, carrera_nombre, curso_nombre):
        """Obtiene la ruta de la carpeta del curso"""
        carrera_path = self._get_carrera_path(carrera_nombre)
        curso_path = os.path.join(carrera_path, curso_nombre)
        if not os.path.exists(curso_path):
            os.makedirs(curso_path)
        return curso_path
    
    def guardar_curso(self, carrera_nombre, curso_nombre, materias_con_docentes):
        """
        Guarda un curso con su estructura de materias y docentes
        materias_con_docentes: dict {materia_nombre: [docente1, docente2, ...]}
        """
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
        
        print(f"Curso guardado en: {archivo}")
        return archivo
    
    def cargar_curso(self, carrera_nombre, curso_nombre):
        """Carga la estructura de un curso desde el JSON"""
        curso_path = self._get_curso_path(carrera_nombre, curso_nombre)
        archivo = os.path.join(curso_path, "estructura.json")
        
        print(f"Buscando estructura en: {archivo}")
        
        if not os.path.exists(archivo):
            print(f"Archivo no encontrado: {archivo}")
            return None
        
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                print(f"Estructura cargada: {datos.get('curso', '')} - {len(datos.get('materias', []))} materias")
                return datos
        except Exception as e:
            print(f"Error al cargar estructura: {e}")
            return None
    
    def guardar_paralelos(self, carrera_nombre, curso_nombre, paralelos):
        """
        Guarda los paralelos de un curso
        paralelos: lista de dict con {letra, aula, horario, materias: [{nombre, docente, aula}]}
        """
        curso_path = self._get_curso_path(carrera_nombre, curso_nombre)
        
        datos_paralelos = {
            "curso": curso_nombre,
            "carrera": carrera_nombre,
            "fecha_creacion": datetime.now().isoformat(),
            "paralelos": paralelos
        }
        
        archivo = os.path.join(curso_path, "paralelos.json")
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos_paralelos, f, ensure_ascii=False, indent=4)
        
        print(f"Paralelos guardados en: {archivo}")
        return archivo
    
    def cargar_paralelos(self, carrera_nombre, curso_nombre):
        """Carga los paralelos de un curso"""
        curso_path = self._get_curso_path(carrera_nombre, curso_nombre)
        archivo = os.path.join(curso_path, "paralelos.json")
        
        if not os.path.exists(archivo):
            return None
        
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def listar_cursos(self, carrera_nombre):
        """Lista todos los cursos de una carrera"""
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
        """Lista todas las carreras que tienen cursos"""
        if not os.path.exists(self.base_path):
            return []
        
        carreras = []
        for item in os.listdir(self.base_path):
            item_path = os.path.join(self.base_path, item)
            if os.path.isdir(item_path):
                carreras.append(item)
        
        return carreras