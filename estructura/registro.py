import json

class Registro:
    def __init__(self):
        self.archivo_permitidos = "Datos/permitidos.json"
    
    def verificar_cedula_permitida(self, cedula):
        try:
            with open(self.archivo_permitidos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except FileNotFoundError:
            return None
        
        if cedula in datos.get("cedulas_estudiantes", []):
            return "estudiante"
        elif cedula in datos.get("cedulas_docentes", []):
            return "docente"
        elif cedula in datos.get("cedulas_personal", []):
            return "personal"
        return None