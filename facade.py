from estructura.Almacenamiento_horario import GuardarHorarios
from estructura.Almacenamiento_horario_docente import horariodocentealmacenar
from estructura.estudiantes import Estudiante
from estructura.docentes import Docente
from estructura.personal_administrativo import Personal
from estructura.asignatura import Asignatura
from estructura.calificaciones import Calificaciones
from estructura.carrera import Carrera
from estructura.tutoria import Tutoria
from estructura.gestor_curso import Gestor_curso
from estructura.cursos import Curso
from estructura.registro import Registro
from estructura.Almacenamieto import Almacenamiento_Usuarios
from estructura.Almacenamiento_ingreso import GestorAlmacenamiento
from estructura.Autenticacion import Autenticacion
from estructura.fabrica_usuarios import FabricaUsuarios
from estructura.gest_permitidos import GestionPermitidos
from facade_datos import FacadeDatos

class FacadeSistemaAcademico:
    def __init__(self):
        self._inicializar_subsistemas()
        self.lista_usuarios = []
        self.lista_carreras = []
        self.lista_materias = []
        self.lista_cursos = []
        self.lista_paralelos = []
        self.lista_tutorias = []
        self.lista_notas = []
        self.facade_datos = FacadeDatos()
        self.almacenamiento_carreras = self.facade_datos.almacenamiento_carreras

    def _inicializar_subsistemas(self):
        self.gestor_horarios = GuardarHorarios()
        self.gestor_horarios_docentes = horariodocentealmacenar()
        self.registro = Registro()
        self.almacenamiento_usuarios = GestorAlmacenamiento()
        self.autenticacion = Autenticacion(Almacenamiento_Usuarios())
        self.gestor_cursos = Gestor_curso()
        self.gestion_permitidos = GestionPermitidos()
        self.fabrica_usuarios = FabricaUsuarios()
        self.almacenamiento_verificacion = Almacenamiento_Usuarios()

    def crear_administrador(self, nombre, cedula, apellido, correo, contrasena):
        administrador = Personal(nombre, cedula, apellido, correo, contrasena, "personal")
        self.lista_usuarios.append(administrador)
        self.facade_datos.agregar_usuario({
            "cedula": cedula,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contrasena": contrasena,
            "rol": "personal",
        }, "personal")
        return administrador

    def crear_docente(self, nombre, cedula, apellido, correo, contrasena):
        docente = Docente(nombre, cedula, apellido, correo, contrasena, "docente")
        self.lista_usuarios.append(docente)
        self.facade_datos.agregar_usuario({
            "cedula": cedula,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contrasena": contrasena,
            "rol": "docente",
        }, "docente")
        return docente

    def crear_estudiante(self, nombre, cedula, apellido, correo, contrasena):
        estudiante = Estudiante(nombre, cedula, apellido, correo, contrasena, "estudiante")
        self.lista_usuarios.append(estudiante)
        self.facade_datos.agregar_usuario({
            "cedula": cedula,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contrasena": contrasena,
            "rol": "estudiante",
        }, "estudiante")
        return estudiante

    def _registrar_usuario(self, nombre, cedula, apellido, correo, contrasena, rol):
        if not self.facade_datos.verificar_cedula(cedula):
            return False, "cedula no permitida"
        if self.facade_datos.comprobar_duplicados(cedula, rol):
            return False, "ese usuario ya existe"
        usuario = {
            "cedula": cedula,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contrasena": contrasena,
            "rol": rol,
        }
        if self.facade_datos.agregar_usuario(usuario, rol):
            usuario_obj = self.fabrica_usuarios.crear_usuario(usuario)
            self.lista_usuarios.append(usuario_obj)
            return True, f"el {nombre} quedo registrado"
        return False, "fallo el registro"

    # Métodos para gestión de carreras
    def crear_carrera(self, id, area, nombre, modalidad):
        if self.obtener_carrera_por_id(id):
            return None, "Ya existe una carrera con ese ID"
        
        carrera = Carrera(id, area, nombre, modalidad)
        self.lista_carreras.append(carrera)
        
        if self.facade_datos.guardar_carrera(carrera):
            return carrera, "Carrera creada exitosamente"
        else:
            self.lista_carreras.remove(carrera)
            return None, "Error al guardar la carrera"
    
    def obtener_carrera_por_id(self, id_carrera):
        for carrera in self.lista_carreras:
            if carrera.id == id_carrera:
                return carrera
        
        carrera = self.facade_datos.cargar_carrera(id_carrera)
        if carrera:
            self.lista_carreras.append(carrera)
        return carrera
    
    def obtener_todas_carreras(self):
        carreras_almacenadas = self.facade_datos.cargar_todas_carreras()
        ids_memoria = {c.id for c in self.lista_carreras}
        
        for carrera in carreras_almacenadas:
            if carrera.id not in ids_memoria:
                self.lista_carreras.append(carrera)
        
        return self.lista_carreras
    
    def eliminar_carrera(self, id_carrera):
        self.lista_carreras = [c for c in self.lista_carreras if c.id != id_carrera]
        return self.facade_datos.eliminar_carrera(id_carrera)
    
    def agregar_asignatura_a_carrera(self, id_carrera, asignatura):
        carrera = self.obtener_carrera_por_id(id_carrera)
        if carrera:
            if not hasattr(carrera, 'asignaturas'):
                carrera.asignaturas = []
            carrera.asignaturas.append(asignatura)
            return self.facade_datos.guardar_carrera(carrera)
        
        return self.facade_datos.agregar_asignatura_a_carrera(id_carrera, asignatura)
    
    def obtener_asignaturas_carrera(self, id_carrera):
        carrera = self.obtener_carrera_por_id(id_carrera)
        if carrera and hasattr(carrera, 'asignaturas'):
            return carrera.asignaturas
        return self.facade_datos.obtener_asignaturas_carrera(id_carrera)

    def crear_asignatura(self, nombre, codigo, creditos, horas, modalidad):
        asignatura = Asignatura(nombre, codigo, creditos, horas, modalidad)
        self.lista_materias.append(asignatura)
        return asignatura

    def crear_curso(self, nombre_curso):
        curso = Curso(nombre_curso)
        self.gestor_cursos.crear_curso(nombre_curso)
        self.lista_cursos.append(curso)
        return curso

    def agregar_materia_a_curso(self, curso, materia, horas_requeridas=1):
        curso.agregar_materia(materia, horas_requeridas)
        
    def asignar_docente_a_materia(self, curso, docente, materia):
        docente_obj = None
        docente_nombre = docente.nombre if hasattr(docente, 'nombre') else docente
        
        for usuario in self.lista_usuarios:
            if hasattr(usuario, 'nombre') and usuario.nombre == docente_nombre and usuario.rol == "docente":
                docente_obj = usuario
                break
        
        if not docente_obj:
            return False
        
        materia_nombre = materia.nombre if hasattr(materia, 'nombre') else materia
        
        curso.agregar_docente(docente_obj, materia_nombre)
        return True
        
    def inscribir_estudiante_en_paralelo(self, paralelo, estudiante):
        paralelo.inscribir_estudiante(estudiante)

    def crear_tutoria(self, id, fecha, tema, estudiantes=None):
        tutoria = Tutoria(id, fecha, tema, estudiantes)
        self.lista_tutorias.append(tutoria)
        return tutoria
    
    # En facade.py, agregar este método:

    def registrar_usuario(self, nombre="", cedula="", apellido="", correo="", contrasena="", rol=""):
        """
        Registra un usuario en el sistema
        """
        # Verificar si la cédula está permitida
        if not self.facade_datos.verificar_cedula(cedula):
            return False, "Cédula no permitida"
        
        # Verificar si el usuario ya existe
        if self.facade_datos.verificar_usuario_existe(cedula, rol):
            return False, "El usuario ya existe"
        
        # Crear usuario según el rol
        if rol == "estudiante":
            usuario = self.crear_estudiante(nombre, cedula, apellido, correo, contrasena)
        elif rol == "docente":
            usuario = self.crear_docente(nombre, cedula, apellido, correo, contrasena)
        elif rol == "personal" or rol == "administrador":
            usuario = self.crear_administrador(nombre, cedula, apellido, correo, contrasena)
        else:
            return False, "Rol no válido"
        
        return True, f"Usuario {nombre} registrado exitosamente"