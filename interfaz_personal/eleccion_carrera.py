import customtkinter as ctk
from interfaz_personal.creacion_cursos import Cursos_crear
from interfaz_personal.creacion_asignaturas import Asignaturas_crear    
from interfaz_personal.gestionar_permitidos import Permitidos_gestionar

class Carrera_seleccionada(ctk.CTkToplevel):
    def __init__(self,inicio):
        super().__init__(inicio)
        self.title("carrera seleccionada")
        self.inicio = inicio
        self.permitidos = None
        self.asignatura = None
        self.cursos = None
        self.geometry("900x500")
        
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_inicio
        )
        self.bton_volver.pack()

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()
        
        
    def boton_crear_cursos(self):
        self.bton = ctk.CTkButton(self, text="crear cursos", command=self.crear_cursos)
        self.bton.pack()
    
    def crear_cursos(self):
        if self.cursos is None or not self.cursos.winfo_exists():
            self.cursos = Cursos_crear(self)
            self.cursos.boton_finalizar_creacion()
            self.cursos.crear_boton_volver()

        
        else:
            self.cursos.deiconify()

        self.withdraw()
        
    def boton_crear_asignaturas(self):
        self.bton = ctk.CTkButton(self, text="crear asignaturas", command=self.crear_asignaturas)
        self.bton.pack()
        
    def crear_asignaturas(self):
        if self.asignatura is None or not self.asignatura.winfo_exists():
            self.asignatura = Asignaturas_crear(self)
            self.asignatura.crear_boton_volver()
        
        else:
            self.asignatura.deiconify()

        self.withdraw()
        
    def boton_gestionar_permitidos(self):
        self.bton = ctk.CTkButton(self, text="gestionar permitidos", command=self.gestionar_permitidos)
        self.bton.pack()
        
    def gestionar_permitidos(self):
        if self.permitidos is None or not self.permitidos.winfo_exists():
            self.permitidos = Permitidos_gestionar(self)
            self.permitidos.crear_boton_volver()
        
        else:
            self.permitidos.deiconify()

        self.withdraw()
        