# Importamos la clase que gestiona los horarios y los archivos
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from estructura.Almacenamiento_horario import GuardarHorarios
# CAMBIO 1: Importas tu clase Visualizador_Horarios (ajusta la ruta de importación si está en otro archivo)
from estructura.VisualizacionDeHorarios import Visualizador_Horarios 

# =====================================================================
# SIMULACIÓN DE LA CLASE PARALELO (Para que el main pueda crear objetos)
# =====================================================================
class Paralelo:
    def __init__(self, id, nombre, jornada, aula, horario):
        self.id = id
        self.nombre = nombre
        self.jornada = jornada
        self.aula = aula
        self.horario = horario

# =====================================================================
# SCRIPT PRINCIPAL DE EJECUCIÓN (MAIN)
# =====================================================================
if __name__ == "__main__":
    print("=== INICIANDO PRUEBA DEL SISTEMA DE HORARIOS ===\n")

    # 1. Instanciamos el gestor de horarios
    gestor = GuardarHorarios()

    # 2. Creamos datos de prueba (Simulando la entrada del sistema)
    horario_paralelo_a = {
        "Matemáticas": {"hora": "07:15 - 09:00", "docente": "Ing. Carlos Pérez"},
        "Programación": {"hora": "09:00 - 10:45", "docente": "Ing. Ana Gómez"}
    }
    
    horario_paralelo_b = {
        "Física": {"hora": "18:30 - 20:15", "docente": "Dr. Luis Silva"},
        "Base de Datos": {"hora": "20:15 - 22:00", "docente": "Msc. Marta Rivas"}
    }

    lista_nuevos_paralelos = [
        Paralelo(10, "Paralelo A", "Matutina", "Aula 101", horario_paralelo_a),
        Paralelo(20, "Paralelo B", "Nocturna", "Aula 102", horario_paralelo_b),
        Paralelo(30, "Paralelo A", "Matutina", "Aula 101", {}),  # DUPLICADO EN NOMBRE
        Paralelo(10, "Paralelo C", "Vespertina", "Aula 103", {}) # DUPLICADO EN ID
    ]

    # 3. PROBAMOS LA ESCRITURA (Guardar los paralelos)
    print("--- PASO 1: Intentando guardar la lista de paralelos ---")
    gestor.guardar_paralelos(lista_nuevos_paralelos)
    
    print("\n--- PASO 2: Intentando guardar la misma lista de nuevo (Simulación de re-ejecución) ---")
    gestor.guardar_paralelos(lista_nuevos_paralelos)

    # 4. PROBAMOS LA LECTURA Y MUESTRA DE DATOS
    # CAMBIO 2: Ahora usamos la propiedad .horario del Visualizador_Horarios
    print("\n--- PASO 3: Probando visualización de horarios (Propiedad .horario) ---")
    
    # Caso Exitoso 1: Paralelo A
    v_paralelo_a = Visualizador_Horarios("paralelo", "Paralelo A")
    v_paralelo_a.horario  # <- Invocación como propiedad (sin paréntesis)
    
    # Caso Exitoso 2: Paralelo B
    v_paralelo_b = Visualizador_Horarios("paralelo", "Paralelo B")
    v_paralelo_b.horario  # <- Invocación como propiedad
    
    # Caso Fallido: El paralelo no existe
    v_paralelo_z = Visualizador_Horarios("paralelo", "Paralelo Z")
    v_paralelo_z.horario  # <- Nos dará el mensaje de "no se encontró..."

    print("\n=== PRUEBA FINALIZADA ===")