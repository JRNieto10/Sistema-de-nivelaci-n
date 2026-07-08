import json
import os

class login_docentes:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena
        self.ruta_docentes = 'Datos/docentes.json'
    
    def validar_login(self):
        if not os.path.exists(self.ruta_docentes):
            return False, "No hay docentes registrados en el sistema"
        
        try:
            with open(self.ruta_docentes, 'r', encoding='utf-8') as archivo:
                docentes = json.load(archivo)
            
            for docente in docentes:
                if docente.get("cedula") == self.cedula and docente.get("contrasena") == self.contrasena:
                    return True, "Login exitoso"
            
            return False, "Cédula o contraseña incorrecta"
            
        except json.JSONDecodeError:
            return False, "Error en el formato del archivo de docentes"
        except Exception as e:
            return False, f"Error al leer el archivo: {e}"