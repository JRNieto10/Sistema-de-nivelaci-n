from .clases_abstractas import Usuarios
from .interfaces import ActualizadorDatos
from estructura.entidades import Carrera
from estructura.Almacenamiento_carreras import Almacenamiento_Carreras
from .entidades import *


# Aqui se hizo Herencia
class Docente(Usuarios):
    def __init__(self, nombre, apellido, correo, contrasena, rol, cedula):
        super().__init__(nombre, apellido, correo, contrasena, rol, cedula)

    # 🔒 Permisos exclusivos para el Docente
    # Aqui se hizo Polimorfismo
    @property
    def opciones_menu(self):
        return ["Mis Materias", "Gestionar Actividades", "Tutorías"]

    def cambiar_contraseña(self, nueva_contra):
        self.contrasena = nueva_contra

    def ver_materias_asignadas(self):
        """Devuelve los paralelos (grupo + materia + horario) que este docente dicta."""
        from estructura.Almacenamiento_horario import GuardarHorarios
        gestor = GuardarHorarios()
        paralelos = gestor.listar_paralelos()
        asignados = []
        for p in paralelos:
            if p.get("docente_cedula") == self.cedula:
                asignados.append(p)
                continue
            docentes_por_materia = p.get("docentes_por_materia", {})
            if self.cedula in docentes_por_materia.values():
                asignados.append(p)
        return asignados

    def calificar_estudiante(self, cedula_estudiante, materia, nota, fecha):
        from estructura.Almacenamiento_calificaciones import Almacenamiento_Calificaciones
        almacenamiento = Almacenamiento_Calificaciones()
        return almacenamiento.registrar_nota(cedula_estudiante, materia, nota, self.cedula, fecha)

    def calificar_actividad(self, cedula_estudiante, materia, segmento, actividad, nota, fecha, paralelo_id=""):
        # Aqui se hizo registro de actividades por segmento
        from estructura.Almacenamiento_calificaciones import Almacenamiento_Calificaciones
        almacenamiento = Almacenamiento_Calificaciones()
        return almacenamiento.registrar_actividad(cedula_estudiante, materia, segmento, actividad, nota, self.cedula, fecha, paralelo_id)

    def crear_tutoria(self, id_tutoria, fecha, tema, materia="", paralelo_id="", obligatorios=None):
        # Aqui se hizo Metodo con parametros para materia y estudiantes obligatorios
        from estructura.tutoria import Tutoria
        from estructura.Almacenamiento_tutorias import Almacenamiento_Tutorias
        obligatorios = obligatorios or []
        # Si el profesor marca estudiantes obligatorios, quedan inscritos automaticamente.
        tutoria = Tutoria(id_tutoria, fecha, tema, self.cedula, materia, paralelo_id, obligatorios.copy(), obligatorios)
        Almacenamiento_Tutorias().guardar_tutoria(tutoria)
        return tutoria

    def ver_tutorias(self):
        from estructura.Almacenamiento_tutorias import Almacenamiento_Tutorias
        return Almacenamiento_Tutorias().obtener_tutorias_docente(self.cedula)


# Aqui se hizo Herencia
class Estudiante(Usuarios):
    def __init__(self, nombre, apellido, correo, contrasena, rol, cedula):
        super().__init__(nombre, apellido, correo, contrasena, rol, cedula)

    # Aqui se hizo Polimorfismo
    @property
    def opciones_menu(self):
        return ["Ver Notas", "Actividades", "Mis Horarios", "Matricularme", "Tutorías"]

    def cambiar_contraseña(self, nueva_contra):
        self.contrasena = nueva_contra

    def ver_notas(self):
        from estructura.Almacenamiento_calificaciones import Almacenamiento_Calificaciones
        return Almacenamiento_Calificaciones().obtener_notas_estudiante(self.cedula)


    def ver_actividades(self):
        # Aqui se hizo consulta de actividades del estudiante
        from estructura.Almacenamiento_actividades import Almacenamiento_Actividades
        return Almacenamiento_Actividades().listar_actividades_estudiante(self.cedula)

    def ver_horario(self):
        from estructura.Almacenamiento_horario import GuardarHorarios
        return GuardarHorarios().obtener_horario_estudiante(self.cedula)

    def listar_paralelos_disponibles(self):
        from estructura.Almacenamiento_horario import GuardarHorarios
        return GuardarHorarios().listar_paralelos()

    def matricularse(self, id_paralelo, materia):
        from estructura.Almacenamiento_horario import GuardarHorarios
        return GuardarHorarios().inscribir_estudiante(id_paralelo, self.cedula, materia)

    def ver_tutorias_disponibles(self):
        from estructura.Almacenamiento_tutorias import Almacenamiento_Tutorias
        return Almacenamiento_Tutorias().obtener_tutorias_estudiante(self.cedula)

    def inscribirse_en_tutoria(self, id_tutoria):
        from estructura.Almacenamiento_tutorias import Almacenamiento_Tutorias
        return Almacenamiento_Tutorias().inscribir_estudiante(id_tutoria, self.cedula)


