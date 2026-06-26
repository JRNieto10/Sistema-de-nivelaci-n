
from estructura.estudiantes import Estudiante
from estructura.docentes import Docente
from estructura.personal_administrativo import Personal
from estructura.asignatura import Asignatura
from estructura.calificaciones import Calificaciones
from estructura.carrera import Carrera
from estructura.tutoria import Tutoria
from estructura.horarios import HorarioParalelo
from estructura.horario_docente import HorarioDocente
from estructura.gestor_curso import Gestor_curso
from estructura.cursos import Curso
from estructura.registro import Registro
from estructura.Almacenamieto import Almacenamiento_Usuarios
from estructura.Almacenamiento_ingreso import GestorAlmacenamiento
from estructura.Almacenamiento_horario import GuardarHorarios
from estructura.Almacenamiento_horario_docente import horariodocentealmacenar
from estructura.Autenticacion import Autenticacion
from estructura.fabrica_usuarios import FabricaUsuarios
from Ingresar_datos import Ingreso_datos
from estructura.gest_permitidos import GestionPermitidos

import json
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
        self.registro = Registro()
        self.almacenamiento_usuarios = GestorAlmacenamiento()
        self.autenticacion = Autenticacion(Almacenamiento_Usuarios())
        self.gestor_cursos = Gestor_curso()
        self.gestor_horarios = GuardarHorarios()
        self.gestor_horarios_docentes = horariodocentealmacenar()
        self.gestion_permitidos = GestionPermitidos()
        self.fabrica_usuarios = FabricaUsuarios()
        self.ingreso_datos = Ingreso_datos()
        self.almacenamiento_verificacion = Almacenamiento_Usuarios()
    
    def crear_archivos_directorios(self):
        import os
        if not os.path.exists("Datos"):
            os.makedirs("Datos")
        
        archivos = [
            "Datos/estudiantes.json",
            "Datos/docentes.json",
            "Datos/personal_administrativo.json",
            "Datos/permitidos.json",
            "Datos/paralelos.json",
            "Datos/horarios_docentes.json"
        ]
        for archivo in archivos:
            if not os.path.exists(archivo):
                with open(archivo, 'w', encoding='utf-8') as f:
                    if "permitidos" in archivo:
                        json.dump({
                            "cedulas_estudiantes": [],
                            "cedulas_docentes": [],
                            "cedulas_personal": []
                        }, f, ensure_ascii=False, indent=4)
                    else:
                        json.dump([], f, ensure_ascii=False, indent=4)
    
    def agregar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.agregar_cedula(cedula, tipo)
    
    def agregar_cedulas_multiples(self, cedulas, tipo):
        return self.gestion_permitidos.agregar_multiple(cedulas, tipo)
    
    def eliminar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.eliminar_cedula(cedula, tipo)
    
    def verificar_cedula(self, cedula):
        return self.gestion_permitidos.verificar_cedula(cedula)
    
    def listar_cedulas_permitidas(self, tipo=None):
        return self.gestion_permitidos.listar_cedulas(tipo)
    
    def mostrar_cedulas_permitidas(self):
        self.gestion_permitidos.mostrar_todos()
    
    def registrar_usuario(self, nombre, cedula, apellido, correo, contrasena, rol):
        if not self.gestion_permitidos.verificar_cedula(cedula):
            return False, "cedula no permitida mi pana"
        
        if self.almacenamiento_usuarios.comprobar_duplicados(cedula, rol):
            return False, "ese usuario ya existe bro"
        
        usuario = {
            'cedula': cedula,
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'contrasena': contrasena,
            'rol': rol
        }
        
        if self.almacenamiento_usuarios.agregar_usuario(usuario, rol):
            usuario_obj = self.fabrica_usuarios.crear_usuario(usuario)
            self.lista_usuarios.append(usuario_obj)
            return True, f"el {nombre} quedo registrado bien"
        return False, "fallo el registro"
    
    def crear_administrativo(self, nombre, cedula, apellido, correo, contrasena):
        return self.registrar_usuario(nombre, cedula, apellido, correo, contrasena, "administrativo")
    
    def crear_docente(self, nombre, cedula, apellido, correo, contrasena):
        return self.registrar_usuario(nombre, cedula, apellido, correo, contrasena, "docente")
    
    def crear_estudiante(self, nombre, cedula, apellido, correo, contrasena):
        return self.registrar_usuario(nombre, cedula, apellido, correo, contrasena, "estudiante")
    
    def crear_carrera(self, id, area, nombre, jornada, modalidad):
        carrera = Carrera(id, area, nombre, jornada, modalidad)
        self.lista_carreras.append(carrera)
        return carrera
    
    def crear_asignatura(self, nombre, codigo, creditos, horas, modalidad):
        asignatura = Asignatura(nombre, codigo, creditos, horas, modalidad)
        self.lista_materias.append(asignatura)
        return asignatura
    
    def calcular_carga_horaria_asignatura(self, asignatura):
        return asignatura.calcular_carga_horaria()
    
    def crear_curso(self, nombre_curso):
        curso = Curso(nombre_curso)
        self.lista_cursos.append(curso)
        return curso
    
    def agregar_materia_a_curso(self, curso, materia, horas_requeridas=1):
        curso.agregar_materia(materia, horas_requeridas)
    
    def asignar_docente_a_materia(self, curso, docente, materia):
        curso.agregar_docente(docente, materia)
    
    def crear_paralelos(self, nombre_curso_base, cantidad_paralelos, curso):
        paralelos = self.gestor_cursos.crear_cursos(nombre_curso_base, cantidad_paralelos, curso)
        self.lista_paralelos.extend(paralelos)
        self.gestor_horarios.guardar_paralelos(paralelos)
        return paralelos
    
    def inscribir_estudiante_en_paralelo(self, paralelo, estudiante_nombre):
        paralelo.inscribir_estudiante(estudiante_nombre)
    
    def retirar_estudiante_de_paralelo(self, paralelo, estudiante_nombre):
        return paralelo.retirar_estudiante(estudiante_nombre)
    
    def guardar_horarios_docentes(self, docentes):
        for docente in docentes:
            horario = self.gestor_cursos.obtener_horario_por_docente(docente.nombre)
            if horario:
                self.gestor_horarios_docentes.guardar_horario_docente(docente, horario)
    
    def obtener_horario_paralelo(self, nombre_paralelo):
        return self.gestor_horarios.obtener_horario_paralelo(nombre_paralelo)
    
    def mostrar_horario_paralelo(self, nombre_paralelo):
        self.gestor_horarios.mostrar_horario_paralelo(nombre_paralelo)
    
    def obtener_horario_docente(self, cedula):
        return self.gestor_horarios_docentes.obtener_horario_docente(cedula)
    
    def mostrar_horario_docente(self, cedula):
        self.gestor_horarios_docentes.mostrar_horario_docente(cedula)
    
    def crear_horario_paralelo(self, paralelo):
        return HorarioParalelo(paralelo)
    
    def crear_horario_docente(self, nombre_docente):
        return HorarioDocente(nombre_docente, self.gestor_cursos)
    
    def crear_tutoria(self, id, fecha, tema, estudiantes=None):
        tutoria = Tutoria(id, fecha, tema, estudiantes)
        self.lista_tutorias.append(tutoria)
        return tutoria
    
    def programar_tutoria(self, tutoria):
        tutoria.programar()
    
    def cancelar_tutoria(self, tutoria):
        tutoria.cancelar()
    
    def ver_asistentes_tutoria(self, tutoria):
        tutoria.estud_asistentes()
    
    def crear_calificacion(self, nota, fecha):
        calificacion = Calificaciones(nota, fecha)
        self.lista_notas.append(calificacion)
        return calificacion
    
    def verificar_aprobacion(self, calificacion):
        return calificacion.aprobar()
    
    def login(self, cedula, contrasena):
        return self.autenticacion.iniciar_sesion(cedula, contrasena)
    
    def logout(self):
        self.autenticacion.cerrar_sesion()
    
    def verificar_credenciales(self, cedula, contrasena):
        return self.almacenamiento_verificacion.verificar_credenciales(cedula, contrasena)
    
    def mostrar_todos_paralelos(self):
        for paralelo in self.lista_paralelos:
            print(paralelo)
    
    def mostrar_todas_carreras(self):
        for carrera in self.lista_carreras:
            print(f"carrera: {carrera.nombre} - {carrera.jornada}")
    
    def mostrar_todas_asignaturas(self):
        for asignatura in self.lista_materias:
            print(f"materia: {asignatura.nombre} - {asignatura.codigo}")
    
    def matricular_carrera(self, carrera):
        carrera.matricularse()
    
    def retirar_carrera(self, carrera):
        carrera.retirarse()
    
    def crear_usuario_con_fabrica(self, datos_usuario):
        return self.fabrica_usuarios.crear_usuario(datos_usuario)
    
    def obtener_docentes_por_materia(self, curso, materia):
        return curso.obtener_docentes_por_materia(materia)
    
    def obtener_materias_por_docente(self, curso, docente):
        return curso.obtener_materias_por_docente(docente)