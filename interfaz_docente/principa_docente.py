import customtkinter as ctk 
from interfaz_docente.asignaturas import Asignaturas
from interfaz_docente.horarios import Horario
from interfaz_docente.perfil import Perfil

class inicial_docente(ctk.CTkToplevel):
    def __init__(self,inicio):
        super().__init__(inicio)
        self.title("ventana docente")
        self.inicio = inicio
        self.asignatura = None
        self.horario = None
        self.perfil=None
        self.geometry("900x500")
        
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_inicio
        )
        self.bton_volver.pack()

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()
        
    def boton_asignaturas(self):
        self.bton_ver_asignaturas = ctk.CTkButton(
            self, text="Ver asignaturas", command=self.ver_asignaturas
        )
        self.bton_ver_asignaturas.pack()
        
    def ver_asignaturas(self):
        if self.asignatura is None or not self.asignatura.winfo_exists():
            self.asignatura = Asignaturas(self)
            self.asignatura.crear_boton_volver()
            self.asignatura.boton_crear_tutoria()
        
        else:
            self.asignatura.deiconify()

        self.withdraw()
            
    def boton_horarios(self):
        self.bton_ver_horarios = ctk.CTkButton(
            self, text="Ver horarios", command=self.ver_horarios
        )
        self.bton_ver_horarios.pack()
        
    def ver_horarios(self):
        if self.horario is None or not self.horario.winfo_exists():
            self.horario = Horario(self)
            self.horario.crear_boton_volver()
            self.horario.boton_seleccionar_materia()
            self.horario.bton_tutorias_pendientes()
        
        else:
            self.horario.deiconify()

        self.withdraw()
        
        
    def boton_perfil(self):
        self.bton_perfil = ctk.CTkButton(
            self, text="Perfil", command=self.ver_perfil
        )
        self.bton_perfil.pack()
        
    def ver_perfil(self):
        if self.perfil is None or not self.perfil.winfo_exists():
            self.perfil = Perfil(self)
            self.perfil.crear_boton_volver()
     
        
        else:
            self.perfil.deiconify()

        self.withdraw()
        