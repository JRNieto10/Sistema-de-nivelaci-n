import customtkinter as ctk
from interfaz_docente.tutorias import Tutorias


class Horario(ctk.CTkToplevel):
    def __init__(self,inicio):
        super().__init__(inicio)
        self.title("ventana docente")
        self.inicio = inicio
        self.asignatura = None
        self.tutorias = None
        self.geometry("900x500")
        
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_inicio
        )
        self.bton_volver.pack()

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()
        
    def boton_seleccionar_materia(self):
        self.bton_ver_horarios = ctk.CTkButton(
            self, text="seleccionar materia", command=self.seleccionar_materia
        )
        self.bton_ver_horarios.pack()
        
    def seleccionar_materia(self):
        pass
        
    def bton_tutorias_pendientes(self):
        self.bton_ver_horarios = ctk.CTkButton(
            self, text="Tutorias", command=self.tutorias_pendientes
        )
        self.bton_ver_horarios.pack()
        
    def tutorias_pendientes(self):
        if self.tutorias is None or not self.tutorias.winfo_exists():
            self.tutorias = Tutorias(self)
            self.tutorias.crear_boton_volver()
        
        else:
            self.tutorias.deiconify()

        self.withdraw()
        
        
        