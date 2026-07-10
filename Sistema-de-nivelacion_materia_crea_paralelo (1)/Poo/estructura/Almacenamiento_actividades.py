# Aqui se implementa el Modelo (MVC)
# Aqui se hizo manejo de actividades, entregas y calificaciones
import os
import shutil
from datetime import datetime
from estructura.facade_json import Facada_json
from estructura.Almacenamiento_calificaciones import Almacenamiento_Calificaciones


class Almacenamiento_Actividades:
    def __init__(self):
        self.actividades = Facada_json("Datos/actividades.json")
        self.entregas = Facada_json("Datos/entregas.json")
        carpeta_estructura = os.path.dirname(os.path.abspath(__file__))
        carpeta_poo = os.path.dirname(carpeta_estructura)
        self.carpeta_proyecto = os.path.dirname(carpeta_poo)
        self.carpeta_entregas = os.path.join(self.carpeta_proyecto, "Entregas")
        os.makedirs(self.carpeta_entregas, exist_ok=True)

    @staticmethod
    def _parse_fecha(valor):
        valor = str(valor or "").strip()
        for formato in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(valor, formato)
            except ValueError:
                pass
        return None

    def crear_actividad(self, docente, paralelo_id, materia, segmento, nombre, descripcion, fecha_limite, fecha_cierre):
        nombre = nombre.strip()
        if not all([paralelo_id, materia, segmento, nombre, fecha_limite, fecha_cierre]):
            return False, "Complete todos los campos obligatorios."
        limite = self._parse_fecha(fecha_limite)
        cierre = self._parse_fecha(fecha_cierre)
        if not limite or not cierre:
            return False, "Use fechas AAAA-MM-DD HH:MM."
        if cierre < limite:
            return False, "La fecha de cierre no puede ser anterior a la fecha limite."

        datos = self.actividades.repo.leer_todo()
        if any(a.get("paralelo_id") == paralelo_id and a.get("materia") == materia and a.get("nombre", "").lower() == nombre.lower() for a in datos):
            return False, "Ya existe una actividad con ese nombre en la materia."
        nuevo_id = f"ACT-{len(datos)+1:04d}"
        datos.append({
            "id": nuevo_id,
            "docente": docente,
            "paralelo_id": paralelo_id,
            "materia": materia,
            "segmento": segmento,
            "nombre": nombre,
            "descripcion": descripcion.strip(),
            "fecha_limite": fecha_limite.strip(),
            "fecha_cierre": fecha_cierre.strip(),
            "creada_en": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        if self.actividades.repo.guardar_todo(datos):
            return True, f"Actividad creada con codigo {nuevo_id}."
        return False, "No se pudo guardar la actividad."

    def listar_actividades_docente(self, cedula_docente, paralelo_id=None, materia=None):
        salida = []
        for a in self.actividades.repo.leer_todo():
            if a.get("docente") != cedula_docente:
                continue
            if paralelo_id and a.get("paralelo_id") != paralelo_id:
                continue
            if materia and a.get("materia") != materia:
                continue
            salida.append(a)
        return salida

    def listar_actividades_estudiante(self, cedula_estudiante):
        from estructura.Almacenamiento_horario import GuardarHorarios
        paralelos = GuardarHorarios().obtener_horario_estudiante(cedula_estudiante)
        ids = {p.get("id") for p in paralelos}
        entregas = {e.get("actividad_id"): e for e in self.entregas.repo.leer_todo() if e.get("cedula_estudiante") == cedula_estudiante}
        salida = []
        for actividad in self.actividades.repo.leer_todo():
            if actividad.get("paralelo_id") not in ids:
                continue
            paralelo = next((p for p in paralelos if p.get("id") == actividad.get("paralelo_id")), None)
            if not paralelo or actividad.get("materia") not in paralelo.get("materias", []):
                continue
            item = actividad.copy()
            item["entrega"] = entregas.get(actividad.get("id"))
            item["estado_plazo"] = self.estado_plazo(actividad)
            salida.append(item)
        return sorted(salida, key=lambda x: x.get("fecha_cierre", ""))

    def obtener_actividad(self, actividad_id):
        return next((a for a in self.actividades.repo.leer_todo() if a.get("id") == actividad_id), None)

    def estado_plazo(self, actividad, momento=None):
        momento = momento or datetime.now()
        limite = self._parse_fecha(actividad.get("fecha_limite"))
        cierre = self._parse_fecha(actividad.get("fecha_cierre"))
        if cierre and momento > cierre:
            return "Cerrada"
        if limite and momento > limite:
            return "Con atraso"
        return "Puntual"

    def subir_entrega(self, actividad_id, cedula_estudiante, ruta_archivo):
        actividad = self.obtener_actividad(actividad_id)
        if not actividad:
            return False, "Actividad no encontrada."
        estado = self.estado_plazo(actividad)
        if estado == "Cerrada":
            return False, "La actividad ya esta cerrada y no admite entregas."
        if not ruta_archivo or not os.path.isfile(ruta_archivo):
            return False, "Seleccione un archivo valido."

        extension = os.path.splitext(ruta_archivo)[1]
        nombre_seguro = f"{actividad_id}_{cedula_estudiante}{extension}"
        carpeta_actividad = os.path.join(self.carpeta_entregas, actividad_id)
        os.makedirs(carpeta_actividad, exist_ok=True)
        destino = os.path.join(carpeta_actividad, nombre_seguro)
        shutil.copy2(ruta_archivo, destino)
        ruta_relativa = os.path.relpath(destino, self.carpeta_proyecto)

        datos = self.entregas.repo.leer_todo()
        registro = next((e for e in datos if e.get("actividad_id") == actividad_id and e.get("cedula_estudiante") == cedula_estudiante), None)
        nuevo = {
            "actividad_id": actividad_id,
            "cedula_estudiante": cedula_estudiante,
            "archivo": ruta_relativa,
            "nombre_original": os.path.basename(ruta_archivo),
            "fecha_entrega": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "estado_entrega": estado,
            "nota": registro.get("nota") if registro else None,
            "observacion": registro.get("observacion", "") if registro else "",
        }
        if registro:
            registro.update(nuevo)
        else:
            datos.append(nuevo)
        return self.entregas.repo.guardar_todo(datos), f"Trabajo subido: {estado}."

    def entregas_actividad(self, actividad_id, estudiantes):
        entregas = {(e.get("actividad_id"), e.get("cedula_estudiante")): e for e in self.entregas.repo.leer_todo()}
        return [{"cedula": cedula, "entrega": entregas.get((actividad_id, cedula))} for cedula in estudiantes]

    def calificar_entrega(self, actividad_id, cedula_estudiante, nota, observacion=""):
        try:
            nota = float(nota)
        except ValueError:
            return False, "La nota debe ser numerica."
        if nota < 0 or nota > 10:
            return False, "La nota debe estar entre 0 y 10."
        actividad = self.obtener_actividad(actividad_id)
        if not actividad:
            return False, "Actividad no encontrada."
        datos = self.entregas.repo.leer_todo()
        entrega = next((e for e in datos if e.get("actividad_id") == actividad_id and e.get("cedula_estudiante") == cedula_estudiante), None)
        # Aqui el profesor puede calificar aunque el estudiante no haya subido archivo.
        if not entrega:
            entrega = {
                "actividad_id": actividad_id,
                "cedula_estudiante": cedula_estudiante,
                "archivo": "",
                "nombre_original": "",
                "fecha_entrega": "",
                "estado_entrega": "Sin archivo",
            }
            datos.append(entrega)
        entrega["nota"] = nota
        entrega["observacion"] = observacion.strip()
        entrega["calificada_en"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not self.entregas.repo.guardar_todo(datos):
            return False, "No se pudo guardar la calificacion."

        # La misma nota alimenta el promedio del segmento y la nota final de la materia.
        Almacenamiento_Calificaciones().registrar_actividad(
            cedula_estudiante,
            actividad.get("materia"),
            actividad.get("segmento"),
            actividad.get("nombre"),
            nota,
            actividad.get("docente"),
            entrega.get("calificada_en"),
            actividad.get("paralelo_id", ""),
        )
        return True, "Actividad calificada y promedio actualizado."

    def ruta_absoluta_archivo(self, entrega):
        if not entrega or not entrega.get("archivo"):
            return ""
        return os.path.join(self.carpeta_proyecto, entrega.get("archivo"))
