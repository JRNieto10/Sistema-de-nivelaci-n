# Aqui se implementa el Controlador (MVC)
# Esta clase conecta el login con los modelos de usuario.
# autenticacion.py
from estructura.AlmacenamietoUsuarios import *
# Importamos tu nueva Fábrica (ajusta la ruta de carpetas si es necesario)
from estructura.fabrica_usuarios import FabricaUsuarios 

class Autenticacion:
    def __init__(self, almacenamiento: Almacenamiento_Usuarios):
        self.almacenamiento = almacenamiento
        self.fabrica = FabricaUsuarios()  # 💡 Instanciamos tu fábrica aquí
        self.usuario_actual = None

    def iniciar_sesion(self, correo, contrasena):
        # 1. El almacenamiento busca en el JSON y nos devuelve un diccionario plano (si coincide)
        usuario_dict = self.almacenamiento.verificar_credenciales(correo, contrasena)
        
        if usuario_dict:
            try:
                # 2. 💡 ¡Aquí usamos tu Fábrica! Convertimos el diccionario en un OBJETO REAL (Docente/Estudiante/Personal)
                self.usuario_actual = self.fabrica.crear_usuario(usuario_dict)
                
                # Corregido: Comillas simples en el f-string para evitar el SyntaxError
                print(f"El {self.usuario_actual.rol} {self.usuario_actual.nombre} ha iniciado sesión correctamente")
                return True
            except ValueError as e:
                print(f"Error en la fábrica: {e}")
                return False
                
        print("Credenciales incorrectas")
        return False

    def cerrar_sesion(self):
        if self.usuario_actual:
            print(f"El {self.usuario_actual.rol} {self.usuario_actual.nombre} ha cerrado sesión")
            self.usuario_actual = None
        else:
            print("No hay sesiones activas")