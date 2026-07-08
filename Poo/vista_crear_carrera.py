import customtkinter as ctk
from estructura.entidades import Carrera

class VentanaCrearCarrera(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Crear Nueva Carrera")
        self.geometry("300x350")
        self.grab_set()

        self.entry_id = ctk.CTkEntry(self, placeholder_text="ID Carrera")
        self.entry_id.pack(pady=10)
        
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre de Carrera")
        self.entry_nombre.pack(pady=10)
        
        self.entry_duracion = ctk.CTkEntry(self, placeholder_text="Duración (semestres)")
        self.entry_duracion.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(self, text="Guardar Carrera", command=self.guardar_carrera)
        self.btn_guardar.pack(pady=20)

    def guardar_carrera(self):
        # Llamada al método de Personal (Admin)
        self.auth.usuario_actual.crear_carrera(
            self.entry_id.get(), 
            self.entry_nombre.get(), 
            self.entry_duracion.get()
        )
        self.destroy()