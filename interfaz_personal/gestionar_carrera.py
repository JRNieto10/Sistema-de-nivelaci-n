import customtkinter as ctk 
from interfaz_personal.creacion_carrera import Crear_carrera
from interfaz_personal.eleccion_carrera import Carrera_seleccionada


class Gestionar_carrera(ctk.CTkToplevel):
    def __init__(self,principal):
        super().__init__(principal)
        self.title("gestion de carrera")
        self.principal = principal
        self.carrera =None
        self.avanzar =None
        self.geometry("900x500")
 
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_principal
        )
        self.bton_volver.pack()

    def volver_principal(self):
        self.destroy()
        self.principal.deiconify()
        
    def boton_crear_carrera(self):
        self.bton = ctk.CTkButton(self, text="crear carrera", command=self.crear_carrera)
        self.bton.pack()

    def crear_carrera(self):
        if self.carrera is None or not self.carrera.winfo_exists():
            self.carrera = Crear_carrera(self)
            self.carrera.crear_boton_volver()
        
        else:
            self.carrera.deiconify()

        self.withdraw()


    def boton_avanzar_carrera(self):
        self.bton = ctk.CTkButton(self, text="seleccionar carrera", command=self.avanzar_carrera)
        self.bton.pack()

    def avanzar_carrera(self):
        if self.avanzar is None or not self.avanzar.winfo_exists():
            self.avanzar = Carrera_seleccionada(self)
            self.avanzar.crear_boton_volver()
            self.avanzar.boton_crear_cursos()
            self.avanzar.boton_crear_asignaturas()
            self.avanzar.boton_gestionar_permitidos()
        
        else:
            self.avanzar.deiconify()

        self.withdraw()
