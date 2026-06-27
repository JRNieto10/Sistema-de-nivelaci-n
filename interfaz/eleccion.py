import customtkinter as ctk
from interfaz.registro import Registro

class Eleccion(ctk.CTkToplevel):
    def __init__(self, inicio):
        super().__init__()
        self.inicio = inicio
        self.title("Elección de rol")
        self.geometry("400x300")

        self.label_rol = None
        self.combo_rol = None
        self.bton_seleccionar = None
        self.bton_continuar = None
        self.registroo = None
        
    def boton_volver(self):
        self.bton_volver = ctk.CTkButton(self, text="Volver", command=self.volver_inicio)
        self.bton_volver.pack(pady=10)
    
    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()

        

    
    def combobox_rol(self):
        self.label_rol = ctk.CTkLabel(self, text="Seleccione su rol:")
        self.label_rol.pack(pady=10)
        self.combo_rol = ctk.CTkComboBox(
            self, values=["Estudiante", "Docente", "Administrador"]
        )
        self.combo_rol.pack(pady=10)
        self.bton_seleccionar = ctk.CTkButton(
            self, text="Seleccionar", command=self.seleccionar_rol
        )
        self.bton_seleccionar.pack(pady=10)
        
    def seleccionar_rol(self):
        rol_seleccionado = self.combo_rol.get()
        if rol_seleccionado == "Estudiante":
            self.label_rol.configure(text="Has seleccionado el rol de Estudiante")
            
        elif rol_seleccionado == "Docente":
            self.label_rol.configure(text="Has seleccionado el rol de Docente")
        elif rol_seleccionado == "Administrador":
            self.label_rol.configure(text="Has seleccionado el rol de Administrador")
            
            
        if self.bton_continuar is None:
            self.boton_continuar_registro()
        else:
            self.bton_continuar.pack_forget()
            self.bton_continuar.pack(pady=10)
            
            
            
    def boton_continuar_registro(self):
        self.bton_continuar = ctk.CTkButton(
            self, text="Continuar al registro", command=self.continuar_registro
        )
        self.bton_continuar.pack(pady=10)               
        
    def continuar_registro(self):
        if self.registroo is None or not self.registroo.winfo_exists():
            self.registroo = Registro(self)
            self.registroo.input_cedula()
            self.registroo.boton_validar_cedula()
            self.registroo.crear_boton_volver()
            self.registroo.mostrar_rol()
        else:
            self.registroo.deiconify()

        self.withdraw()
        
