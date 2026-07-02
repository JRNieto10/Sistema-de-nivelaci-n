# Ubicación: prueba_docentes.py (En la raíz de tu proyecto)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class DocenteMock:
    def __init__(self, cedula, nombre, apellido, correo):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo

# Importaciones correctas de tus gestores
from estructura.Almacenamiento_horario_individal import horariodocentealmacenar 

from estructura.VisualizacionDeHorarios import Visualizador_Horarios

def ejecutar_prueba():
    print("=== INICIANDO PRUEBA DEL SISTEMA DE HORARIOS ===")
    roles = ["Docente","Estudiante"]
    for rol in roles:

        almacenador = horariodocentealmacenar(rol)
        visualizador = Visualizador_Horarios(rol)
        
        # Docente de prueba
        persona1 = DocenteMock(
            cedula="1723456789", 
            nombre="Kevin", 
            apellido="Mendoza", 
            correo="kevin.mendoza@universidad.edu.ec"
        )
        
        # NUEVO: Diccionario estructurado incluyendo la clave 'dia' dentro de cada materia
        horario_prueba = {
            "Paralelo A": {
                "jornada": "Matutina",
                "aula": "Bloque B - 204",
                "materias": [
                    {
                        "dia": "Lunes", 
                        "hora": "07:00 - 09:00", 
                        "materia": "Programación Orientada a Objetos"
                    },
                    {
                        "dia": "Miércoles", 
                        "hora": "09:00 - 11:00", 
                        "materia": "Estructura de Datos"
                    }
                ]
            },
            "Paralelo B": {
                "jornada": "Nocturna",
                "aula": "Laboratorio 3",
                "materias": [
                    {
                        "dia": "Viernes", 
                        "hora": "18:00 - 20:00", 
                        "materia": "Arquitectura de Software"
                    }
                ]
            }
        }
        
        # 1. Guardar o actualizar
        print(f"\n[1] Guardando horario para el docente {persona1.nombre}...")
        almacenador.guardar_horario_docente(persona1, horario_prueba)
        print("¡Datos persistidos de forma segura en el JSON!")
        
        # 2. Visualizar resultado con días incluidos
        print(f"\n[2] Consultando el horario asignado a la cédula: {persona1.cedula}...")
        visualizador.mostrar_horario_docente(persona1.cedula)

if __name__ == "__main__":
    ejecutar_prueba()