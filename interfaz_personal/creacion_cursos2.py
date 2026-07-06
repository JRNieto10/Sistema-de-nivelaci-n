import customtkinter as ctk

class Cursos_crear2(ctk.CTkToplevel):
    def __init__(self,principal):
        super().__init__(principal)
        self.title("creacion completa")
        self.principal = principal
        self.carrera =None
        self.geometry("900x500")
 
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_principal
        )
        self.bton_volver.pack()

    def volver_principal(self):
        self.destroy()
        self.principal.deiconify()
        