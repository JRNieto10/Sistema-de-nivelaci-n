# facade_datos.py
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

    def agregar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.agregar_cedula(cedula, tipo)

    def eliminar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.eliminar_cedula(cedula, tipo)

    def verificar_cedula(self, cedula):
        return self.gestion_permitidos.verificar_cedula(cedula)

    def listar_cedulas(self):
        return self.gestion_permitidos.listar_cedulas()

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

    def guardar_curso(self, carrera_nombre, curso_nombre, materias_con_docentes):
        return self.almacenamiento_cursos.guardar_curso(carrera_nombre, curso_nombre, materias_con_docentes)

    def cargar_curso(self, carrera_nombre, curso_nombre):
        return self.almacenamiento_cursos.cargar_curso(carrera_nombre, curso_nombre)

    def guardar_paralelos(self, carrera_nombre, curso_nombre, paralelos_data):
        return self.almacenamiento_cursos.guardar_paralelos(carrera_nombre, curso_nombre, paralelos_data)

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

    def comprobar_duplicados(self, cedula, rol):
        return self.almacenamiento_usuarios.comprobar_duplicados(cedula, rol)

    def agregar_usuario(self, usuario, rol):
        return self.almacenamiento_usuarios.agregar_usuario(usuario, rol)
    
    def obtener_todas_cedulas(self):
        return self.gestion_permitidos.listar_cedulas()

    def agregar_cedulas_masivas(self, cedulas, tipo):
        return self.gestion_permitidos.agregar_multiple(cedulas, tipo)

    def limpiar_todas_cedulas(self):
        return self.gestion_permitidos.limpiar_todos()

    def guardar_paralelo_actualizado(self, paralelo):
        for p in self.lista_paralelos:
            if p.nombre == paralelo.nombre:
                self.gestor_horarios.guardar_paralelo(p)
                return True
        return False
    
    
    def sincronizar_paralelo_con_matriculas(self, paralelo_nombre):
        """Sincroniza los estudiantes de un paralelo con sus matrículas"""
        # Buscar el paralelo en la lista en memoria
        paralelo_obj = None
        for p in self.lista_paralelos:
            if p.nombre == paralelo_nombre:
                paralelo_obj = p
                break
        
        if not paralelo_obj:
            print(f"Paralelo {paralelo_nombre} no encontrado en memoria")
            return False
        
        # Obtener nombres de estudiantes de las matrículas
        ruta_matriculas = os.path.join(self.ruta_base, "matriculas")
        estudiantes_nombres = []
        
        if os.path.exists(ruta_matriculas):
            for archivo in os.listdir(ruta_matriculas):
                if archivo.startswith("matricula_") and archivo.endswith(".json"):
                    ruta_matricula = os.path.join(ruta_matriculas, archivo)
                    try:
                        with open(ruta_matricula, 'r', encoding='utf-8') as f:
                            datos = json.load(f)
                            if datos.get("paralelo") == paralelo_nombre:
                                estudiantes_nombres.append(datos.get("nombre"))
                    except Exception as e:
                        print(f"Error al leer {archivo}: {e}")
        
        # Actualizar la lista de estudiantes del paralelo
        paralelo_obj.estudiantes = estudiantes_nombres
        
        # Guardar el paralelo actualizado en el archivo
        try:
            ruta_paralelos = os.path.join(self.ruta_base, "paralelos.json")
            
            # Cargar todos los paralelos existentes
            paralelos_data = []
            if os.path.exists(ruta_paralelos):
                with open(ruta_paralelos, 'r', encoding='utf-8') as f:
                    paralelos_data = json.load(f)
            
            # Buscar y actualizar el paralelo específico
            encontrado = False
            for i, p_data in enumerate(paralelos_data):
                if p_data.get("nombre") == paralelo_nombre:
                    # Convertir el objeto Paralelo a diccionario
                    p_data["estudiantes"] = estudiantes_nombres
                    encontrado = True
                    break
            
            # Si no se encontró, agregarlo
            if not encontrado:
                nuevo_paralelo = {
                    "nombre": paralelo_nombre,
                    "id": paralelo_obj.id,
                    "curso": str(paralelo_obj.curso) if hasattr(paralelo_obj, 'curso') else "",
                    "estudiantes": estudiantes_nombres,
                    "horario": {}
                }
                paralelos_data.append(nuevo_paralelo)
            
            # Guardar el archivo actualizado
            with open(ruta_paralelos, 'w', encoding='utf-8') as f:
                json.dump(paralelos_data, f, ensure_ascii=False, indent=4)
            
            print(f"Paralelo {paralelo_nombre} actualizado con {len(estudiantes_nombres)} estudiantes")
            return True
            
        except Exception as e:
            print(f"Error al guardar paralelo: {e}")
            return False
    def sincronizar_todos_paralelos(self):
        """Sincroniza todos los paralelos con sus matrículas"""
        print("Sincronizando todos los paralelos...")
        contador = 0
        for paralelo in self.lista_paralelos:
            nombre = paralelo.nombre if hasattr(paralelo, 'nombre') else str(paralelo)
            if self.sincronizar_paralelo_con_matriculas(nombre):
                contador += 1
        print(f"Sincronización completada. {contador} paralelos actualizados.")
        return True