# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from estructura.Almacenamiento_horario import GuardarHorarios
from estructura.Almacenamiento_carreras import Almacenamiento_Carreras


class VentanaCrearParalelo(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Crear Paralelo en Materia")
        self.geometry("540x620")
        self.grab_set()
        self.gestor = GuardarHorarios()
        self.carreras = Almacenamiento_Carreras().json.repo.leer_todo()
        self.mapa_materias = {}

        ctk.CTkLabel(self, text="Crear paralelo para materia existente", font=("Arial", 16, "bold")).pack(pady=(14, 6))
        ctk.CTkLabel(self, text="Primero se crea la materia. Luego aquí puede crear más paralelos para esa materia.", text_color="gray", wraplength=450).pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Carrera:").pack(pady=(6, 2))
        self.combo_carrera = ctk.CTkComboBox(self, values=self._valores_carreras(), width=390, command=lambda _: self.actualizar_materias())
        self.combo_carrera.pack(pady=4)

        ctk.CTkLabel(self, text="Materia creada:").pack(pady=(6, 2))
        self.combo_materia = ctk.CTkComboBox(self, values=["Sin materias"], width=390)
        self.combo_materia.pack(pady=4)

        ctk.CTkLabel(self, text="El codigo del paralelo se asigna automaticamente.", text_color="gray").pack(pady=(7, 2))
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre Paralelo (ejemplo: A)", width=390)
        self.entry_nombre.pack(pady=6)
        ctk.CTkLabel(self, text="Jornada:").pack(pady=(6, 2))
        self.combo_jornada = ctk.CTkComboBox(self, values=["Matutina", "Vespertina", "Nocturna"], width=390)
        self.combo_jornada.pack(pady=4)

        ctk.CTkButton(self, text="Crear Paralelo", fg_color="#2ecc71", command=self.guardar).pack(pady=12)
        self.lbl_mensaje = ctk.CTkLabel(self, text="", wraplength=450)
        self.lbl_mensaje.pack(pady=4)

        ctk.CTkLabel(self, text="Paralelos existentes", font=("Arial", 13, "bold")).pack(pady=(12, 4))
        self.texto_paralelos = ctk.CTkTextbox(self, width=470, height=220)
        self.texto_paralelos.pack(pady=6)
        self.actualizar_materias()
        self.cargar_resumen()

    def _valores_carreras(self):
        return [c.get("nombre") for c in self.carreras if c.get("nombre")] or ["Sin carreras"]

    def actualizar_materias(self):
        carrera_nombre = self.combo_carrera.get()
        materias = []
        self.mapa_materias = {}
        for c in self.carreras:
            if c.get("nombre") == carrera_nombre:
                for m in c.get("materias", []):
                    nombre = m.get("nombre")
                    if nombre and nombre not in materias:
                        materias.append(nombre)
                        self.mapa_materias[nombre] = m
        if not materias:
            materias = ["Sin materias"]
        self.combo_materia.configure(values=materias)
        self.combo_materia.set(materias[0])

    def guardar(self):
        materia = self.combo_materia.get().strip()
        nombre = self.entry_nombre.get().strip()
        jornada = self.combo_jornada.get().strip()
        if not nombre or not materia or materia.startswith("Sin"):
            self.lbl_mensaje.configure(text_color="red", text="Complete los datos y seleccione una materia existente.")
            return
        ok, msg = self.gestor.crear_paralelo_para_materia(nombre, jornada, materia)
        self.lbl_mensaje.configure(text_color="green" if ok else "red", text=msg)
        self.cargar_resumen()

    def cargar_resumen(self):
        self.texto_paralelos.delete("1.0", "end")
        paralelos = self.gestor.listar_paralelos()
        if not paralelos:
            self.texto_paralelos.insert("end", "No hay paralelos creados todavía.")
            return
        for p in paralelos:
            materias = p.get("materias", []) or ([] if not p.get("materia") else [p.get("materia")])
            self.texto_paralelos.insert("end", f"{p.get('id')} - {p.get('nombre')} ({p.get('jornada')})\n  Materias: {', '.join(materias) if materias else 'Sin materias'}\n  Estudiantes: {len(p.get('estudiantes', []))}\n\n")
