from estructura.facade_json import Facada_json

class Almacenamiento_Usuarios:

    def __init__(self):
        self.ruta = "Poo/Datos/users.json"
        self.json = Facada_json()
    
    def verificar_credenciales(self,correo_ingresado,contrasena_ingresada):
        datos_cargados = self.json.cargar_datos(self.ruta)
        if not datos_cargados:
            print("No existe ningun usuario registrado por el momento")
            return False
        
        for usuario in datos_cargados:
            if usuario["correo"] == correo_ingresado and usuario["contraseña"] == contrasena_ingresada:
                return usuario
        return False
        
    def obtener(self,user):
        try:
            if self.json.guardar_datos(self.ruta,'correo',user):
                print("exito")
            else: 
                print( "Error ya existe este usuario")
        except Exception as e:
            print("Ocurrio un fallo inseperado",e)