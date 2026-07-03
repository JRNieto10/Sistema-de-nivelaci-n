import json
import os

class horariodocentealmacenar:
    def __init__(self):
        self.ruta_horarios_docentes = "Datos/horarios_docentes.json"
        if not os.path.exists("Datos"):
            os.makedirs("Datos")
            
    #lo que haremos en primero desde la lista cursos obtener cada curso con sus materias solo si coincide con el nombre del docente, guarda todo eso de los cursos en un diccionario y lo guardamos para el hoario de un docente con esta estructura como una estructura como esta con los datos que tengamos {
#     "docentes": [
#         {
#             "cedula": "111111111",
#             "nombre": "pepito",
#             "apellido": "garcia",
#             "correo": "pepito@uleam.edu",
#             "contrasena": "pepito123",
#             "rol": "docente",
#             "especialidad": "Programacion",
#             "titulo": "Ingeniero en Sistemas",
#             "fecha_contratacion": "2024-01-15",
#             "estado": "activo",
#             "cursos_asignados": [
#                 {
#                     "curso": "Tercero A",
#                     "materias": ["POO", "Estructura"]
#                 },
#                 {
#                     "curso": "Tercero B",
#                     "materias": ["POO"]
#                 }
#             ],
#             "horario": {
#                 "lunes": ["07:00-09:00", "14:00-16:00"],
#                 "martes": ["09:00-11:00"],
#                 "miercoles": [],
#                 "jueves": ["14:00-16:00"],
#                 "viernes": ["07:00-09:00"]
#             },
#             "telefono": "0987654321",
#             "direccion": "Calle Principal #123"
#         }
#     ]
# }

    def guardar_horario_docente(self, docente, cursos):
        # Crear un diccionario para almacenar la información del docente
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

        # Agregar los cursos y materias asignadas al docente
        for curso in cursos:
            materias_asignadas = curso.obtener_materias_por_docente(docente)
            if materias_asignadas:
                curso_info = {
                    "curso": curso.nombre,
                    "materias": materias_asignadas
                }
                docente_info["cursos_asignados"].append(curso_info)

        # Leer los datos existentes del archivo JSON
        if os.path.exists(self.ruta_horarios_docentes):
            with open(self.ruta_horarios_docentes, 'r') as archivo:
                try:
                    datos_existentes = json.load(archivo)
                    # Si es una lista, convertir a diccionario
                    if isinstance(datos_existentes, list):
                        datos_existentes = {"docentes": datos_existentes}
                except json.JSONDecodeError:
                    datos_existentes = {"docentes": []}
        else:
            datos_existentes = {"docentes": []}

        # Asegurarse de que la clave "docentes" existe
        if "docentes" not in datos_existentes:
            datos_existentes["docentes"] = []

        # Verificar si el docente ya existe en los datos existentes
        for i, d in enumerate(datos_existentes["docentes"]):
            if d["cedula"] == docente.cedula:
                # Actualizar la información del docente existente
                datos_existentes["docentes"][i] = docente_info
                break
        else:
            # Si el docente no existe, agregarlo a la lista
            datos_existentes["docentes"].append(docente_info)

        # Guardar los datos actualizados en el archivo JSON
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
            print(f"Horario del docente {docente['nombre']} {docente['apellido']} (Cédula: {docente['cedula']}):")
            for dia, clases in docente["horario"].items():
                print(f"{dia.capitalize()}: {', '.join(clases) if clases else 'No tiene clases asignadas'}")
        else:
            print(f"No se encontró un docente con la cédula {cedula}.")