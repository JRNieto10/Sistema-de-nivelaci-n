# Aqui se implementa el Modelo (MVC)
from estructura.facade_json import Facada_json


class GuardarHorarios:
    def __init__(self):
        self.ruta_paralelos = "Datos/paralelos.json"
        self.json = Facada_json(self.ruta_paralelos)

    def _serializar(self, paralelo_objeto):
        horario_obj = paralelo_objeto.horario
        return {
            "id": paralelo_objeto.id,
            "nombre": paralelo_objeto.paralelo,
            "jornada": paralelo_objeto.jornada,
            "materia": getattr(paralelo_objeto, "materia", None),
            "materias": getattr(paralelo_objeto, "materias", []),
            "docente_cedula": getattr(paralelo_objeto, "docente_cedula", None),
            "horario": {
                "dia": horario_obj.dia,
                "hora_inicio": horario_obj.hora_inicio,
                "hora_fin": horario_obj.hora_fin,
                "aula": horario_obj.aula,
            } if horario_obj else None,
            "estudiantes": [
                e.cedula if hasattr(e, "cedula") else e for e in paralelo_objeto.estudiantes
            ],
        }

    def guardar_paralelo(self, paralelo_objeto):
        """Guarda un paralelo nuevo, o actualiza uno existente con el mismo id."""
        nuevo = self._serializar(paralelo_objeto)
        datos = self.json.repo.leer_todo()

        for i, item in enumerate(datos):
            if item["id"] == nuevo["id"]:
                datos[i] = nuevo
                return self.json.repo.guardar_todo(datos)

        datos.append(nuevo)
        return self.json.repo.guardar_todo(datos)

    # Compatibilidad con la firma antigua que recibía una lista de paralelos
    def guardar_paralelos(self, paralelos):
        exito = True
        for paralelo in paralelos:
            exito = self.guardar_paralelo(paralelo) and exito
        return exito

    def listar_paralelos(self):
        return self.json.repo.leer_todo()

    def obtener_paralelo(self, id_paralelo):
        for p in self.listar_paralelos():
            if p["id"] == id_paralelo:
                return p
        return None

    def agregar_materia_a_paralelo(self, id_paralelo, nombre_materia):
        """Permite que un paralelo tenga varias materias asignadas."""
        datos = self.json.repo.leer_todo()
        nombre_materia = str(nombre_materia).strip()

        for p in datos:
            if p["id"] == id_paralelo:
                if "materias" not in p or not isinstance(p["materias"], list):
                    p["materias"] = []

                if nombre_materia in p["materias"]:
                    return False, "La materia ya está asignada a este paralelo."

                p["materias"].append(nombre_materia)

                # Compatibilidad con pantallas antiguas que leen solo 'materia'.
                if not p.get("materia"):
                    p["materia"] = nombre_materia

                self.json.repo.guardar_todo(datos)
                return True, "Materia asignada al paralelo."

        return False, "Paralelo no encontrado."


    def asignar_docente_a_materia(self, id_paralelo, nombre_materia, cedula_docente):
        """Asigna un docente a una materia específica dentro de un paralelo."""
        datos = self.json.repo.leer_todo()
        nombre_materia = str(nombre_materia).strip()
        cedula_docente = str(cedula_docente).strip()

        for p in datos:
            if p.get("id") == id_paralelo:
                materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
                if nombre_materia not in materias:
                    return False, "La materia no pertenece a este paralelo."

                p.setdefault("docentes_por_materia", {})
                p["docentes_por_materia"][nombre_materia] = cedula_docente

                # Compatibilidad con pantallas antiguas: si el paralelo solo tiene una materia, se guarda también aquí.
                if len(materias) == 1:
                    p["docente_cedula"] = cedula_docente

                self.json.repo.guardar_todo(datos)
                return True, "Docente matriculado correctamente."

        return False, "Paralelo no encontrado."

    def _hay_choque(self, h1, h2):
        if not h1 or not h2:
            return False
        if h1.get("dia") != h2.get("dia"):
            return False
        return (h1.get("hora_inicio") < h2.get("hora_fin")) and (h2.get("hora_inicio") < h1.get("hora_fin"))

    def _docente_ocupado(self, datos, id_actual, cedula_docente, horario_nuevo):
        if not cedula_docente:
            return False
        for otro in datos:
            if otro.get("id") == id_actual:
                continue
            asignaciones = otro.get("docentes_por_materia", {})
            horarios = otro.get("horarios_por_materia", {})
            for materia, docente in asignaciones.items():
                if docente == cedula_docente and self._hay_choque(horario_nuevo, horarios.get(materia)):
                    return True
            if otro.get("docente_cedula") == cedula_docente and self._hay_choque(horario_nuevo, otro.get("horario")):
                return True
        return False

    def generar_horarios_paralelo(self, id_paralelo):
        # Aqui se hizo Validacion de choques de horarios
        # Genera horarios para todas las materias del paralelo y evita que un docente choque con otro paralelo.
        datos = self.json.repo.leer_todo()
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        franjas = {
            "Matutina": [("07:00", "09:00"), ("09:00", "11:00"), ("11:00", "13:00")],
            "Vespertina": [("14:00", "16:00"), ("16:00", "18:00"), ("18:00", "20:00")],
            "Nocturna": [("18:00", "20:00"), ("20:00", "22:00")],
        }

        for p in datos:
            if p.get("id") == id_paralelo:
                materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
                if not materias:
                    return False, "Este paralelo no tiene materias asignadas."

                jornada = p.get("jornada", "Matutina")
                bloques = franjas.get(jornada, franjas["Matutina"])
                asignaciones = p.get("docentes_por_materia", {})
                horarios = {}

                for materia in materias:
                    ced_docente = asignaciones.get(materia) or p.get("docente_cedula")
                    colocado = False
                    for dia in dias:
                        for inicio, fin in bloques:
                            candidato = {
                                "dia": dia,
                                "hora_inicio": inicio,
                                "hora_fin": fin,
                                "aula": f"Aula {len(horarios) + 1}",
                                "jornada": jornada,
                            }
                            # No repetir bloque dentro del mismo paralelo.
                            if any(self._hay_choque(candidato, h) for h in horarios.values()):
                                continue
                            # No chocar con el mismo docente en otros paralelos de la misma jornada.
                            if self._docente_ocupado(datos, id_paralelo, ced_docente, candidato):
                                continue
                            horarios[materia] = candidato
                            colocado = True
                            break
                        if colocado:
                            break
                    if not colocado:
                        return False, f"No hay bloque disponible para {materia} sin choque de docente."

                p["horarios_por_materia"] = horarios
                primera = materias[0]
                p["horario"] = horarios[primera]
                self.json.repo.guardar_todo(datos)
                return True, "Horarios generados correctamente sin choque de docente."

        return False, "Paralelo no encontrado."

    def _generar_codigo_paralelo(self, datos=None):
        # Aqui se hizo generacion automatica del codigo del paralelo
        datos = datos if datos is not None else self.json.repo.leer_todo()
        numeros = []
        for p in datos:
            codigo = str(p.get("id", ""))
            if codigo.startswith("PAR-"):
                try:
                    numeros.append(int(codigo.split("-")[-1]))
                except ValueError:
                    pass
        return f"PAR-{(max(numeros, default=0) + 1):03d}"

    def crear_paralelo_para_materia(self, nombre_paralelo, jornada, nombre_materia, id_paralelo=None):
        # Aqui se hizo Relacion entre clases: Materia -> Paralelo
        # El codigo ya no se escribe, el sistema lo genera automaticamente.
        from estructura.paralelo import Paralelo

        datos = self.json.repo.leer_todo()
        id_paralelo = id_paralelo or self._generar_codigo_paralelo(datos)
        if any(p.get("id") == id_paralelo for p in datos):
            return False, "Ya existe un paralelo con ese codigo."
        nuevo = Paralelo(id_paralelo, nombre_paralelo, jornada, None)
        nuevo.materia = nombre_materia
        nuevo.materias = [nombre_materia]
        self.guardar_paralelo(nuevo)
        return True, f"Paralelo creado con codigo {id_paralelo}."

    def _materias_paralelo(self, paralelo):
        return paralelo.get("materias") or ([] if not paralelo.get("materia") else [paralelo.get("materia")])

    def _estudiantes_materia(self, paralelo, materia):
        matriculas = paralelo.get("matriculas_por_materia", {})
        if materia in matriculas:
            return matriculas.get(materia, [])
        # Compatibilidad con datos antiguos: si el paralelo solo tiene una materia,
        # los estudiantes antiguos pertenecen a esa materia.
        materias = self._materias_paralelo(paralelo)
        if len(materias) == 1 and materia in materias:
            return paralelo.get("estudiantes", [])
        return []

    def estudiantes_de_materia(self, id_paralelo, materia):
        paralelo = self.obtener_paralelo(id_paralelo)
        return self._estudiantes_materia(paralelo or {}, materia)

    def _horario_materia(self, paralelo, materia):
        horarios = paralelo.get("horarios_por_materia", {})
        if materia in horarios:
            return horarios.get(materia)
        materias = self._materias_paralelo(paralelo)
        if len(materias) == 1 and materia in materias:
            return paralelo.get("horario")
        return None

    def inscribir_estudiante(self, id_paralelo, cedula_estudiante, materia):
        """Matricula al estudiante en un solo paralelo por materia y evita choques."""
        datos = self.json.repo.leer_todo()
        paralelo_destino = next((p for p in datos if p.get("id") == id_paralelo), None)
        if not paralelo_destino:
            return False, "Paralelo no encontrado."

        materia = str(materia or "").strip()
        if materia not in self._materias_paralelo(paralelo_destino):
            return False, "La materia no pertenece al paralelo seleccionado."

        if cedula_estudiante in self._estudiantes_materia(paralelo_destino, materia):
            return False, "Ya esta matriculado en este paralelo para la materia."

        # Aqui se valido un solo paralelo por materia.
        for otro in datos:
            if cedula_estudiante in self._estudiantes_materia(otro, materia):
                return False, f"Ya esta matriculado en {materia} dentro del paralelo '{otro.get('nombre')}'."

        horario_nuevo = self._horario_materia(paralelo_destino, materia)
        if not horario_nuevo:
            return False, "La materia seleccionada todavia no tiene horario generado."

        # Aqui se hizo validacion para que las materias del estudiante no choquen.
        for otro in datos:
            for otra_materia in self._materias_paralelo(otro):
                if cedula_estudiante not in self._estudiantes_materia(otro, otra_materia):
                    continue
                otro_horario = self._horario_materia(otro, otra_materia)
                if self._hay_choque(horario_nuevo, otro_horario):
                    return False, (
                        f"No se puede matricular porque el horario de {materia} choca "
                        f"con {otra_materia} del paralelo '{otro.get('nombre')}'."
                    )

        paralelo_destino.setdefault("matriculas_por_materia", {})
        paralelo_destino["matriculas_por_materia"].setdefault(materia, []).append(cedula_estudiante)
        # Lista general para mantener compatibilidad con otras pantallas.
        paralelo_destino.setdefault("estudiantes", [])
        if cedula_estudiante not in paralelo_destino["estudiantes"]:
            paralelo_destino["estudiantes"].append(cedula_estudiante)
        self.json.repo.guardar_todo(datos)
        return True, f"Matricula exitosa en {materia}, paralelo {paralelo_destino.get('nombre')}."

    def obtener_horario_estudiante(self, cedula_estudiante):
        # Devuelve solo las materias en las que realmente esta matriculado.
        resultado = []
        for p in self.listar_paralelos():
            materias_inscritas = [
                m for m in self._materias_paralelo(p)
                if cedula_estudiante in self._estudiantes_materia(p, m)
            ]
            if not materias_inscritas:
                continue
            copia = dict(p)
            copia["materias"] = materias_inscritas
            copia["horarios_por_materia"] = {
                m: self._horario_materia(p, m) for m in materias_inscritas
            }
            resultado.append(copia)
        return resultado
