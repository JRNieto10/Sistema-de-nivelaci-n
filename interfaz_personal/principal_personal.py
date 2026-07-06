import customtkinter as ctk 
from interfaz_personal.gestionar_carrera import Gestionar_carrera

class inicial_personal(ctk.CTkToplevel):
    def __init__(self,inicio):
        super().__init__(inicio)
        self.title("ventana personal")
        self.inicio = inicio
        self.gestion=None
        self.geometry("900x500")
        
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_inicio
        )
        self.bton_volver.pack()

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()
        
    def boton_gestionar_carreras(self):
        self.bton_gestionar_carreras = ctk.CTkButton(
            self, text="Gestionar Carreras", command=self.gestion_carrera
        )
        self.bton_gestionar_carreras.pack()
        

    def gestion_carrera(self):
        if self.gestion is None or not self.gestion.winfo_exists():
            self.gestion = Gestionar_carrera(self)
            self.gestion.crear_boton_volver()
            self.gestion.boton_crear_carrera()
            self.gestion.boton_avanzar_carrera()

         
        else:
            self.gestion.deiconify()

        self.withdraw()
