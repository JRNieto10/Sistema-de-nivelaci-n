# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from estructura.Almacenamiento_evaluaciones import Almacenamiento_Evaluaciones


class VentanaCalificar(ctk.CTkToplevel):
    def __init__(self, master, auth, paralelo):
        super().__init__(master)
        self.auth = auth
        self.paralelo = paralelo
        self.title(f"Calificar actividades - {paralelo['nombre']}")
        self.geometry("470x520")
        self.grab_set()

        materias = paralelo.get("materias", []) or ([paralelo.get("materia")] if paralelo.get("materia") else [])
        asignadas = paralelo.get("docentes_por_materia", {})
        ced_docente = self.auth.usuario_actual.cedula
        self.materias_docente = [m for m in materias if asignadas.get(m) == ced_docente or paralelo.get("docente_cedula") == ced_docente]
        segmentos = Almacenamiento_Evaluaciones().nombres_segmentos()

        ctk.CTkLabel(self, text="Registrar actividad por segmento", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self, text="Las actividades se promedian dentro de su segmento y luego se suman para la nota final.", wraplength=410, text_color="gray").pack(pady=(0, 8))

        ctk.CTkLabel(self, text="Materia:").pack(pady=(8, 0))
        self.combo_materia = ctk.CTkComboBox(self, values=self.materias_docente or ["-- Sin materias asignadas --"], width=360, command=lambda _: self.actualizar_estudiantes())
        self.combo_materia.pack(pady=5)

        ctk.CTkLabel(self, text="Estudiante:").pack(pady=(8, 0))
        self.combo_estudiante = ctk.CTkComboBox(self, values=["-- Sin estudiantes inscritos --"], width=360)
        self.combo_estudiante.pack(pady=5)
        self.actualizar_estudiantes()

        ctk.CTkLabel(self, text="Segmento:").pack(pady=(8, 0))
        self.combo_segmento = ctk.CTkComboBox(self, values=segmentos or ["Evaluacion final"], width=360)
        self.combo_segmento.pack(pady=5)

        self.entry_actividad = ctk.CTkEntry(self, placeholder_text="Nombre de la actividad", width=360)
        self.entry_actividad.pack(pady=8)

        self.entry_nota = ctk.CTkEntry(self, placeholder_text="Nota de la actividad (0-10)", width=360)
        self.entry_nota.pack(pady=8)

        self.entry_fecha = ctk.CTkEntry(self, placeholder_text="Fecha (AAAA-MM-DD)", width=360)
        self.entry_fecha.pack(pady=8)

        self.lbl_mensaje = ctk.CTkLabel(self, text="", text_color="red", wraplength=410)
        self.lbl_mensaje.pack(pady=5)

        ctk.CTkButton(self, text="Guardar Actividad", fg_color="#2ecc71", command=self.guardar).pack(pady=15)

    def actualizar_estudiantes(self):
        from estructura.Almacenamiento_horario import GuardarHorarios
        materia = self.combo_materia.get()
        estudiantes = GuardarHorarios().estudiantes_de_materia(self.paralelo.get("id"), materia)
        valores = estudiantes or ["-- Sin estudiantes inscritos --"]
        self.combo_estudiante.configure(values=valores)
        self.combo_estudiante.set(valores[0])

    def guardar(self):
        cedula = self.combo_estudiante.get()
        materia = self.combo_materia.get()
        segmento = self.combo_segmento.get()
        actividad = self.entry_actividad.get().strip()

        if not cedula or cedula.startswith("--"):
            self.lbl_mensaje.configure(text_color="red", text="No hay estudiantes inscritos en este paralelo.")
            return
        if not materia or materia.startswith("--"):
            self.lbl_mensaje.configure(text_color="red", text="No hay materia válida para calificar.")
            return
        if not actividad:
            self.lbl_mensaje.configure(text_color="red", text="Ingrese el nombre de la actividad.")
            return
        try:
            nota = float(self.entry_nota.get())
        except ValueError:
            self.lbl_mensaje.configure(text_color="red", text="La nota debe ser un número.")
            return

        ok, msg = self.auth.usuario_actual.calificar_actividad(
            cedula, materia, segmento, actividad, nota, self.entry_fecha.get().strip(), self.paralelo.get("id", "")
        )
        self.lbl_mensaje.configure(text_color="green" if ok else "red", text=msg)
