# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from estructura.Almacenamiento_horario import GuardarHorarios


class VentanaCrearTutoria(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Programar Tutoría por Materia")
        self.geometry("560x620")
        self.grab_set()
        self.gestor = GuardarHorarios()
        self.paralelos_docente = self.auth.usuario_actual.ver_materias_asignadas()
        self.mapa_opciones = {}
        self.checks_estudiantes = {}

        ctk.CTkLabel(self, text="Programar tutoría", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self, text="La tutoría queda ligada a una materia creada y solo la verán estudiantes matriculados en esa materia.", wraplength=490, text_color="gray").pack(pady=(0, 8))

        self.entry_id = ctk.CTkEntry(self, placeholder_text="ID Tutoría", width=380)
        self.entry_id.pack(pady=6)

        self.entry_fecha = ctk.CTkEntry(self, placeholder_text="Fecha (AAAA-MM-DD)", width=380)
        self.entry_fecha.pack(pady=6)

        self.entry_tema = ctk.CTkEntry(self, placeholder_text="Tema", width=380)
        self.entry_tema.pack(pady=6)

        ctk.CTkLabel(self, text="Materia / Paralelo:").pack(pady=(10, 3))
        self.combo_materia = ctk.CTkComboBox(self, values=self._valores_materia(), width=430, command=lambda _: self.cargar_estudiantes())
        self.combo_materia.pack(pady=5)

        ctk.CTkLabel(self, text="Estudiantes obligatorios:", font=("Arial", 13, "bold")).pack(pady=(12, 2))
        self.frame_estudiantes = ctk.CTkScrollableFrame(self, width=470, height=250)
        self.frame_estudiantes.pack(pady=6)

        self.lbl_mensaje = ctk.CTkLabel(self, text="", text_color="red", wraplength=490)
        self.lbl_mensaje.pack(pady=5)

        ctk.CTkButton(self, text="Programar", fg_color="#2ecc71", command=self.guardar).pack(pady=12)
        self.cargar_estudiantes()

    def _valores_materia(self):
        opciones = []
        for p in self.paralelos_docente:
            materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
            asignaciones = p.get("docentes_por_materia", {})
            for materia in materias:
                if asignaciones.get(materia) == self.auth.usuario_actual.cedula or p.get("docente_cedula") == self.auth.usuario_actual.cedula:
                    texto = f"{p.get('id')} - {p.get('nombre')} | {materia}"
                    opciones.append(texto)
                    self.mapa_opciones[texto] = (p.get("id"), materia, p)
        return opciones or ["Sin materias asignadas"]

    def cargar_estudiantes(self):
        for w in self.frame_estudiantes.winfo_children():
            w.destroy()
        self.checks_estudiantes = {}
        data = self.mapa_opciones.get(self.combo_materia.get())
        if not data:
            ctk.CTkLabel(self.frame_estudiantes, text="No hay materia seleccionada.", text_color="gray").pack(anchor="w")
            return
        paralelo_id, materia, paralelo = data
        estudiantes = self.gestor.estudiantes_de_materia(paralelo_id, materia)
        if not estudiantes:
            ctk.CTkLabel(self.frame_estudiantes, text="No hay estudiantes matriculados en esta materia/paralelo.", text_color="gray").pack(anchor="w")
            return
        for cedula in estudiantes:
            var = ctk.BooleanVar(value=False)
            self.checks_estudiantes[cedula] = var
            ctk.CTkCheckBox(self.frame_estudiantes, text=cedula, variable=var).pack(anchor="w", pady=2)

    def guardar(self):
        data = self.mapa_opciones.get(self.combo_materia.get())
        if not data:
            self.lbl_mensaje.configure(text="Seleccione una materia válida.")
            return
        if not self.entry_id.get().strip() or not self.entry_tema.get().strip():
            self.lbl_mensaje.configure(text="ID y tema son obligatorios.")
            return
        paralelo_id, materia, _ = data
        obligatorios = [ced for ced, var in self.checks_estudiantes.items() if var.get()]
        self.auth.usuario_actual.crear_tutoria(
            self.entry_id.get().strip(),
            self.entry_fecha.get().strip(),
            self.entry_tema.get().strip(),
            materia,
            paralelo_id,
            obligatorios,
        )
        self.lbl_mensaje.configure(text_color="green", text="Tutoría programada para la materia seleccionada.")
        self.after(900, self.destroy)
