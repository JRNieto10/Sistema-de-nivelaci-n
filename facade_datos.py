import json
import os
from estructura.Almacenamiento_horario import GuardarHorarios
from estructura.Almacenamiento_horario_docente import horariodocentealmacenar
from estructura.gest_permitidos import GestionPermitidos
from estructura.almacenamiento_curso import AlmacenamientoCursos
from estructura.almacenamiento_carreras import AlmacenamientoCarreras
from estructura.Almacenamieto import Almacenamiento_Usuarios

class FacadeDatos:
    def __init__(self):
        self._inicializar_subsistemas()
        self.lista_paralelos = []
        self.ruta_base = "Datos"
        self.almacenamiento_cursos = AlmacenamientoCursos()
        self.almacenamiento_carreras = AlmacenamientoCarreras()
        self.almacenamiento_usuarios = Almacenamiento_Usuarios()
        self._crear_directorios_archivos()

    def _inicializar_subsistemas(self):
        self.gestor_horarios = GuardarHorarios()
        self.gestor_horarios_docentes = horariodocentealmacenar()
        self.gestion_permitidos = GestionPermitidos()

    def _crear_directorios_archivos(self):
        if not os.path.exists(self.ruta_base):
            os.makedirs(self.ruta_base)
        archivos = [
            "Datos/estudiantes.json",
            "Datos/docentes.json",
            "Datos/personal_administrativo.json",
            "Datos/permitidos.json",
            "Datos/paralelos.json",
            "Datos/horarios_docentes.json",
            "Datos/carreras.json",
        ]
        for archivo in archivos:
            if not os.path.exists(archivo):
                with open(archivo, "w", encoding="utf-8") as f:
                    if "permitidos" in archivo:
                        json.dump(
                            {
                                "cedulas_estudiantes": [],
                                "cedulas_docentes": [],
                                "cedulas_personal": [],
                            },
                            f,
                            ensure_ascii=False,
                            indent=4,
                        )
                    elif "carreras" in archivo:
                        json.dump([], f, ensure_ascii=False, indent=4)
                    else:
                        json.dump([], f, ensure_ascii=False, indent=4)

    # Métodos para gestión de permitidos (usados por gestionar_permitidos.py)
    def agregar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.agregar_cedula(cedula, tipo)

    def eliminar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.eliminar_cedula(cedula, tipo)

    def verificar_cedula(self, cedula):
        return self.gestion_permitidos.verificar_cedula(cedula)

    def listar_cedulas(self):
        return self.gestion_permitidos.listar_cedulas()

    # Métodos para gestión de horarios (usados por otros módulos)
    def guardar_horario_docente(self, docente, cursos):
        if hasattr(docente, 'horario'):
            self.gestor_horarios_docentes.guardar_horario_docente(docente, cursos)

    def crear_horario_paralelo(self, curso, nombre_paralelo=None):
        from estructura.gestor_curso import Gestor_curso
        gestor_cursos = Gestor_curso()
        if nombre_paralelo is None:
            cantidad_paralelos = len([p for p in self.lista_paralelos if p.curso == curso])
            letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            letra = letras[cantidad_paralelos % len(letras)]
            nombre_paralelo = f"{curso.nombre}_{letra}"
        paralelo = gestor_cursos.crear_paralelo(nombre_paralelo, 1, curso)
        self.lista_paralelos.append(paralelo)
        self.gestor_horarios.guardar_paralelo(paralelo)
        return paralelo

    def mostrar_horario_paralelo(self, nombre_paralelo):
        self.gestor_horarios.mostrar_horario_paralelo(nombre_paralelo)

    def mostrar_horario_docente(self, docente):
        if hasattr(docente, 'horario'):
            for dia, clases in docente.horario.items():
                if clases:
                    for clase in clases:
                        print(f"{dia.upper()}: {clase['hora_inicio']} - {clase['hora_fin']} | Materia: {clase['materia']} | Paralelo: {clase['paralelo']} | Aula: {clase['aula']}")

    def mostrar_todos_los_paralelos(self):
        for paralelo in self.lista_paralelos:
            print(f"- {paralelo.nombre if hasattr(paralelo, 'nombre') else paralelo}")

    # Métodos para consulta de usuarios (usados por módulos de estudiantes)
    def obtener_estudiante(self, cedula):
        ruta_estudiantes = os.path.join(self.ruta_base, "estudiantes.json")
        if os.path.exists(ruta_estudiantes):
            try:
                with open(ruta_estudiantes, 'r', encoding='utf-8') as archivo:
                    estudiantes = json.load(archivo)
                    for est in estudiantes:
                        if est.get("cedula") == cedula:
                            return est
            except Exception:
                pass
        return None

    def obtener_docente(self, cedula):
        ruta_docentes = os.path.join(self.ruta_base, "docentes.json")
        if os.path.exists(ruta_docentes):
            try:
                with open(ruta_docentes, 'r', encoding='utf-8') as archivo:
                    docentes = json.load(archivo)
                    for doc in docentes:
                        if doc.get("cedula") == cedula:
                            return doc
            except Exception:
                pass
        return None

    def obtener_personal(self, cedula):
        ruta_personal = os.path.join(self.ruta_base, "personal_administrativo.json")
        if os.path.exists(ruta_personal):
            try:
                with open(ruta_personal, 'r', encoding='utf-8') as archivo:
                    personal = json.load(archivo)
                    for per in personal:
                        if per.get("cedula") == cedula:
                            return per
            except Exception:
                pass
        return None

    def obtener_usuario_por_cedula(self, cedula, rol):
        if rol == "estudiante":
            return self.obtener_estudiante(cedula)
        elif rol == "docente":
            return self.obtener_docente(cedula)
        elif rol == "personal":
            return self.obtener_personal(cedula)
        return None

    # Métodos para gestión de matrículas (usados por módulos de estudiantes)
    def cargar_estado_matricula(self, cedula):
        if not cedula:
            return None
        ruta_matricula = os.path.join(self.ruta_base, "matriculas", f"matricula_{cedula}.json")
        if os.path.exists(ruta_matricula):
            try:
                with open(ruta_matricula, 'r', encoding='utf-8') as archivo:
                    return json.load(archivo)
            except Exception:
                pass
        return None

    def guardar_estado_matricula(self, datos):
        cedula = datos.get("cedula")
        if not cedula:
            return
        ruta_matriculas = os.path.join(self.ruta_base, "matriculas")
        os.makedirs(ruta_matriculas, exist_ok=True)
        ruta_matricula = os.path.join(ruta_matriculas, f"matricula_{cedula}.json")
        try:
            with open(ruta_matricula, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
        except Exception:
            pass

    # Métodos de verificación de existencia (usados por módulos de estudiantes)
    def verificar_estudiante_existe(self, cedula):
        ruta_estudiantes = os.path.join(self.ruta_base, "estudiantes.json")
        if os.path.exists(ruta_estudiantes):
            try:
                with open(ruta_estudiantes, 'r', encoding='utf-8') as archivo:
                    estudiantes = json.load(archivo)
                    for est in estudiantes:
                        if est.get("cedula") == cedula:
                            return True
            except Exception:
                pass
        return False

    def verificar_docente_existe(self, cedula):
        ruta_docentes = os.path.join(self.ruta_base, "docentes.json")
        if os.path.exists(ruta_docentes):
            try:
                with open(ruta_docentes, 'r', encoding='utf-8') as archivo:
                    docentes = json.load(archivo)
                    for doc in docentes:
                        if doc.get("cedula") == cedula:
                            return True
            except Exception:
                pass
        return False

    def verificar_personal_existe(self, cedula):
        ruta_personal = os.path.join(self.ruta_base, "personal_administrativo.json")
        if os.path.exists(ruta_personal):
            try:
                with open(ruta_personal, 'r', encoding='utf-8') as archivo:
                    personal = json.load(archivo)
                    for per in personal:
                        if per.get("cedula") == cedula:
                            return True
            except Exception:
                pass
        return False

    def verificar_usuario_existe(self, cedula, rol):
        if rol == "estudiante":
            return self.verificar_estudiante_existe(cedula)
        elif rol == "docente":
            return self.verificar_docente_existe(cedula)
        elif rol == "personal":
            return self.verificar_personal_existe(cedula)
        return False

    # Métodos para búsqueda de paralelos (usados por módulos de estudiantes)
    def buscar_paralelos(self, carrera):
        paralelos = []
        ruta_carrera = os.path.join(self.ruta_base, carrera)
        if not os.path.exists(ruta_carrera):
            return paralelos
        for carpeta_curso in os.listdir(ruta_carrera):
            ruta_curso = os.path.join(ruta_carrera, carpeta_curso)
            if os.path.isdir(ruta_curso):
                ruta_paralelos_json = os.path.join(ruta_curso, "paralelos.json")
                if os.path.exists(ruta_paralelos_json):
                    try:
                        with open(ruta_paralelos_json, 'r', encoding='utf-8') as archivo:
                            datos = json.load(archivo)
                            if "paralelos" in datos and isinstance(datos["paralelos"], list):
                                for paralelo_data in datos["paralelos"]:
                                    paralelo_info = {
                                        "nombre": f"Curso {carpeta_curso} - Paralelo {paralelo_data.get('letra', '')}",
                                        "curso": carpeta_curso,
                                        "letra": paralelo_data.get("letra", ""),
                                        "aula": paralelo_data.get("aula", ""),
                                        "horario": paralelo_data.get("horario", ""),
                                        "materias": paralelo_data.get("materias", []),
                                        "ruta": ruta_curso,
                                        "datos": datos
                                    }
                                    paralelos.append(paralelo_info)
                    except Exception:
                        pass
        return paralelos

    def carrera_existe(self, carrera):
        ruta_carrera = os.path.join(self.ruta_base, carrera)
        return os.path.exists(ruta_carrera)

    # Métodos para carga de datos (usados por módulos de estudiantes y otros)
    def cargar_docentes_desde_json(self):
        try:
            ruta = os.path.join(self.ruta_base, "docentes.json")
            if not os.path.exists(ruta):
                return []
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def cargar_estudiantes_desde_json(self):
        try:
            ruta = os.path.join(self.ruta_base, "estudiantes.json")
            if not os.path.exists(ruta):
                return []
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def cargar_personal_desde_json(self):
        try:
            ruta = os.path.join(self.ruta_base, "personal_administrativo.json")
            if not os.path.exists(ruta):
                return []
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    # Métodos para guardado de cursos y carreras (usados por módulos de creación)
    def guardar_curso(self, carrera_nombre, curso_nombre, materias_con_docentes):
        return self.almacenamiento_cursos.guardar_curso(carrera_nombre, curso_nombre, materias_con_docentes)

    def cargar_curso(self, carrera_nombre, curso_nombre):
        return self.almacenamiento_cursos.cargar_curso(carrera_nombre, curso_nombre)

    def guardar_paralelos(self, carrera_nombre, curso_nombre, paralelos_data):
        return self.almacenamiento_cursos.guardar_paralelos(carrera_nombre, curso_nombre, paralelos_data)

    # Métodos para gestión de carreras (usados por facade.py)
    def guardar_carrera(self, carrera):
        return self.almacenamiento_carreras.guardar_carrera(carrera)

    def cargar_carrera(self, id_carrera):
        return self.almacenamiento_carreras.cargar_carrera(id_carrera)

    def cargar_todas_carreras(self):
        return self.almacenamiento_carreras.cargar_todas_carreras()

    def eliminar_carrera(self, id_carrera):
        return self.almacenamiento_carreras.eliminar_carrera(id_carrera)

    def agregar_asignatura_a_carrera(self, id_carrera, asignatura):
        return self.almacenamiento_carreras.agregar_asignatura_a_carrera(id_carrera, asignatura)

    def obtener_asignaturas_carrera(self, id_carrera):
        return self.almacenamiento_carreras.obtener_asignaturas_carrera(id_carrera)

    # Métodos para gestión de usuarios (usados por facade.py)
    def comprobar_duplicados(self, cedula, rol):
        return self.almacenamiento_usuarios.comprobar_duplicados(cedula, rol)

    def agregar_usuario(self, usuario, rol):
        return self.almacenamiento_usuarios.agregar_usuario(usuario, rol)