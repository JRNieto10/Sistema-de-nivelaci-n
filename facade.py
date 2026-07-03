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
import json
import os

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

    def crear_archivos_directorios(self):
        if not os.path.exists("Datos"):
            os.makedirs("Datos")
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
                    else:
                        json.dump([], f, ensure_ascii=False, indent=4)







    def crear_administrador(self, nombre, cedula, apellido, correo, contrasena):
        administrador = Personal(nombre, cedula, apellido, correo, contrasena, "personal")
        self.lista_usuarios.append(administrador)
        return administrador




    def crear_docente(self, nombre, cedula, apellido, correo, contrasena):
        docente = Docente(nombre, cedula, apellido, correo, contrasena, "docente")
        self.lista_usuarios.append(docente)
        return docente
        




    def crear_estudiante(self, nombre, cedula, apellido, correo, contrasena):
        estudiante = Estudiante(nombre, cedula, apellido, correo, contrasena, "estudiante")
        self.lista_usuarios.append(estudiante)
        return estudiante

    def _registrar_usuario(self, nombre, cedula, apellido, correo, contrasena, rol):
        if not self.gestion_permitidos.verificar_cedula(cedula):
            return False, "cedula no permitida"
        if self.almacenamiento_usuarios.comprobar_duplicados(cedula, rol):
            return False, "ese usuario ya existe"
        usuario = {
            "cedula": cedula,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contrasena": contrasena,
            "rol": rol,
        }
        if self.almacenamiento_usuarios.agregar_usuario(usuario, rol):
            usuario_obj = self.fabrica_usuarios.crear_usuario(usuario)
            self.lista_usuarios.append(usuario_obj)
            return True, f"el {nombre} quedo registrado"
        return False, "fallo el registro"

    def crear_carrera(self, id, area, nombre, modalidad):
        carrera = Carrera(id, area, nombre, modalidad)
        self.lista_carreras.append(carrera)
        return carrera

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
        # Buscar el objeto docente por nombre o por el objeto completo
        docente_obj = None
        docente_nombre = docente.nombre if hasattr(docente, 'nombre') else docente
        
        for usuario in self.lista_usuarios:
            if hasattr(usuario, 'nombre') and usuario.nombre == docente_nombre and usuario.rol == "docente":
                docente_obj = usuario
                break
        
        if not docente_obj:
            print(f"Docente '{docente_nombre}' no encontrado")
            return False
        
        # Buscar el nombre de la materia
        materia_nombre = materia.nombre if hasattr(materia, 'nombre') else materia
        
        curso.agregar_docente(docente_obj, materia_nombre)
        return True
    def inscribir_estudiante_en_paralelo(self, paralelo, estudiante):
        paralelo.inscribir_estudiante(estudiante)

    def crear_tutoria(self, id, fecha, tema, estudiantes=None):
        tutoria = Tutoria(id, fecha, tema, estudiantes)
        self.lista_tutorias.append(tutoria)
        return tutoria
