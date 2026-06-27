import json
with open('Datos/permitidos.json', 'r', encoding='utf-8') as archivo:
    permitidos = json.load(archivo)
class encontrar_cedula:
    def __init__(self, cedula):
        self.cedula = cedula


    def buscar_cedula(self):
        if self.cedula in permitidos["cedulas_estudiantes"]:
            return "Estudiante"
        elif self.cedula in permitidos["cedulas_docentes"]:
            return "Docente"
        elif self.cedula in permitidos["cedulas_personal"]:
            return "Personal"
        else:
            return "No encontrada"
