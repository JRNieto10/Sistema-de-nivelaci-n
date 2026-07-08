import json
import os

class encontrar_cedula:
    def __init__(self, cedula, rol):
        self.cedula = cedula
        self.rol = rol
        self.ruta_permitidos = 'Datos/permitidos.json'
    
    def buscar_cedula(self):
        if not os.path.exists(self.ruta_permitidos):
            return "No hay registros de cédulas permitidas"
        
        try:
            with open(self.ruta_permitidos, 'r', encoding='utf-8') as archivo:
                permitidos = json.load(archivo)
            
            # Verificar estructura del JSON
            if not isinstance(permitidos, dict):
                return "Error en la estructura del archivo de permitidos"
            
            if self.rol == "Estudiante":
                if self.cedula in permitidos.get("cedulas_estudiantes", []):
                    return "Estudiante"
                else:
                    return "No encontrada"
            
            elif self.rol == "Docente":
                if self.cedula in permitidos.get("cedulas_docentes", []):
                    return "Docente"
                else:
                    return "No encontrada"
            
            elif self.rol == "Administrador":
                if self.cedula in permitidos.get("cedulas_personal", []):
                    return "Personal"
                else:
                    return "No encontrada"
            else:
                return "Rol no válido"
                
        except json.JSONDecodeError:
            return "Error en el formato del archivo de permitidos"
        except Exception as e:
            return f"Error al leer el archivo: {e}"