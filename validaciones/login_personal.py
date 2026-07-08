import json
import os

class login_personal:
    def __init__(self, cedula, contrasena):
        self.cedula = cedula
        self.contrasena = contrasena
        self.ruta_personal = 'Datos/personal_administrativo.json'
    
    def validar_login(self):
        if not os.path.exists(self.ruta_personal):
            return False, "No hay personal administrativo registrado en el sistema"
        
        try:
            with open(self.ruta_personal, 'r', encoding='utf-8') as archivo:
                personal = json.load(archivo)
            
            for persona in personal:
                if persona.get("cedula") == self.cedula and persona.get("contrasena") == self.contrasena:
                    return True, "Login exitoso"
            
            return False, "Cédula o contraseña incorrecta"
            
        except json.JSONDecodeError:
            return False, "Error en el formato del archivo de personal"
        except Exception as e:
            return False, f"Error al leer el archivo: {e}"