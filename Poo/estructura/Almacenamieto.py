from estructura.facade import *

class Almacenamiento_Usuarios:

    def __init__(self,archivo = "users.json"):
        self.archivo = archivo
        self.json = Facada_json()

    def comprobar_duplicados(self,user,lista):
        for usuario in lista:
            if usuario['correo'] == user['correo']:
                return True
        return False
    
    def verificar_credenciales(self,correo_ingresado,contrasena_ingresada):
        try:
            datos_cargados = self.json.cargar_datos(self.archivo)
        except Exception:
            print("No existe ningun usuario registrado por el momento")
            return False

        for usuario in datos_cargados:
            if usuario["correo"] == correo_ingresado and usuario["contraseña"] == contrasena_ingresada:
                return usuario
        return False
        
    def obtener(self,user):
        datos_cargados = self.json.cargar_datos(self.archivo)
        if not datos_cargados:
            datos_cargados= []
        for i in datos_cargados:
            if user == i:
                True

        if self.comprobar_duplicados(user,datos_cargados) == True:
            print( "Error ya existe este usuario")
            return
        
        datos_cargados.append(user)
        try:
            self.json.guardar_datos(self.archivo,datos_cargados)
            print("exito")
        except Exception as e:
            print("Ocurrio un fallo inseperado",e)