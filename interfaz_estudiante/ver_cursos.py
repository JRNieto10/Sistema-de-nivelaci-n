import customtkinter as ctk
from interfaz_estudiante.ver_materia import VerMateria

class VerCursos(ctk.CTkToplevel):
    def __init__(self, principal, paralelo, app_principal):
        super().__init__(principal)
        self.title("Materias del Paralelo")
        self.principal = principal
        self.paralelo = paralelo
        self.app_principal = app_principal
        self.ventana_materia = None
        self.geometry("900x600")
        
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text=f"Materias - {paralelo['nombre']}",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=10)
        
        self.subtitulo = ctk.CTkLabel(
            self.frame_principal,
            text=f"Carrera: {app_principal.carrera_seleccionada} | Aula: {paralelo['aula']} | Horario: {paralelo['horario']}",
            font=("Arial", 14)
        )
        self.subtitulo.pack(pady=5)
        
        self.frame_materias = ctk.CTkScrollableFrame(
            self.frame_principal,
            label_text="Materias del Paralelo",
            label_font=("Arial", 18, "bold")
        )
        self.frame_materias.pack(pady=20, padx=20, fill="both", expand=True)
    
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self.frame_principal,
            text="Volver al Inicio",
            command=self.volver_principal,
            width=150,
            height=40
        )
        self.bton_volver.pack(pady=10)
    
    def volver_principal(self):
        self.destroy()
        self.app_principal.deiconify()
    
    def mostrar_materias(self):
        materias = self.paralelo.get("materias", [])
        
        if materias:
            for i, materia in enumerate(materias):
                frame_card = ctk.CTkFrame(
                    self.frame_materias,
                    border_width=2,
                    corner_radius=10
                )
                frame_card.pack(pady=10, fill="x")
                
                def crear_comando(materia_data):
                    return lambda: self.ver_detalle_materia(materia_data)
                
                label_nombre = ctk.CTkLabel(
                    frame_card,
                    text=f"{materia.get('nombre', f'Materia {i+1}')}",
                    font=("Arial", 18, "bold"),
                    cursor="hand2"
                )
                label_nombre.pack(pady=5, padx=15, anchor="w")
                label_nombre.bind("<Button-1>", lambda e, m=materia: self.ver_detalle_materia(m))
                
                docente = materia.get("docente")
                if docente and isinstance(docente, dict):
                    nombre_docente = f"{docente.get('nombre', '')} {docente.get('apellido', '')}".strip()
                    if nombre_docente:
                        label_docente = ctk.CTkLabel(
                            frame_card,
                            text=f"Docente: {nombre_docente}",
                            font=("Arial", 13)
                        )
                        label_docente.pack(pady=2, padx=15, anchor="w")
                
                btn_ver = ctk.CTkButton(
                    frame_card,
                    text="Ver Detalles",
                    command=lambda m=materia: self.ver_detalle_materia(m),
                    width=120,
                    height=30,
                    font=("Arial", 12)
                )
                btn_ver.pack(pady=10, padx=15, anchor="e")
                
                label_estado = ctk.CTkLabel(
                    frame_card,
                    text="INSCRITO",
                    font=("Arial", 12, "bold")
                )
                label_estado.pack(pady=2, padx=15, anchor="e")
        else:
            label_no_materias = ctk.CTkLabel(
                self.frame_materias,
                text="No hay materias disponibles en este paralelo",
                font=("Arial", 16, "bold")
            )
            label_no_materias.pack(pady=30)
    
    def ver_detalle_materia(self, materia):
        if self.ventana_materia is None or not self.ventana_materia.winfo_exists():
            self.ventana_materia = VerMateria(self, materia, self.app_principal)
            self.ventana_materia.crear_boton_volver()
            self.ventana_materia.mostrar_detalles()
        else:
            self.ventana_materia.deiconify()
        self.withdraw()