# Aqui se hizo Herencia multiple e interfaz
# El Admin hereda de Usuarios y tambien cumple con ActualizadorDatos.
class Personal(Usuarios, ActualizadorDatos):
    def __init__(self, nombre, apellido, correo, contrasena, rol, cedula):
        super().__init__(nombre, apellido, correo, contrasena, rol, cedula)

    # Aqui se hizo Polimorfismo
    @property
    def opciones_menu(self):
        return [
            "Gestionar Usuarios",
            "Crear Carreras",
            "Crear Materias",
            "Matricular Docentes",
            "Crear Paralelos",
            "Crear Horarios",
            "Configurar Evaluaciones",
            "Importar Usuarios",
            "Exportar Aprobados",
        ]

    def cambiar_contraseña(self, nueva_contra):
        self.contrasena = nueva_contra

    def actualizar_datos_usuario(self, usuario_objetivo, nuevos_datos):
        """
        Modifica cualquier usuario (Estudiante, Docente o Personal).
        usuario_objetivo: El objeto instanciado (ej. un objeto Estudiante).
        nuevos_datos: Diccionario con los campos a actualizar.
        """
        atributos_permitidos = ["nombre", "apellido", "correo", "contrasena"]

        for campo, valor in nuevos_datos.items():
            if campo in atributos_permitidos and hasattr(usuario_objetivo, campo):
                setattr(usuario_objetivo, campo, valor)

        print(f"[Admin] Se han actualizado los datos de {usuario_objetivo.nombre} ({usuario_objetivo.rol}) con éxito.")

    def crear_carrera(self, id_carrera, nombre, duracion):
        nueva_carrera = Carrera(id_carrera, nombre, duracion)
        almacenamiento = Almacenamiento_Carreras()
        if almacenamiento.guardar_carrera(nueva_carrera):
            print(f"Carrera {nombre} guardada.")
        return nueva_carrera

    def crear_paralelo(self, id_paralelo, nombre_paralelo, jornada, materia=None, cedula_docente=None,
                        dia=None, hora_inicio=None, hora_fin=None, aula=None):
        """Crea un paralelo. Las materias se asignan luego desde Crear Materias."""
        from estructura.horario import Horario
        from estructura.paralelo import Paralelo
        from estructura.Almacenamiento_horario import GuardarHorarios

        horario = None
        if dia and hora_inicio and hora_fin and aula:
            horario = Horario(dia, hora_inicio, hora_fin, aula)

        paralelo = Paralelo(id_paralelo, nombre_paralelo, jornada, horario)
        paralelo.materia = materia
        paralelo.materias = [materia] if materia else []
        paralelo.docente_cedula = cedula_docente

        GuardarHorarios().guardar_paralelo(paralelo)
        return paralelo

    # Aqui se hizo Metodo
    def importar_usuarios(self, ruta_archivo):
        """Importación masiva de usuarios completos desde CSV/Excel."""
        from estructura.estrategias_importacion import FabricaEstrategiasImportacion

        try:
            estrategia = FabricaEstrategiasImportacion.crear_para_archivo(ruta_archivo)
        except ValueError as e:
            return {"total": 0, "exitosos": 0, "duplicados": 0, "errores": [str(e)]}

        return estrategia.importar(ruta_archivo)

    # Compatibilidad por si alguna ventana antigua llama a importar_cedulas.
    def importar_cedulas(self, ruta_archivo):
        return self.importar_usuarios(ruta_archivo)


# Metodos agregados al administrador para configurar evaluaciones
def _personal_configurar_evaluaciones(self, segmentos, nota_final=10):
    from estructura.Almacenamiento_evaluaciones import Almacenamiento_Evaluaciones
    return Almacenamiento_Evaluaciones().guardar_configuracion(segmentos, nota_final)

Personal.configurar_evaluaciones = _personal_configurar_evaluaciones
