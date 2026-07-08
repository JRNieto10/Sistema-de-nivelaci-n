import json
import os

class horariodocentealmacenar:
    def __init__(self):
        self.ruta_horarios_docentes = "Datos/horarios_docentes.json"
        if not os.path.exists("Datos"):
            os.makedirs("Datos")

    def guardar_horario_docente(self, docente, cursos):
        # Obtener el nombre del docente para comparar
        nombre_docente = docente.nombre
        
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
            "telefono": getattr(docente, 'telefono', ''),
            "direccion": getattr(docente, 'direccion', '')
        }

        # Procesar cada curso para ver qué materias tiene este docente
        for curso in cursos:
            materias_del_curso = []
            # Verificar si el curso tiene el método obtener_materias_por_docente
            if hasattr(curso, 'obtener_materias_por_docente'):
                # Pasar el NOMBRE del docente, no el objeto
                materias_asignadas = curso.obtener_materias_por_docente(nombre_docente)
                if materias_asignadas:
                    curso_info = {
                        "curso": curso.nombre,
                        "materias": materias_asignadas
                    }
                    docente_info["cursos_asignados"].append(curso_info)
            else:
                # Si no tiene el método, construir manualmente
                if hasattr(curso, 'materias') and curso.materias:
                    for materia_nombre, info in curso.materias.items():
                        if nombre_docente in info.get("docentes", []):
                            materias_del_curso.append(materia_nombre)
                    if materias_del_curso:
                        curso_info = {
                            "curso": curso.nombre,
                            "materias": materias_del_curso
                        }
                        docente_info["cursos_asignados"].append(curso_info)

        # Guardar en el archivo JSON
        if os.path.exists(self.ruta_horarios_docentes):
            with open(self.ruta_horarios_docentes, 'r', encoding='utf-8') as archivo:
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

        # Actualizar o agregar el docente
        encontrado = False
        for i, d in enumerate(datos_existentes["docentes"]):
            if d["cedula"] == docente.cedula:
                datos_existentes["docentes"][i] = docente_info
                encontrado = True
                break
        
        if not encontrado:
            datos_existentes["docentes"].append(docente_info)

        with open(self.ruta_horarios_docentes, 'w', encoding='utf-8') as archivo:
            json.dump(datos_existentes, archivo, indent=4, ensure_ascii=False)
        
        print(f"Horario guardado para docente: {docente.nombre}")
        return True
    
    def obtener_horario_docente(self, cedula):
        if os.path.exists(self.ruta_horarios_docentes):
            with open(self.ruta_horarios_docentes, 'r', encoding='utf-8') as archivo:
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
            with open(self.ruta_horarios_docentes, 'r', encoding='utf-8') as archivo:
                try:
                    datos = json.load(archivo)
                    datos["docentes"] = [docente for docente in datos.get("docentes", []) if docente["cedula"] != cedula]
                except json.JSONDecodeError:
                    return False

            with open(self.ruta_horarios_docentes, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        return False
    
    def mostrar_horario_docente(self, cedula):
        docente = self.obtener_horario_docente(cedula)
        if docente:
            return docente
        return None