# Aqui se implementa el Modelo (MVC)
# estructura/Almacenamiento_calificaciones.py
from estructura.facade_json import Facada_json
from estructura.Almacenamiento_evaluaciones import Almacenamiento_Evaluaciones


class Almacenamiento_Calificaciones:
    def __init__(self):
        self.ruta = "Datos/calificaciones.json"
        self.json = Facada_json(self.ruta)
        self.evaluaciones = Almacenamiento_Evaluaciones()

    def _calcular_promedios(self, registro):
        # Aqui se hizo Calculo de promedio por segmento
        config = self.evaluaciones.obtener_configuracion()
        segmentos_cfg = {s["nombre"]: s for s in config.get("segmentos", [])}
        actividades = registro.get("actividades", [])
        resumen = {}
        nota_final = 0

        for nombre, segmento in segmentos_cfg.items():
            notas = [float(a.get("nota", 0)) for a in actividades if a.get("segmento") == nombre]
            promedio_10 = round(sum(notas) / len(notas), 2) if notas else 0
            valor_segmento = float(segmento.get("valor", 0))
            aporte = round((promedio_10 / 10) * valor_segmento, 2)
            resumen[nombre] = {
                "promedio_10": promedio_10,
                "valor_segmento": valor_segmento,
                "aporte": aporte,
                "cantidad_actividades": len(notas),
            }
            nota_final += aporte

        registro["resumen_segmentos"] = resumen
        registro["nota_final"] = round(nota_final, 2)
        registro["aprobado"] = registro["nota_final"] >= 7
        return registro

    def registrar_actividad(self, cedula_estudiante, nombre_materia, segmento, actividad, nota, cedula_docente, fecha, paralelo_id=""):
        # Aqui se hizo Metodo para registrar actividades por segmento
        nota = float(nota)
        if nota < 0 or nota > 10:
            return False, "La nota debe estar entre 0 y 10."

        datos = self.json.repo.leer_todo()
        registro = None
        for item in datos:
            if item.get("cedula_estudiante") == cedula_estudiante and item.get("materia") == nombre_materia and item.get("paralelo_id", "") == paralelo_id:
                registro = item
                break

        if registro is None:
            registro = {
                "cedula_estudiante": cedula_estudiante,
                "materia": nombre_materia,
                "paralelo_id": paralelo_id,
                "docente": cedula_docente,
                "actividades": [],
            }
            datos.append(registro)

        actividades = registro.setdefault("actividades", [])
        nueva = {
            "segmento": segmento,
            "actividad": actividad,
            "nota": nota,
            "fecha": fecha,
        }

        # Si ya existe la misma actividad dentro del segmento, se actualiza.
        actualizada = False
        for item in actividades:
            if item.get("segmento") == segmento and item.get("actividad") == actividad:
                item.update(nueva)
                actualizada = True
                break
        if not actualizada:
            actividades.append(nueva)

        self._calcular_promedios(registro)
        return self.json.repo.guardar_todo(datos), "Actividad guardada y promedio recalculado."

    # Compatibilidad con la forma antigua de guardar una sola nota.
    def registrar_nota(self, cedula_estudiante, nombre_materia, nota, cedula_docente, fecha):
        return self.registrar_actividad(cedula_estudiante, nombre_materia, "Evaluacion final", "Nota general", nota, cedula_docente, fecha)

    def obtener_notas_estudiante(self, cedula_estudiante):
        datos = self.json.repo.leer_todo()
        salida = [self._calcular_promedios(d) for d in datos if d.get("cedula_estudiante") == cedula_estudiante]
        self.json.repo.guardar_todo(datos)
        return salida

    def obtener_notas_registradas_por_docente(self, cedula_docente):
        datos = self.json.repo.leer_todo()
        return [self._calcular_promedios(d) for d in datos if d.get("docente") == cedula_docente]
