import json

class Almacenamiento_Usuarios:

    def __init__(self,archivo = "users.json"):
        self.archivo = archivo

    def comprobar_duplicados(self,user,lista):
        for usuario in lista:
            if usuario['correo'] == user['correo']:
                return True
        return False
    
    def verificar_credenciales(self,correo_ingresado,contrasena_ingresada):
        try:
            with open(self.archivo,"r", encoding="utf-8") as archivo:
                datos_cargados = json.load(archivo)
        except Exception:
            print("No existe ningun usuario registrado por el momento")
            return False

        for usuario in datos_cargados:
            if usuario["correo"] == correo_ingresado and usuario["contraseña"] == contrasena_ingresada:
                return usuario
        return False
        
    def obtener(self,user):
        try:
            with open(self.archivo,"r", encoding="utf-8") as archivo:
                datos_cargados = json.load(archivo)
        except Exception:
            datos_cargados= []
        for i in datos_cargados:
            if user == i:
                True

        if self.comprobar_duplicados(user,datos_cargados) == True:
            print( "Error ya existe este usuario")
            return
        
        datos_cargados.append(user)
        try:
            with open(self.archivo,"w",encoding="utf-8") as archivo:
                json.dump(datos_cargados, archivo, indent=4, ensure_ascii=False)
            print("exito")
        except Exception:
            print("Ocurrio un fallo inseperado")