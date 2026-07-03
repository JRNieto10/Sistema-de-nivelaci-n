import json
import os

class GuardarHorarios:
    def __init__(self):
        self.paralelos = []
        if not os.path.exists("Datos"):
            os.makedirs("Datos")
    
    def guardar_paralelo(self, paralelo):
        """Guarda un paralelo en la lista y en el archivo JSON"""
        
        # Construir el horario desde el curso si no tiene horario asignado
        horario = getattr(paralelo, 'horario', None)
        
        # Si no tiene horario o está vacío, construirlo desde el curso
        if horario is None or horario == {}:
            horario = self._construir_horario_desde_curso(paralelo.curso)
        
        paralelo_dict = {
            "nombre": paralelo.nombre,
            "id": paralelo.id,
            "curso": paralelo.curso.nombre_curso if hasattr(paralelo.curso, 'nombre_curso') else str(paralelo.curso),
            "estudiantes": [est.nombre if hasattr(est, 'nombre') else str(est) for est in paralelo.estudiantes],
            "horario": horario
        }
        self.paralelos.append(paralelo_dict)
        self._guardar_en_archivo()
    
    def _construir_horario_desde_curso(self, curso):
        """Construye un horario desde las materias del curso"""
        if not hasattr(curso, 'materias') or not curso.materias:
            return {"materias": []}
        
        materias_horario = []
        horas = ["07:00-08:00", "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00"]
        hora_idx = 0
        
        for materia, info in curso.materias.items():
            if hora_idx < len(horas):
                # Obtener el primer docente asignado a la materia o "Sin docente"
                docente = info["docentes"][0] if info["docentes"] else "Sin docente"
                materias_horario.append({
                    "hora": horas[hora_idx],
                    "materia": materia,
                    "docente": docente
                })
                hora_idx += 1
        
        return {"materias": materias_horario}
    
    def cargar_paralelos(self):
        try:
            with open("Datos/paralelos.json", "r", encoding="utf-8") as f:
                self.paralelos = json.load(f)
        except FileNotFoundError:
            self.paralelos = []
        return self.paralelos
    
    def obtener_horario_paralelo(self, nombre_paralelo):
        for paralelo in self.paralelos:
            if paralelo["nombre"] == nombre_paralelo:
                return paralelo["horario"]
        return None
    
    def mostrar_horario_paralelo(self, nombre_paralelo):
        horario = self.obtener_horario_paralelo(nombre_paralelo.nombre)
        if not horario or not horario.get("materias"):
            print(f"No se encontró horario para el paralelo {nombre_paralelo.nombre}")
            return
        
        print(f"\nHorario del paralelo {nombre_paralelo.nombre}")
        print("=" * 40)
        for materia_info in horario["materias"]:
            print(f"{materia_info['hora']} - {materia_info['materia']} - Docente: {materia_info['docente']}")
    
    def _guardar_en_archivo(self):
        with open("Datos/paralelos.json", "w", encoding="utf-8") as f:
            json.dump(self.paralelos, f, ensure_ascii=False, indent=4)