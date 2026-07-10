# Aqui se implementa el Modelo (MVC)
# estructura/Almacenamiento_tutorias.py
from estructura.facade_json import Facada_json


class Almacenamiento_Tutorias:
    def __init__(self):
        self.ruta = "Datos/tutorias.json"
        self.json = Facada_json(self.ruta)

    def guardar_tutoria(self, tutoria_objeto):
        # Si un estudiante es obligatorio, queda inscrito automaticamente en la tutoria.
        estudiantes = list(dict.fromkeys((getattr(tutoria_objeto, "estudiantes", []) or []) + (getattr(tutoria_objeto, "obligatorios", []) or [])))
        tutoria_dict = {
            "id": tutoria_objeto.id,
            "fecha": tutoria_objeto.fecha,
            "tema": tutoria_objeto.tema,
            "docente": tutoria_objeto.docente_cedula,
            "materia": getattr(tutoria_objeto, "materia", ""),
            "paralelo_id": getattr(tutoria_objeto, "paralelo_id", ""),
            "estado": tutoria_objeto.estado,
            "estudiantes": estudiantes,
            "obligatorios": getattr(tutoria_objeto, "obligatorios", []),
        }
        return self.json.guardar_datos("id", tutoria_dict)

    def obtener_tutorias_docente(self, cedula_docente):
        datos = self.json.repo.leer_todo()
        return [t for t in datos if t.get("docente") == cedula_docente]

    def obtener_tutorias_estudiante(self, cedula_estudiante):
        # Solo muestra tutorias de materias donde el estudiante esta matriculado o fue marcado obligatorio.
        datos = self.json.repo.leer_todo()
        from estructura.Almacenamiento_horario import GuardarHorarios
        paralelos_estudiante = GuardarHorarios().obtener_horario_estudiante(cedula_estudiante)
        ids_paralelos = {p.get("id") for p in paralelos_estudiante}
        materias_estudiante = set()
        for p in paralelos_estudiante:
            for m in p.get("materias") or ([] if not p.get("materia") else [p.get("materia")]):
                materias_estudiante.add(m)

        visibles = []
        for t in datos:
            # Aqui se hizo Tutoria obligatoria: el estudiante ya queda inscrito si fue seleccionado por el docente.
            if cedula_estudiante in t.get("obligatorios", []) and cedula_estudiante not in t.get("estudiantes", []):
                t.setdefault("estudiantes", []).append(cedula_estudiante)
            es_obligatorio = cedula_estudiante in t.get("obligatorios", [])
            misma_materia = t.get("materia") in materias_estudiante
            mismo_paralelo = not t.get("paralelo_id") or t.get("paralelo_id") in ids_paralelos
            if es_obligatorio or (misma_materia and mismo_paralelo):
                visibles.append(t)
        self.json.repo.guardar_todo(datos)
        return visibles

    def obtener_todas(self):
        return self.json.repo.leer_todo()

    def inscribir_estudiante(self, id_tutoria, cedula_estudiante):
        datos = self.json.repo.leer_todo()
        for t in datos:
            if t.get("id") == id_tutoria:
                # Aqui se hizo Validacion: solo estudiantes de esa materia pueden inscribirse.
                visibles = self.obtener_tutorias_estudiante(cedula_estudiante)
                if not any(v.get("id") == id_tutoria for v in visibles):
                    return False
                if cedula_estudiante in t.get("estudiantes", []):
                    return False
                t.setdefault("estudiantes", []).append(cedula_estudiante)
                return self.json.repo.guardar_todo(datos)
        return False
