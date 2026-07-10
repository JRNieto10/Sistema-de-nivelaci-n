# Aqui se implementa el Modelo (MVC)
# estructura/entidades.py
class Materia:
    def __init__(self, id_materia, nombre, creditos, id_carrera_asociada):
        self.id_materia = id_materia
        self.nombre = nombre
        self.creditos = creditos
        self.id_carrera = id_carrera_asociada # Aquí guardamos la relación


class Carrera:
    def __init__(self, id_carrera, nombre, duracion):
        self.id_carrera = id_carrera  # <--- Este es el nombre real
        self.nombre = nombre
        self.duracion = duracion
        self.materias = []  # 🔧 CORREGIDO: antes no se inicializaba y agregar_materia() fallaba

    def agregar_materia(self, materia_objeto):
        """Recibe un objeto de la clase Materia y lo añade a la lista"""
        self.materias.append(materia_objeto)