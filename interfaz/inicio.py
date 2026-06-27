import customtkinter as ctk
from interfaz.login import Login
from interfaz.eleccion import Eleccion

class Inicio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.loginn = None
        self.registroo = None
        self.eleccionn = None

        self.geometry("900x500")
        self.title("Principal")

    def crear_boton_login(self):
        self.bton = ctk.CTkButton(self, text="Iniciar Sesión", command=self.abrir_login)
        self.bton.pack()

    def abrir_login(self):
        if self.loginn is None or not self.loginn.winfo_exists():
            self.loginn = Login(self)
            self.loginn.crear_boton_volver()
            self.loginn.crear_entrada_cedula()
            self.loginn.crear_entrada_contraseña()
            self.loginn.combox_rol()
            self.loginn.boton_enviar()
        else:
            self.loginn.deiconify()

        self.withdraw()

    def final(self):
        self.mainloop()

    def boton_ir_eleccion(self):
        self.bton_ir_eleccion = ctk.CTkButton(
            self, text="Registrarse", command=self.ir_eleccion
        )
        self.bton_ir_eleccion.pack()
        
    def ir_eleccion(self):
        if self.eleccionn is None or not self.eleccionn.winfo_exists():
            self.eleccionn = Eleccion(self)
            self.eleccionn.boton_volver()
            self.eleccionn.combobox_rol()
     

           
        else:
            self.eleccionn.deiconify()

        self.withdraw()
