# Aqui se implementa el Modelo (MVC)
from estructura.facade_json import Facada_json

class CreadorAcademico:
    def __init__(self):
        self.ruta_carreras = "Datos/carreras.json"
        self.json = Facada_json(self.ruta_carreras)
    
    def registrar_carrera_completa(self, carrera_objeto):
        """
        Recibe un objeto Carrera (que ya contiene sus objetos Materia dentro)
        y lo traduce todo a un diccionario para guardarlo en el JSON.
        """
        datos_cargados = self.json.repo.leer_todo()
        
        # Validar si la carrera ya existe por ID
        for item in datos_cargados:
            if item["id"] == carrera_objeto.id:
                print(f"[Error] La carrera con ID {carrera_objeto.id} ya existe.")
                return False
        
        # 🔄 Traducir la lista de objetos Materia a una lista de diccionarios
        lista_materias_dict = []
        for mat in carrera_objeto.materias:
            lista_materias_dict.append({
                "id": mat.id,
                "nombre": mat.nombre,
                "creditos": mat.creditos
            })
        
        # Estructura final que va al archivo único
        carrera_dict = {
            "id": carrera_objeto.id,
            "nombre": carrera_objeto.nombre,
            "duracion_semestres": carrera_objeto.duracion,
            "materias": lista_materias_dict  # Aquí quedan guardadas juntas
        }
        
        datos_cargados.append(carrera_dict)
        self.json.repo.guardar_todo(datos_cargados)
        print(f"¡Carrera '{carrera_objeto.nombre}' con sus materias guardada con éxito!")
        return True
    # Agregar este método a tu clase CreadorAcademico en Almacenamiento_materias.py

# estructura/Almacenamiento_materias.py

    def agregar_materia_a_carrera(self, nombre_carrera, materia_dict):
        datos = self.json.repo.leer_todo()
        for carrera in datos:
            if carrera["nombre"] == nombre_carrera:
                
                # ✅ SOLUCIÓN: Verifica si la clave 'materias' existe, si no, créala
                if "materias" not in carrera:
                    carrera["materias"] = []
                
                # Ahora es seguro hacer el append
                carrera["materias"].append(materia_dict)
                self.json.repo.guardar_todo(datos)
                return True
        return False
    
    def matricular_docente(self, id_docente, nombre_carrera, nombre_materia):
        # Esta lógica busca la carrera y materia, y añade al docente
        datos = self.json.repo.leer_todo()
        for carrera in datos:
            if carrera["nombre"] == nombre_carrera:
                for materia in carrera.get("materias", []):
                    if materia["nombre"] == nombre_materia:
                        materia["docente_asignado"] = id_docente
                        self.json.repo.guardar_todo(datos)
                        return True
        return False