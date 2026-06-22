# def validar_nombre(nombre):
#     var = input("Estas seguro que tu nombre es : ",nombre)
#     if var.lower() == "si":
#         return True
#     else:        return False

class Ingreso_datos:
        def __init__(self):
                self.roles=["Docente","Personal","Estudiante"]

        def agregar(self,num):
                nombre = input(f"Ingrese el nombre del {self.roles[num]}: ")
                apellido = input(f"Ingrese el apellido del {self.roles[num]}: ")
                correo = input(f"Ingrese el correo del {self.roles[num]}: ")
                contrasena = input(f"Ingrese la contraseña del {self.roles[num]}: ")
                rol = self.roles[num]
                #estudiante = Estudiante(nombre,apellido,correo,contrasena,rol)
                user ={  
                "nombre": nombre,
                "apellido": apellido,
                "correo" : correo,
                "contraseña" : contrasena,
                "rol": rol }
                return user
