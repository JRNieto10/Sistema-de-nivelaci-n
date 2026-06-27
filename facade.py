"""
facade.py  —  FacadeSistemaAcademico
=====================================
Patrón Facade: punto de entrada único para toda la lógica del sistema.
Wagner conecta cada método de esta clase a los eventos de CustomTkinter
(botones, campos de texto, comboboxes, etc.).

Nuevo en esta versión:
- importar_cedulas_csv()   → carga cédulas desde un archivo CSV
- listar_csvs_carpeta()    → lista archivos CSV disponibles en una carpeta
"""

from estructura.estudiantes                    import Estudiante
from estructura.docentes                       import Docente
from estructura.personal_administrativo        import Personal
from estructura.asignatura                     import Asignatura
from estructura.calificaciones                 import Calificaciones
from estructura.carrera                        import Carrera
from estructura.tutoria                        import Tutoria
from estructura.horarios                       import HorarioParalelo
from estructura.horario_docente                import HorarioDocente
from estructura.gestor_curso                   import Gestor_curso
from estructura.cursos                         import Curso
from estructura.registro                       import Registro
from estructura.Almacenamieto                  import Almacenamiento_Usuarios
from estructura.Almacenamiento_ingreso         import GestorAlmacenamiento
from estructura.Almacenamiento_horario         import GuardarHorarios
from estructura.Almacenamiento_horario_docente import horariodocentealmacenar
from estructura.Autenticacion                  import Autenticacion
from estructura.fabrica_usuarios               import FabricaUsuarios
from estructura.gest_permitidos                import GestionPermitidos
from estructura.importador_csv                 import ImportadorCSV
from Ingresar_datos                            import Ingreso_datos

import json


