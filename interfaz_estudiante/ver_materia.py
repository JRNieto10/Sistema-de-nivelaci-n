# ver_materia.py
import customtkinter as ctk

class VerMateria(ctk.CTkToplevel):
    def __init__(self, principal, materia, app_principal):
        super().__init__(principal)
        self.title("Detalles de la Materia")
        self.principal = principal
        self.materia = materia
        self.app_principal = app_principal
        self.geometry("700x500")
        
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text=f"{materia.get('nombre', 'Materia')}",
            font=("Arial", 26, "bold")
        )
        self.titulo.pack(pady=20)
        
        self.frame_info = ctk.CTkFrame(self.frame_principal)
        self.frame_info.pack(pady=20, fill="both", expand=True)
    
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self.frame_principal,
            text="Volver a Materias",
            command=self.volver_materias,
            width=150,
            height=40
        )
        self.bton_volver.pack(pady=20)
    
    def volver_materias(self):
        self.destroy()
        self.principal.deiconify()
    
    def mostrar_detalles(self):
        self.crear_fila_info("Nombre:", self.materia.get('nombre', 'No especificado'))
        
        self.crear_fila_info("Aula:", self.materia.get('aula', 'No especificada'))
        
        docente = self.materia.get('docente')
        if docente and isinstance(docente, dict):
            nombre_completo = f"{docente.get('nombre', '')} {docente.get('apellido', '')}".strip()
            self.crear_fila_info("Docente:", nombre_completo if nombre_completo else 'No especificado')
            self.crear_fila_info("Correo:", docente.get('correo', 'No especificado'))
            self.crear_fila_info("Cedula:", docente.get('cedula', 'No especificada'))
        else:
            self.crear_fila_info("Docente:", "No asignado")
        
        label_estado = ctk.CTkLabel(
            self.frame_info,
            text="Estado: Matriculado",
            font=("Arial", 16, "bold")
        )
        label_estado.pack(pady=15, anchor="w", padx=20)
        
        ctk.CTkFrame(self.frame_info, height=2).pack(pady=10, padx=20, fill="x")
        
        label_paralelo = ctk.CTkLabel(
            self.frame_info,
            text=f"Paralelo: {self.app_principal.paralelo_seleccionado}",
            font=("Arial", 14)
        )
        label_paralelo.pack(pady=5, anchor="w", padx=20)
        
        label_carrera = ctk.CTkLabel(
            self.frame_info,
            text=f"Carrera: {self.app_principal.carrera_seleccionada}",
            font=("Arial", 14)
        )
        label_carrera.pack(pady=5, anchor="w", padx=20)
    
    def crear_fila_info(self, label, valor):
        frame_fila = ctk.CTkFrame(self.frame_info, fg_color="transparent")
        frame_fila.pack(pady=8, anchor="w", padx=20, fill="x")
        
        label_info = ctk.CTkLabel(
            frame_fila,
            text=label,
            font=("Arial", 14, "bold"),
            width=120
        )
        label_info.pack(side="left")
        
        valor_info = ctk.CTkLabel(
            frame_fila,
            text=valor,
            font=("Arial", 14)
        )
        valor_info.pack(side="left", padx=10)