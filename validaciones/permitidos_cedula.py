import json
with open('Datos/permitidos.json', 'r', encoding='utf-8') as archivo:
    permitidos = json.load(archivo)
class encontrar_cedula:
    def __init__(self, cedula, rol):
        self.cedula = cedula
        self.rol = rol



    def buscar_cedula(self):
        if self.rol == "Estudiante":
            if self.cedula in permitidos["cedulas_estudiantes"]:
                return "Estudiante"
            else:
                return "No encontrada"
        elif self.rol == "Docente":
            if self.cedula in permitidos["cedulas_docentes"]:
                return "Docente"
            else:
                return "No encontrada"
        elif self.rol == "Administrador":
            if self.cedula in permitidos["cedulas_personal"]:
                return "Personal"
            else:
                return "No encontrada"
        else:
            return "Rol no válido"