class FacadeSistemaAcademico:
    def __init__(self):
        self._inicializar_subsistemas()
        self.lista_usuarios  = []
        self.lista_carreras  = []
        self.lista_materias  = []
        self.lista_cursos    = []
        self.lista_paralelos = []
        self.lista_tutorias  = []
        self.lista_notas     = []

    def _inicializar_subsistemas(self):
        self.registro                  = Registro()
        self.almacenamiento_usuarios   = GestorAlmacenamiento()
        self.autenticacion             = Autenticacion(Almacenamiento_Usuarios())
        self.gestor_cursos             = Gestor_curso()
        self.gestor_horarios           = GuardarHorarios()
        self.gestor_horarios_docentes  = horariodocentealmacenar()
        self.gestion_permitidos        = GestionPermitidos()
        self.fabrica_usuarios          = FabricaUsuarios()
        self.ingreso_datos             = Ingreso_datos()
        self.almacenamiento_verificacion = Almacenamiento_Usuarios()
        # Importador CSV — usa GestionPermitidos internamente (DIP)
        self.importador_csv            = ImportadorCSV(self.gestion_permitidos)

    # -----------------------------------------------------------------------
    # INICIALIZACIÓN DE ARCHIVOS Y DIRECTORIOS
    # -----------------------------------------------------------------------

    def crear_archivos_directorios(self):
        """
        Crea la carpeta Datos/ y todos los JSON necesarios si no existen.
        Wagner: llama esto al arrancar la app antes de mostrar cualquier ventana.
        """
        import os
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
                        json.dump({
                            "cedulas_estudiantes": [],
                            "cedulas_docentes": [],
                            "cedulas_personal": []
                        }, f, ensure_ascii=False, indent=4)
                    else:
                        json.dump([], f, ensure_ascii=False, indent=4)

    # -----------------------------------------------------------------------
    # GESTIÓN DE CÉDULAS PERMITIDAS
    # -----------------------------------------------------------------------

    def agregar_cedula_permitida(self, cedula: str, tipo: str) -> bool:
        """
        Agrega una cédula al sistema para habilitar la creación de cuenta.
        Wagner: conectar al botón "Agregar cédula" del panel admin.
        Retorna True si se agregó, False si ya existía.
        """
        return self.gestion_permitidos.agregar_cedula(cedula, tipo)

    def agregar_cedulas_multiples(self, cedulas: list, tipo: str) -> list:
        """
        Agrega una lista de cédulas del mismo tipo de una sola vez.
        Wagner: útil para carga masiva desde la interfaz (lista o tabla).
        Retorna la lista de cédulas efectivamente agregadas.
        """
        return self.gestion_permitidos.agregar_multiple(cedulas, tipo)

    def importar_cedulas_csv(self, ruta_csv: str) -> dict:
        """
        Importa cédulas desde un archivo CSV con columnas 'cedula' y 'tipo'.
        Wagner: conectar al botón "Importar CSV" del panel admin.

        Retorna un dict con:
            {
                "exitosos":   int,   # cédulas nuevas agregadas
                "duplicados": int,   # cédulas que ya existían (ignoradas)
                "errores":    list   # mensajes de filas con problemas
            }

        Ejemplo de uso en CustomTkinter:
            resultado = sistema.importar_cedulas_csv(ruta)
            label_exitosos.configure(text=f"Agregadas: {resultado['exitosos']}")
            label_duplicados.configure(text=f"Duplicadas: {resultado['duplicados']}")
            if resultado["errores"]:
                textbox_errores.insert("end", "\\n".join(resultado["errores"]))
        """
        return self.importador_csv.importar(ruta_csv)

    def listar_csvs_carpeta(self, carpeta: str) -> list:
        """
        Lista los archivos .csv disponibles en una carpeta.
        Wagner: usar para poblar un Combobox o Listbox donde el admin
        selecciona qué archivo importar sin escribir la ruta manualmente.

        Ejemplo de uso en CustomTkinter:
            archivos = sistema.listar_csvs_carpeta("importaciones/")
            combobox.configure(values=archivos)
        """
        return self.importador_csv.listar_csvs(carpeta)

    def eliminar_cedula_permitida(self, cedula: str, tipo: str) -> bool:
        return self.gestion_permitidos.eliminar_cedula(cedula, tipo)

    def verificar_cedula(self, cedula: str) -> str | None:
        """
        Verifica si una cédula está permitida y retorna su tipo
        ("estudiante", "docente", "personal") o None si no está.
        Wagner: usar al validar el campo de cédula en la pantalla de registro.
        """
        return self.gestion_permitidos.verificar_cedula(cedula)

    def listar_cedulas_permitidas(self, tipo: str = None) -> dict | list:
        return self.gestion_permitidos.listar_cedulas(tipo)

    def mostrar_cedulas_permitidas(self):
        self.gestion_permitidos.mostrar_todos()

    # -----------------------------------------------------------------------
    # REGISTRO Y GESTIÓN DE USUARIOS
    # -----------------------------------------------------------------------

    def registrar_usuario(self, nombre: str = None, cedula: str = None, apellido: str = None,
                          correo: str = None, contrasena: str = None, rol: str = None) -> tuple[bool, str]:
        """
        Registra un usuario nuevo validando primero que su cédula esté permitida.
        Wagner: conectar al botón "Crear cuenta" de la pantalla de registro.

        Retorna (True, mensaje_ok) o (False, mensaje_error).

        Ejemplo de uso en CustomTkinter:
            exito, mensaje = sistema.registrar_usuario(
                nombre_entry.get(), cedula_entry.get(), ...
            )
            if exito:
                mostrar_ventana_principal()
            else:
                label_error.configure(text=mensaje)
        """
        if not self.gestion_permitidos.verificar_cedula(cedula):
            return False, "Cédula no registrada en el sistema."

        if self.almacenamiento_usuarios.comprobar_duplicados(cedula, rol):
            return False, "Ya existe una cuenta con esa cédula."

        usuario = {
            "cedula":     cedula,
            "nombre":     nombre,
            "apellido":   apellido,
            "correo":     correo,
            "contrasena": contrasena,
            "rol":        rol,
        }

        if self.almacenamiento_usuarios.agregar_usuario(usuario, rol):
            usuario_obj = self.fabrica_usuarios.crear_usuario(usuario)
            self.lista_usuarios.append(usuario_obj)
            return True, f"Cuenta creada exitosamente. Bienvenido, {nombre}."
        return False, "Error al guardar. Intente nuevamente."

    def crear_administrativo(self, nombre, cedula, apellido, correo, contrasena):
        return self.registrar_usuario(nombre, cedula, apellido, correo, contrasena, "Administrador")

    def crear_docente(self, nombre, cedula, apellido, correo, contrasena):
        return self.registrar_usuario(nombre, cedula, apellido, correo, contrasena, "Docente")

    def crear_estudiante(self, nombre, cedula, apellido, correo, contrasena):
        return self.registrar_usuario(nombre, cedula, apellido, correo, contrasena, "Estudiante")

    # -----------------------------------------------------------------------
    # AUTENTICACIÓN
    # -----------------------------------------------------------------------

    def login(self, cedula: str, contrasena: str) -> bool:
        """
        Inicia sesión. Retorna True si las credenciales son correctas.
        Wagner: conectar al botón "Iniciar sesión".

        Ejemplo de uso en CustomTkinter:
            if sistema.login(cedula_entry.get(), pass_entry.get()):
                rol = sistema.obtener_usuario_actual()["rol"]
                if rol == "Administrador":
                    abrir_ventana_admin()
                elif rol == "docente":
                    abrir_ventana_docente()
                elif rol == "estudiante":
                    abrir_ventana_estudiante()
            else:
                label_error.configure(text="Credenciales incorrectas.")
        """
        return self.autenticacion.iniciar_sesion(cedula, contrasena)

    def logout(self):
        """
        Cierra la sesión activa.
        Wagner: conectar al botón "Cerrar sesión".
        """
        self.autenticacion.cerrar_sesion()

    def obtener_usuario_actual(self) -> dict | None:
        """
        Retorna el dict del usuario con sesión activa, o None si no hay sesión.
        Wagner: usar para mostrar el nombre del usuario en la interfaz
        y para controlar qué ventanas/botones se habilitan según el rol.

        Ejemplo de uso en CustomTkinter:
            usuario = sistema.obtener_usuario_actual()
            if usuario:
                label_bienvenida.configure(text=f"Bienvenido, {usuario['nombre']}")
        """
        return self.autenticacion.usuario_actual

    def verificar_credenciales(self, cedula: str, contrasena: str) -> dict | bool:
        return self.almacenamiento_verificacion.verificar_credenciales(cedula, contrasena)

    # -----------------------------------------------------------------------
    # CARRERAS Y ASIGNATURAS
    # -----------------------------------------------------------------------

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

    def mostrar_todas_carreras(self):
        for carrera in self.lista_carreras:
            print(f"Carrera: {carrera.nombre} - {carrera.jornada}")

    def mostrar_todas_asignaturas(self):
        for asignatura in self.lista_materias:
            print(f"Materia: {asignatura.nombre} - {asignatura.codigo}")

    def matricular_carrera(self, carrera):
        carrera.matricularse()

    def retirar_carrera(self, carrera):
        carrera.retirarse()

    # -----------------------------------------------------------------------
    # CURSOS Y PARALELOS
    # -----------------------------------------------------------------------

    def crear_curso(self, nombre_curso: str) -> Curso:
        curso = Curso(nombre_curso)
        self.lista_cursos.append(curso)
        return curso

    def agregar_materia_a_curso(self, curso, materia, horas_requeridas=1):
        curso.agregar_materia(materia, horas_requeridas)

    def asignar_docente_a_materia(self, curso, docente, materia):
        curso.agregar_docente(docente, materia)
        


    def crear_paralelos(self, nombre_curso_base: str, cantidad_paralelos: int, curso) -> list:
        """
        Genera paralelos automáticamente, asigna jornadas/aulas/horarios
        y guarda todo en paralelos.json.
        Wagner: conectar al botón "Generar paralelos" del panel admin.
        """
        paralelos = self.gestor_cursos.crear_cursos(nombre_curso_base, cantidad_paralelos, curso)
        self.lista_paralelos.extend(paralelos)
        self.gestor_horarios.guardar_paralelos(paralelos)
        return paralelos

    def inscribir_estudiante_en_paralelo(self, paralelo, estudiante_nombre):
        paralelo.inscribir_estudiante(estudiante_nombre)

    def retirar_estudiante_de_paralelo(self, paralelo, estudiante_nombre):
        return paralelo.retirar_estudiante(estudiante_nombre)

    def mostrar_todos_paralelos(self):
        for paralelo in self.lista_paralelos:
            print(paralelo)

    def obtener_docentes_por_materia(self, curso, materia):
        return curso.obtener_docentes_por_materia(materia)

    def obtener_materias_por_docente(self, curso, docente):
        return curso.obtener_materias_por_docente(docente)

    # -----------------------------------------------------------------------
    # HORARIOS
    # -----------------------------------------------------------------------

    def obtener_horario_paralelo(self, nombre_paralelo: str) -> dict | None:
        """
        Retorna el dict del horario de un paralelo desde el JSON.
        Wagner: usar para poblar una tabla/treeview con el horario.
        """
        return self.gestor_horarios.obtener_horario_paralelo(nombre_paralelo)

    def mostrar_horario_paralelo(self, nombre_paralelo: str):
        self.gestor_horarios.mostrar_horario_paralelo(nombre_paralelo)

    def obtener_horario_docente(self, cedula: str) -> dict | None:
        """
        Retorna el dict del horario de un docente desde el JSON.
        Wagner: usar para poblar la vista de horario en el panel docente.
        """
        return self.gestor_horarios_docentes.obtener_horario_docente(cedula)

    def mostrar_horario_docente(self, cedula: str):
        self.gestor_horarios_docentes.mostrar_horario_docente(cedula)

    def guardar_horarios_docentes(self, docentes: list):
        for docente in docentes:
            horario = self.gestor_cursos.obtener_horario_por_docente(docente.nombre)
            if horario:
                self.gestor_horarios_docentes.guardar_horario_docente(docente, horario)

    def crear_horario_paralelo(self, paralelo):
        return HorarioParalelo(paralelo)

    def crear_horario_docente(self, nombre_docente: str):
        return HorarioDocente(nombre_docente, self.gestor_cursos)

    def obtener_paralelos_guardados(self) -> list:
        """
        Retorna todos los paralelos guardados en el JSON.
        Wagner: usar para poblar un Combobox o tabla con los paralelos disponibles.
        """
        return self.gestor_horarios.cargar_paralelos()

    # -----------------------------------------------------------------------
    # TUTORÍAS
    # -----------------------------------------------------------------------

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

    # -----------------------------------------------------------------------
    # CALIFICACIONES
    # -----------------------------------------------------------------------

    def crear_calificacion(self, nota, fecha):
        calificacion = Calificaciones(nota, fecha)
        self.lista_notas.append(calificacion)
        return calificacion

    def verificar_aprobacion(self, calificacion) -> bool:
        """
        Retorna True si la nota es >= 7.
        Wagner: usar para mostrar "Aprobado" / "Reprobado" en la interfaz.
        """
        return calificacion.aprobar()

    # -----------------------------------------------------------------------
    # FÁBRICA
    # -----------------------------------------------------------------------

    def crear_usuario_con_fabrica(self, datos_usuario: dict):
        return self.fabrica_usuarios.crear_usuario(datos_usuario)
