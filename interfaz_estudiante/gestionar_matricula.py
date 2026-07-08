# gestionar_matricula.py
import customtkinter as ctk
from tkinter import messagebox
from facade_datos import FacadeDatos

class GestionarMatricula(ctk.CTkToplevel):
    def __init__(self, principal, cedula_estudiante=None):
        super().__init__(principal)
        self.title("Gestion de Matricula")
        self.principal = principal
        self.cedula_estudiante = cedula_estudiante
        self.geometry("900x700")
        
        self.carrera_seleccionada = None
        self.paralelo_seleccionado = None
        self.datos_paralelo = None
        
        self.facade = FacadeDatos()
        
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Buscar Paralelos Disponibles",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)
        
        self.label_estado = ctk.CTkLabel(
            self.frame_principal,
            text="Ingresa el nombre de tu carrera",
            font=("Arial", 14)
        )
        self.label_estado.pack(pady=10)
        
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self.frame_principal,
            text="Volver",
            command=self.volver_principal,
            width=150,
            height=40
        )
        self.bton_volver.pack(pady=10)

    def volver_principal(self):
        self.destroy()
        self.principal.deiconify()
    
    def crear_widgets_matricula(self):
        if self.cedula_estudiante:
            label_cedula = ctk.CTkLabel(
                self.frame_principal,
                text=f"Cedula: {self.cedula_estudiante}",
                font=("Arial", 14)
            )
            label_cedula.pack(pady=5)
        
        frame_buscar = ctk.CTkFrame(self.frame_principal)
        frame_buscar.pack(pady=20, fill="x", padx=50)
        
        label_carrera = ctk.CTkLabel(
            frame_buscar,
            text="Nombre de la Carrera:",
            font=("Arial", 16, "bold")
        )
        label_carrera.pack(pady=10)
        
        self.entry_carrera = ctk.CTkEntry(
            frame_buscar,
            placeholder_text="Ej: software",
            width=400,
            height=45,
            font=("Arial", 14)
        )
        self.entry_carrera.pack(pady=10)
        
        btn_buscar = ctk.CTkButton(
            frame_buscar,
            text="Buscar Paralelos",
            command=self.buscar_paralelos,
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )
        btn_buscar.pack(pady=10)
        
        self.frame_paralelos = ctk.CTkScrollableFrame(
            self.frame_principal,
            label_text="Paralelos Disponibles",
            label_font=("Arial", 16, "bold")
        )
        self.frame_paralelos.pack(pady=20, padx=50, fill="both", expand=True)
        
        self.label_mensaje = ctk.CTkLabel(
            self.frame_paralelos,
            text="Busca una carrera para ver los paralelos disponibles",
            font=("Arial", 14)
        )
        self.label_mensaje.pack(pady=20)
    
    def buscar_paralelos(self):
        carrera = self.entry_carrera.get().strip().lower()
        
        if not carrera:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre de una carrera")
            return
        
        for widget in self.frame_paralelos.winfo_children():
            widget.destroy()
        
        self.carrera_seleccionada = carrera
        
        if not self.facade.carrera_existe(carrera):
            label_no_paralelos = ctk.CTkLabel(
                self.frame_paralelos,
                text="No hay paralelos disponibles para matricularse en esta carrera",
                font=("Arial", 16, "bold")
            )
            label_no_paralelos.pack(pady=30)
            return
        
        paralelos = self.facade.buscar_paralelos(carrera)
        
        if paralelos:
            self.mostrar_paralelos(paralelos)
        else:
            label_no_paralelos = ctk.CTkLabel(
                self.frame_paralelos,
                text="No hay paralelos disponibles para matricularse",
                font=("Arial", 16, "bold")
            )
            label_no_paralelos.pack(pady=30)
    
    def mostrar_paralelos(self, paralelos):
        for paralelo in paralelos:
            frame_card = ctk.CTkFrame(
                self.frame_paralelos,
                border_width=2,
                corner_radius=10
            )
            frame_card.pack(pady=10, fill="x")
            
            label_nombre = ctk.CTkLabel(
                frame_card,
                text=f"{paralelo['nombre']}",
                font=("Arial", 18, "bold")
            )
            label_nombre.pack(pady=5, padx=15, anchor="w")
            
            label_aula = ctk.CTkLabel(
                frame_card,
                text=f"Aula: {paralelo['aula']}",
                font=("Arial", 13)
            )
            label_aula.pack(pady=2, padx=15, anchor="w")
            
            label_horario = ctk.CTkLabel(
                frame_card,
                text=f"Horario: {paralelo['horario']}",
                font=("Arial", 13)
            )
            label_horario.pack(pady=2, padx=15, anchor="w")
            
            materias = paralelo.get("materias", [])
            label_materias = ctk.CTkLabel(
                frame_card,
                text=f"Materias: {len(materias)}",
                font=("Arial", 13)
            )
            label_materias.pack(pady=2, padx=15, anchor="w")
            
            btn_matricular = ctk.CTkButton(
                frame_card,
                text="Matricularse",
                command=lambda p=paralelo: self.solicitar_confirmacion_matricula(p),
                width=150,
                height=35,
                font=("Arial", 14, "bold")
            )
            btn_matricular.pack(pady=10, padx=15, anchor="e")
    
    def solicitar_confirmacion_matricula(self, paralelo):
        respuesta = messagebox.askyesno(
            "Confirmar Matricula",
            f"¿Estas seguro de que deseas matricularte en {paralelo['nombre']}?"
        )
        
        if respuesta:
            if self.cedula_estudiante:
                if not self.facade.verificar_estudiante_existe(self.cedula_estudiante):
                    messagebox.showerror(
                        "Error",
                        "Tu cedula no esta registrada en el sistema. Contacta al administrador."
                    )
                    return
            
            self.matricularse(paralelo)
    
    def matricularse(self, paralelo):
        self.principal.actualizar_estado_matricula(
            self.carrera_seleccionada,
            paralelo["nombre"],
            paralelo
        )
        
        messagebox.showinfo(
            "Matricula Exitosa",
            f"Te has matriculado exitosamente en {paralelo['nombre']}!"
        )
        
        self.destroy()
        self.principal.deiconify()