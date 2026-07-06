import customtkinter as ctk
from interfaz_personal.creacion_cursos2 import Cursos_crear2

class Cursos_crear(ctk.CTkToplevel):
    def __init__(self,principal):
        super().__init__(principal)
        self.title("gestion de carrera")
        self.principal = principal
        self.carrera2 =None
        self.geometry("900x500")
 
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_principal
        )
        self.bton_volver.pack()

    def volver_principal(self):
        self.destroy()
        self.principal.deiconify()
        
    def boton_finalizar_creacion(self):
        self.bton_finalizar = ctk.CTkButton(
            self, text="Finalizar cursos", command=self.finalizar_cursos
        )
        self.bton_finalizar.pack()
        
    def finalizar_cursos(self):
        if self.carrera2 is None or not self.carrera2.winfo_exists():
            self.carrera2 = Cursos_crear2(self)
            self.carrera2.crear_boton_volver()
        
        else:
            self.carrera2.deiconify()

        self.withdraw()