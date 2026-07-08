# validaciones/login_estudiantes.py
import json
import os

def login_estudiantes(cedula, contrasena):
    ruta_estudiantes = 'Datos/estudiantes.json'
    
    # Verificar si el archivo existe
    if not os.path.exists(ruta_estudiantes):
        return False, "No hay estudiantes registrados en el sistema"
    
    try:
        with open(ruta_estudiantes, 'r', encoding='utf-8') as archivo:
            estudiantes = json.load(archivo)
            
        for estudiante in estudiantes:
            if estudiante.get('cedula') == cedula and estudiante.get('contrasena') == contrasena:
                return True, "Login exitoso"
        
        return False, "Cédula o contraseña incorrecta"
        
    except json.JSONDecodeError:
        return False, "Error en el formato del archivo de estudiantes"
    except Exception as e:
        return False, f"Error al leer el archivo: {e}"