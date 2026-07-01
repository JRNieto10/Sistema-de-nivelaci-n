# Importamos la clase que gestiona los horarios y los arch
from estructura.Almacenamiento_horario import GuardarHorarios
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
    # Nota cómo estructuramos el diccionario "horario" para que funcione con tu método mostrar
    horario_paralelo_a = {
        "Matemáticas": {"hora": "07:15 - 09:00", "docente": "Ing. Carlos Pérez"},
        "Programación": {"hora": "09:00 - 10:45", "docente": "Ing. Ana Gómez"}
    }
    
    horario_paralelo_b = {
        "Física": {"hora": "18:30 - 20:15", "docente": "Dr. Luis Silva"},
        "Base de Datos": {"hora": "20:15 - 22:00", "docente": "Msc. Marta Rivas"}
    }

    # Creamos una lista de objetos de la clase Paralelo
    # Incluimos repetidos adrede para probar tus filtros (Nombres e IDs duplicados)
    lista_nuevos_paralelos = [
        Paralelo(10, "Paralelo A", "Matutina", "Aula 101", horario_paralelo_a),
        Paralelo(20, "Paralelo B", "Nocturna", "Aula 102", horario_paralelo_b),
        Paralelo(30, "Paralelo A", "Matutina", "Aula 101", {}),  # DUPLICADO EN NOMBRE (Tu set lo filtrará)
        Paralelo(10, "Paralelo C", "Vespertina", "Aula 103", {}) # DUPLICADO EN ID (La fachada lo filtrará)
    ]

    # 3. PROBAMOS LA ESCRITURA (Guardar los paralelos)
    print("--- PASO 1: Intentando guardar la lista de paralelos ---")
    gestor.guardar_paralelos(lista_nuevos_paralelos)
    
    # Intentamos guardar lo mismo otra vez para ver el comportamiento del validador
    print("\n--- PASO 2: Intentando guardar la misma lista de nuevo (Simulación de re-ejecución) ---")
    gestor.guardar_paralelos(lista_nuevos_paralelos)

    # 4. PROBAMOS LA LECTURA Y MUESTRA DE DATOS
    print("\n--- PASO 3: Probando visualización de horarios (Método Mostrar) ---")
    
    # Caso Exitoso: El paralelo existe en el archivo
    gestor.mostrar_horario_paralelo("Paralelo A")
    gestor.mostrar_horario_paralelo("Paralelo B")
    
    # Caso Fallido: El paralelo no existe
    gestor.mostrar_horario_paralelo("Paralelo Z")

    print("\n=== PRUEBA FINALIZADA ===")
