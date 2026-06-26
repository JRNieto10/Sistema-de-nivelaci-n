
class Ingreso_datos:
    def __init__(self):
        self.roles=["Docente","Personal","Estudiante"]

    def agregar(self,num):
        nombre = input(f"Ingrese el nombre del {self.roles[num]}: ")
        apellido = input(f"Ingrese el apellido del {self.roles[num]}: ")
        correo = input(f"Ingrese el correo del {self.roles[num]}: ")
        contrasena = input(f"Ingrese la contraseña del {self.roles[num]}: ")
        rol = self.roles[num].lower()
        user = {  
            "nombre": nombre,
            "apellido": apellido,
            "correo" : correo,
            "contrasena" : contrasena,
            "rol": rol
        }
        return user