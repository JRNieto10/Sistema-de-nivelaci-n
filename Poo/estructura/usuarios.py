from .clases_abstractas import Usuarios
from .interfaces import ActualizadorDatos
from estructura.entidades import Carrera
from estructura.Almacenamiento_carreras import Almacenamiento_Carreras
from .entidades import *

class Docente(Usuarios):
    def __init__(self, nombre, apellido, correo, contrasena, rol,cedula):
        super().__init__(nombre, apellido, correo, contrasena, rol,cedula) 

    # 🔒 CORREGIDO: Permisos exclusivos para el Docente
    @property
    def opciones_menu(self): return ["Mis Cursos", "Calificaciones"]

    def cambiar_contraseña(self, nueva_contra):
        self.contrasena = nueva_contra

class Estudiante(Usuarios):
    def __init__(self, nombre, apellido, correo, contrasena, rol,cedula):
        super().__init__(nombre, apellido, correo, contrasena, rol,cedula) 

    @property
    def opciones_menu(self): return ["Ver Notas", "Mis Horarios"]

    def cambiar_contraseña(self, nueva_contra):
        self.contrasena = nueva_contra
   

# 🔑 El Admin (Personal) adquiere la interfaz/herramienta
class Personal(Usuarios, ActualizadorDatos):
    def __init__(self, nombre, apellido, correo, contrasena, rol,cedula):
        super().__init__(nombre, apellido, correo, contrasena, rol,cedula) 

    @property
    def opciones_menu(self): 
        return [
            "Gestionar Usuarios", 
            "Crear Carreras", 
            "Crear Materias", 
            "Matricular Docentes",  # <--- Añade esto exactamente aquí
            "Reportes Globales"
        ]
    
    def cambiar_contraseña(self, nueva_contra):
        self.contrasena = nueva_contra

    def actualizar_datos_usuario(self, usuario_objetivo, nuevos_datos):
            """
            Modifica cualquier usuario (Estudiante, Docente o Personal).
            usuario_objetivo: El objeto instanciado (ej. un objeto Estudiante).
            nuevos_datos: Diccionario con los campos a actualizar.
            """
            # Lista de atributos permitidos para actualizar
            atributos_permitidos = ["nombre", "apellido", "correo", "contrasena"]
            
            for campo, valor in nuevos_datos.items():
                if campo in atributos_permitidos and hasattr(usuario_objetivo, campo):
                    setattr(usuario_objetivo, campo, valor)
            
            print(f"[Admin] Se han actualizado los datos de {usuario_objetivo.nombre} ({usuario_objetivo.rol}) con éxito.")

    # estructura/usuarios.py

    # estructura/usuarios.py

    def crear_carrera(self, id_carrera, nombre, duracion):
        # 1. Crear el objeto
        nueva_carrera = Carrera(id_carrera, nombre, duracion)
        
        # 2. Instanciar el almacenamiento SIN parámetros (CORRECCIÓN AQUÍ)
        almacenamiento = Almacenamiento_Carreras() 
        # 3. Guardar usando el método adecuado
        if almacenamiento.guardar_carrera(nueva_carrera):
            print(f"Carrera {nombre} guardada.")
        return nueva_carrera
        


            