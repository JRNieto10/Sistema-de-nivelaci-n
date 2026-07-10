# estructura/AlmacenamietoUsuarios.py
from estructura.facade_json import Facada_json

# Aqui se implementa el Modelo (MVC)
class Almacenamiento_Usuarios:

    def __init__(self):
        self.ruta = "Datos/users.json"
        self.json = Facada_json(self.ruta)
    
    # Aqui se hizo Metodo
    def verificar_credenciales(self, correo_ingresado, contrasena_ingresada):
        datos_cargados = self.json.repo.leer_todo()
        if not datos_cargados:
            print("No existe ningún usuario registrado por el momento")
            return False
        
        for usuario in datos_cargados:
            if usuario["correo"] == correo_ingresado and usuario["contraseña"] == contrasena_ingresada:
                return usuario
        return False
        

    def listar_usuarios(self):
        # Aqui se hizo Metodo
        return self.json.repo.leer_todo()

    def obtener_usuario_por_cedula(self, cedula):
        # Accedemos al repositorio a través de la fachada
        datos = self.json.repo.leer_todo()
        for usuario in datos:
            # Comparamos con la llave 'cedula' que debe existir en tu JSON
            if usuario.get("cedula") == cedula:
                return usuario
        return None

    # 🔴 ESTE ES EL MÉTODO QUE SOLUCIONA EL ATTRIBUTE-ERROR 🔴
    # Aqui se hizo Metodo
    def guardar_usuario_objeto(self, usuario_objeto):
        """
        Recibe un objeto real (Docente, Estudiante, Personal),
        extrae sus atributos y los guarda como un diccionario dentro del archivo JSON.
        """
        usuario_dict = {
            "cedula":usuario_objeto.cedula,
            "nombre": usuario_objeto.nombre,
            "apellido": usuario_objeto.apellido,
            "correo": usuario_objeto.correo,
            "contraseña": usuario_objeto.contrasena,  # Atributo mapeado de tus clases
            "rol": usuario_objeto.rol
        }
        try:
            # Enviamos el diccionario limpio a la Facade
            if self.json.guardar_datos('correo', usuario_dict):
                print(f"[Almacenamiento] {usuario_objeto.rol} registrado con éxito en el JSON.")
                return True
            else:
                print("[Almacenamiento] Error: El correo electrónico ya existe.")
                return False
        except Exception as e:
            print("Ocurrió un fallo inesperado al procesar el objeto de usuario:", e)
            return False
        
    