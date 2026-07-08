import json
import os

class horariodocentealmacenar:
    def __init__(self):
        self.ruta_horarios_docentes = "Datos/horarios_docentes.json"
        if not os.path.exists("Datos"):
            os.makedirs("Datos")

    def guardar_horario_docente(self, docente, cursos):
        docente_info = {
            "cedula": docente.cedula,
            "nombre": docente.nombre,
            "apellido": docente.apellido,
            "correo": docente.correo,
            "contrasena": docente.contrasena,
            "rol": docente.rol,
            "especialidad": getattr(docente, 'especialidad', ''),
            "titulo": getattr(docente, 'titulo', ''),
            "fecha_contratacion": getattr(docente, 'fecha_contratacion', ''),
            "estado": getattr(docente, 'estado', ''),
            "cursos_asignados": [],
            "horario": docente.horario,
            "telefono": getattr(docente, 'telefono', ''),
            "direccion": getattr(docente, 'direccion', '')
        }

        for curso in cursos:
            materias_asignadas = curso.obtener_materias_por_docente(docente)
            if materias_asignadas:
                curso_info = {
                    "curso": curso.nombre,
                    "materias": materias_asignadas
                }
                docente_info["cursos_asignados"].append(curso_info)

        if os.path.exists(self.ruta_horarios_docentes):
            with open(self.ruta_horarios_docentes, 'r') as archivo:
                try:
                    datos_existentes = json.load(archivo)
                    if isinstance(datos_existentes, list):
                        datos_existentes = {"docentes": datos_existentes}
                except json.JSONDecodeError:
                    datos_existentes = {"docentes": []}
        else:
            datos_existentes = {"docentes": []}

        if "docentes" not in datos_existentes:
            datos_existentes["docentes"] = []

        for i, d in enumerate(datos_existentes["docentes"]):
            if d["cedula"] == docente.cedula:
                datos_existentes["docentes"][i] = docente_info
                break
        else:
            datos_existentes["docentes"].append(docente_info)

        with open(self.ruta_horarios_docentes, 'w') as archivo:
            json.dump(datos_existentes, archivo, indent=4)
    
    def obtener_horario_docente(self, cedula):
        if os.path.exists(self.ruta_horarios_docentes):
            with open(self.ruta_horarios_docentes, 'r') as archivo:
                try:
                    datos = json.load(archivo)
                    for docente in datos.get("docentes", []):
                        if docente["cedula"] == cedula:
                            return docente
                except json.JSONDecodeError:
                    return None
        return None
    
    def eliminar_horario_docente(self, cedula):
        if os.path.exists(self.ruta_horarios_docentes):
            with open(self.ruta_horarios_docentes, 'r') as archivo:
                try:
                    datos = json.load(archivo)
                    datos["docentes"] = [docente for docente in datos.get("docentes", []) if docente["cedula"] != cedula]
                except json.JSONDecodeError:
                    return False

            with open(self.ruta_horarios_docentes, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
            return True
        return False
    
    def mostrar_horario_docente(self, cedula):
        docente = self.obtener_horario_docente(cedula)
        if docente:
            return docente
        return None