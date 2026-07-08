import customtkinter as ctk
from estructura.Almacenamiento_materias import CreadorAcademico

class VentanaMatricularDocente(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.almacenador = CreadorAcademico()
        
        self.title("Matricular Docente")
        self.geometry("300x350")
        
        # Obtener carreras
        carreras = self.almacenador.json.repo.leer_todo()
        
        # Widgets
        ctk.CTkLabel(self, text="Seleccione Carrera:").pack(pady=5)
        self.combo_carreras = ctk.CTkComboBox(self, values=[c['nombre'] for c in carreras])
        self.combo_carreras.pack(pady=5)
        
        ctk.CTkLabel(self, text="ID Docente:").pack(pady=5)
        self.entry_docente = ctk.CTkEntry(self)
        self.entry_docente.pack(pady=5)
        
        # (Aquí podrías añadir otro ComboBox para materias filtradas)
        self.entry_materia = ctk.CTkEntry(self, placeholder_text="Nombre Materia")
        self.entry_materia.pack(pady=5)
        
        ctk.CTkButton(self, text="Confirmar Matrícula", command=self.guardar).pack(pady=20)

    def guardar(self):
        if self.almacenador.matricular_docente(self.entry_docente.get(), self.combo_carreras.get(), self.entry_materia.get()):
            self.destroy()