import customtkinter as ctk 
from interfaz_docente.creacion_tutorias import Crear_tutoria


class Asignaturas(ctk.CTkToplevel):
    def __init__(self,inicio):
        super().__init__(inicio)
        self.title("ventana docente")
        self.inicio = inicio
        self.creacion_tutoria=None
        self.geometry("900x500")
        
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_inicio
        )
        self.bton_volver.pack()

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()
        
    def boton_crear_tutoria(self):
        self.bton_crear_tutoria = ctk.CTkButton(
            self, text="crear tutoria", command=self.crear_tutoria
        )
        self.bton_crear_tutoria.pack()
        
    def crear_tutoria(self):
        if self.creacion_tutoria is None or not self.creacion_tutoria.winfo_exists():
            self.creacion_tutoria = Crear_tutoria(self)
            self.creacion_tutoria.crear_boton_volver()
        
        else:
            self.creacion_tutoria.deiconify()

        self.withdraw()
        
        
