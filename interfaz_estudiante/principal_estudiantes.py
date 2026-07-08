# principal_estudiantes.py
import customtkinter as ctk 
from interfaz_estudiante.gestionar_matricula import GestionarMatricula
from interfaz_estudiante.ver_cursos import VerCursos
from facade_datos import FacadeDatos

class inicial_estudiantes(ctk.CTkToplevel):
    def __init__(self, inicio):
        super().__init__(inicio)
        self.title("Ventana Estudiantes")
        self.inicio = inicio
        self.gestion_matricula = None
        self.ventana_materias = None
        self.geometry("900x500")
        
        self.carrera_seleccionada = None
        self.paralelo_seleccionado = None
        self.datos_paralelo = None
        self.esta_matriculado = False
        
        self.facade = FacadeDatos()
        self.cedula_estudiante = self.obtener_cedula_login()
        
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Panel de Matricula Estudiantil",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)
        
        self.cargar_estado_matricula()
        
        self.mostrar_info_estudiante()
        
        self.crear_boton_volver()
        
        self.actualizar_botones()
    
    def obtener_cedula_login(self):
        if hasattr(self.inicio, 'entry_usuario'):
            return self.inicio.entry_usuario.get()
        return None
    
    def mostrar_info_estudiante(self):
        if self.cedula_estudiante:
            estudiante = self.facade.obtener_estudiante(self.cedula_estudiante)
            if estudiante:
                self.label_estudiante = ctk.CTkLabel(
                    self.frame_principal,
                    text=f"Estudiante: {estudiante.get('nombre', '')} {estudiante.get('apellido', '')}",
                    font=("Arial", 14)
                )
                self.label_estudiante.pack(pady=5)
    
    def cargar_estado_matricula(self):
        datos = self.facade.cargar_estado_matricula(self.cedula_estudiante)
        if datos:
            self.esta_matriculado = datos.get("esta_matriculado", False)
            self.carrera_seleccionada = datos.get("carrera", None)
            self.paralelo_seleccionado = datos.get("paralelo", None)
            self.datos_paralelo = datos.get("datos_paralelo", None)
    
    def guardar_estado_matricula(self):
        datos = {
            "cedula": self.cedula_estudiante,
            "esta_matriculado": self.esta_matriculado,
            "carrera": self.carrera_seleccionada,
            "paralelo": self.paralelo_seleccionado,
            "datos_paralelo": self.datos_paralelo,
            "fecha_matricula": self.datos_paralelo.get("fecha_matricula", "") if self.datos_paralelo else ""
        }
        self.facade.guardar_estado_matricula(datos)
    
    def actualizar_botones(self):
        for widget in self.frame_principal.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                if hasattr(widget, '_text') and widget._text in ["Gestionar Matricula", "Ver Mis Materias"]:
                    widget.destroy()
        
        if hasattr(self, 'label_estado'):
            self.label_estado.destroy()
        
        if self.esta_matriculado:
            self.label_estado = ctk.CTkLabel(
                self.frame_principal,
                text=f"Ya estas matriculado en: {self.paralelo_seleccionado}",
                font=("Arial", 14)
            )
            self.label_estado.pack(pady=10)
            
            self.boton_ver_materias = ctk.CTkButton(
                self.frame_principal,
                text="Ver Mis Materias",
                command=self.ver_mis_materias,
                width=250,
                height=50,
                font=("Arial", 16, "bold")
            )
            self.boton_ver_materias.pack(pady=20)
        else:
            self.label_estado = ctk.CTkLabel(
                self.frame_principal,
                text="Bienvenido al sistema de matricula",
                font=("Arial", 14)
            )
            self.label_estado.pack(pady=10)
            
            self.boton_gestionar_matricula = ctk.CTkButton(
                self.frame_principal,
                text="Gestionar Matricula",
                command=self.gestion_matricula_estudiante,
                width=250,
                height=50,
                font=("Arial", 16, "bold")
            )
            self.boton_gestionar_matricula.pack(pady=20)
        
        if hasattr(self, 'bton_volver'):
            self.bton_volver.pack_forget()
            self.bton_volver.pack(pady=10)
        
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self.frame_principal,
            text="Volver al Inicio",
            command=self.volver_inicio,
            width=150,
            height=40
        )
        self.bton_volver.pack(pady=10)

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()
        
    def gestion_matricula_estudiante(self):
        if self.gestion_matricula is None or not self.gestion_matricula.winfo_exists():
            self.gestion_matricula = GestionarMatricula(self, self.cedula_estudiante)
            self.gestion_matricula.crear_boton_volver()
            self.gestion_matricula.crear_widgets_matricula()
        else:
            self.gestion_matricula.deiconify()
        self.withdraw()
    
    def ver_mis_materias(self):
        if self.datos_paralelo:
            if self.ventana_materias is None or not self.ventana_materias.winfo_exists():
                self.ventana_materias = VerCursos(self, self.datos_paralelo, self)
                self.ventana_materias.crear_boton_volver()
                self.ventana_materias.mostrar_materias()
            else:
                self.ventana_materias.deiconify()
            self.withdraw()
    
    def actualizar_estado_matricula(self, carrera, paralelo, datos_paralelo):
        self.carrera_seleccionada = carrera
        self.paralelo_seleccionado = paralelo
        self.datos_paralelo = datos_paralelo
        self.esta_matriculado = True
        
        from datetime import datetime
        self.datos_paralelo["fecha_matricula"] = datetime.now().isoformat()
        
        self.guardar_estado_matricula()
        
        self.actualizar_botones()