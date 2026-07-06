import customtkinter as ctk


class Permitidos_gestionar(ctk.CTkToplevel):
    def __init__(self,principal):
        super().__init__(principal)
        self.title("gestion de carrera")
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