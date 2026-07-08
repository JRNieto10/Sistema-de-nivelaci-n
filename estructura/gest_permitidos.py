import json
import os

class GestionPermitidos:
    def __init__(self):
        self.ruta_archivo = "Datos/permitidos.json"
        self._crear_archivo_si_no_existe()
    
    def _crear_archivo_si_no_existe(self):
        if not os.path.exists(self.ruta_archivo):
            os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
            datos_iniciales = {
                "cedulas_estudiantes": [],
                "cedulas_docentes": [],
                "cedulas_personal": []
            }
            with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_iniciales, f, ensure_ascii=False, indent=4)
    
    def _cargar_datos(self):
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"cedulas_estudiantes": [], "cedulas_docentes": [], "cedulas_personal": []}
    
    def _guardar_datos(self, datos):
        with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    
    def agregar_cedula(self, cedula, tipo):
        datos = self._cargar_datos()
        
        if tipo.lower() == "estudiante":
            if cedula not in datos["cedulas_estudiantes"]:
                datos["cedulas_estudiantes"].append(cedula)
                self._guardar_datos(datos)
                return True
        elif tipo.lower() == "docente":
            if cedula not in datos["cedulas_docentes"]:
                datos["cedulas_docentes"].append(cedula)
                self._guardar_datos(datos)
                return True
        elif tipo.lower() == "personal":
            if cedula not in datos["cedulas_personal"]:
                datos["cedulas_personal"].append(cedula)
                self._guardar_datos(datos)
                return True
        return False
    
    def eliminar_cedula(self, cedula, tipo):
        datos = self._cargar_datos()
        
        if tipo.lower() == "estudiante":
            if cedula in datos["cedulas_estudiantes"]:
                datos["cedulas_estudiantes"].remove(cedula)
                self._guardar_datos(datos)
                return True
        elif tipo.lower() == "docente":
            if cedula in datos["cedulas_docentes"]:
                datos["cedulas_docentes"].remove(cedula)
                self._guardar_datos(datos)
                return True
        elif tipo.lower() == "personal":
            if cedula in datos["cedulas_personal"]:
                datos["cedulas_personal"].remove(cedula)
                self._guardar_datos(datos)
                return True
        return False
    
    def eliminar_cedula_todos(self, cedula):
        datos = self._cargar_datos()
        eliminada = False
        
        if cedula in datos["cedulas_estudiantes"]:
            datos["cedulas_estudiantes"].remove(cedula)
            eliminada = True
        
        if cedula in datos["cedulas_docentes"]:
            datos["cedulas_docentes"].remove(cedula)
            eliminada = True
        
        if cedula in datos["cedulas_personal"]:
            datos["cedulas_personal"].remove(cedula)
            eliminada = True
        
        if eliminada:
            self._guardar_datos(datos)
        
        return eliminada
    
    def verificar_cedula(self, cedula):
        datos = self._cargar_datos()
        
        if cedula in datos["cedulas_estudiantes"]:
            return "estudiante"
        elif cedula in datos["cedulas_docentes"]:
            return "docente"
        elif cedula in datos["cedulas_personal"]:
            return "personal"
        return None
    
    def listar_cedulas(self, tipo=None):
        datos = self._cargar_datos()
        
        if tipo is None:
            return {
                "estudiantes": datos["cedulas_estudiantes"],
                "docentes": datos["cedulas_docentes"],
                "personal": datos["cedulas_personal"]
            }
        elif tipo.lower() == "estudiante":
            return datos["cedulas_estudiantes"]
        elif tipo.lower() == "docente":
            return datos["cedulas_docentes"]
        elif tipo.lower() == "personal":
            return datos["cedulas_personal"]
        return []
    
    def mostrar_todos(self):
        datos = self._cargar_datos()
        print("\n" + "=" * 50)
        print("CEDULAS PERMITIDAS EN EL SISTEMA")
        print("=" * 50)
        print(f"\nEstudiantes ({len(datos['cedulas_estudiantes'])}):")
        for cedula in datos["cedulas_estudiantes"]:
            print(f"  - {cedula}")
        print(f"\nDocentes ({len(datos['cedulas_docentes'])}):")
        for cedula in datos["cedulas_docentes"]:
            print(f"  - {cedula}")
        print(f"\nPersonal Administrativo ({len(datos['cedulas_personal'])}):")
        for cedula in datos["cedulas_personal"]:
            print(f"  - {cedula}")
        print("=" * 50)
    
    def agregar_multiple(self, cedulas, tipo):
        datos = self._cargar_datos()
        agregadas = []
        
        for cedula in cedulas:
            if tipo.lower() == "estudiante":
                if cedula not in datos["cedulas_estudiantes"]:
                    datos["cedulas_estudiantes"].append(cedula)
                    agregadas.append(cedula)
            elif tipo.lower() == "docente":
                if cedula not in datos["cedulas_docentes"]:
                    datos["cedulas_docentes"].append(cedula)
                    agregadas.append(cedula)
            elif tipo.lower() == "personal":
                if cedula not in datos["cedulas_personal"]:
                    datos["cedulas_personal"].append(cedula)
                    agregadas.append(cedula)
        
        if agregadas:
            self._guardar_datos(datos)
        
        return agregadas
    
    def eliminar_multiple(self, cedulas, tipo):
        datos = self._cargar_datos()
        eliminadas = []
        
        for cedula in cedulas:
            if tipo.lower() == "estudiante":
                if cedula in datos["cedulas_estudiantes"]:
                    datos["cedulas_estudiantes"].remove(cedula)
                    eliminadas.append(cedula)
            elif tipo.lower() == "docente":
                if cedula in datos["cedulas_docentes"]:
                    datos["cedulas_docentes"].remove(cedula)
                    eliminadas.append(cedula)
            elif tipo.lower() == "personal":
                if cedula in datos["cedulas_personal"]:
                    datos["cedulas_personal"].remove(cedula)
                    eliminadas.append(cedula)
        
        if eliminadas:
            self._guardar_datos(datos)
        
        return eliminadas
    
    def limpiar_todos(self):
        datos = {
            "cedulas_estudiantes": [],
            "cedulas_docentes": [],
            "cedulas_personal": []
        }
        self._guardar_datos(datos)
        return True