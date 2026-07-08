import customtkinter as ctk
from interfaz_personal.gestionar_carrera import Gestionar_carrera

class inicial_personal(ctk.CTkToplevel):
    def __init__(self, inicio):
        super().__init__(inicio)
        self.title("Ventana Personal")
        self.inicio = inicio
        self.gestion = None
        self.geometry("900x500")

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Panel de Gestion Personal",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self.frame_principal,
            text="Volver al Inicio",
            command=self.volver_inicio,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150,
            height=40
        )
        self.bton_volver.pack(pady=10)

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()

    def boton_gestionar_carreras(self):
        self.bton_gestionar_carreras = ctk.CTkButton(
            self.frame_principal,
            text="Gestionar Carreras",
            command=self.gestion_carrera,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=200,
            height=50,
            font=("Arial", 14)
        )
        self.bton_gestionar_carreras.pack(pady=20)

    def gestion_carrera(self):
        if self.gestion is None or not self.gestion.winfo_exists():
            self.gestion = Gestionar_carrera(self)
            self.gestion.crear_boton_volver()
            self.gestion.boton_crear_carrera()
            self.gestion.boton_seleccionar_carrera()
        else:
            self.gestion.deiconify()
            if hasattr(self.gestion, 'actualizar_lista_carreras'):
                self.gestion.actualizar_lista_carreras()

        self.withdraw()