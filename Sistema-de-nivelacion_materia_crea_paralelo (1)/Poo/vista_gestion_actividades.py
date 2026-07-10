# Aqui se implementa la Vista (MVC)
import os
import subprocess
import sys
import customtkinter as ctk
from tkinter import messagebox
from estructura.Almacenamiento_actividades import Almacenamiento_Actividades
from estructura.Almacenamiento_evaluaciones import Almacenamiento_Evaluaciones


class VentanaGestionActividades(ctk.CTkToplevel):
    def __init__(self, master, auth, paralelo):
        super().__init__(master)
        self.auth = auth
        self.paralelo = paralelo
        self.gestor = Almacenamiento_Actividades()
        self.title(f"Actividades - {paralelo.get('nombre')}")
        self.geometry("760x620")
        self.grab_set()
        self.materias = self._materias_docente()
        ctk.CTkLabel(self, text="Actividades de la materia", font=("Arial", 18, "bold")).pack(pady=(12, 5))
        self.combo_materia = ctk.CTkComboBox(self, values=self.materias or ["-- Sin materias --"], width=420, command=lambda _: self.cargar())
        self.combo_materia.pack(pady=6)
        ctk.CTkButton(self, text="+ Crear actividad", fg_color="#2ecc71", command=self.crear).pack(pady=7)
        self.frame = ctk.CTkScrollableFrame(self, width=700, height=460)
        self.frame.pack(padx=15, pady=10, fill="both", expand=True)
        self.cargar()

    def _materias_docente(self):
        materias = self.paralelo.get("materias") or ([self.paralelo.get("materia")] if self.paralelo.get("materia") else [])
        asignadas = self.paralelo.get("docentes_por_materia", {})
        cedula = self.auth.usuario_actual.cedula
        return [m for m in materias if asignadas.get(m) == cedula or self.paralelo.get("docente_cedula") == cedula]

    def cargar(self):
        for w in self.frame.winfo_children():
            w.destroy()
        materia = self.combo_materia.get()
        actividades = self.gestor.listar_actividades_docente(self.auth.usuario_actual.cedula, self.paralelo.get("id"), materia)
        if not actividades:
            ctk.CTkLabel(self.frame, text="Todavia no hay actividades en esta materia.", text_color="gray").pack(anchor="w")
            return
        for a in actividades:
            fila = ctk.CTkFrame(self.frame)
            fila.pack(fill="x", pady=6)
            texto = f"{a.get('nombre')} | {a.get('segmento')}\nPuntual: {a.get('fecha_limite')} | Cierre: {a.get('fecha_cierre')}"
            ctk.CTkLabel(fila, text=texto, justify="left", wraplength=540).pack(side="left", padx=10, pady=8)
            ctk.CTkButton(fila, text="Ver y calificar", width=120, command=lambda act=a: DetalleActividadDocente(self, self.auth, self.paralelo, act)).pack(side="right", padx=10)

    def crear(self):
        materia = self.combo_materia.get()
        if materia.startswith("--"):
            return
        CrearActividad(self, self.auth, self.paralelo, materia, self.cargar)


class CrearActividad(ctk.CTkToplevel):
    def __init__(self, master, auth, paralelo, materia, refrescar):
        super().__init__(master)
        self.auth, self.paralelo, self.materia, self.refrescar = auth, paralelo, materia, refrescar
        self.gestor = Almacenamiento_Actividades()
        self.title("Crear actividad")
        self.geometry("520x590")
        self.grab_set()
        ctk.CTkLabel(self, text=f"Nueva actividad - {materia}", font=("Arial", 16, "bold")).pack(pady=12)
        segmentos = Almacenamiento_Evaluaciones().nombres_segmentos()
        self.combo_segmento = ctk.CTkComboBox(self, values=segmentos, width=400)
        self.combo_segmento.pack(pady=6)
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre de la actividad", width=400)
        self.nombre.pack(pady=6)
        self.descripcion = ctk.CTkTextbox(self, width=400, height=120)
        self.descripcion.pack(pady=6)
        self.limite = ctk.CTkEntry(self, placeholder_text="Limite puntual: AAAA-MM-DD HH:MM", width=400)
        self.limite.pack(pady=6)
        self.cierre = ctk.CTkEntry(self, placeholder_text="Cierre definitivo: AAAA-MM-DD HH:MM", width=400)
        self.cierre.pack(pady=6)
        self.lbl = ctk.CTkLabel(self, text="", wraplength=440)
        self.lbl.pack(pady=7)
        ctk.CTkButton(self, text="Guardar actividad", fg_color="#2ecc71", command=self.guardar).pack(pady=10)

    def guardar(self):
        ok, msg = self.gestor.crear_actividad(
            self.auth.usuario_actual.cedula, self.paralelo.get("id"), self.materia,
            self.combo_segmento.get(), self.nombre.get(), self.descripcion.get("1.0", "end"),
            self.limite.get(), self.cierre.get())
        self.lbl.configure(text_color="green" if ok else "red", text=msg)
        if ok:
            self.refrescar()
            self.after(900, self.destroy)


class DetalleActividadDocente(ctk.CTkToplevel):
    def __init__(self, master, auth, paralelo, actividad):
        super().__init__(master)
        self.auth, self.paralelo, self.actividad = auth, paralelo, actividad
        self.gestor = Almacenamiento_Actividades()
        self.title(f"Calificar - {actividad.get('nombre')}")
        self.geometry("880x650")
        self.grab_set()
        ctk.CTkLabel(self, text=f"{actividad.get('nombre')} - {actividad.get('materia')}", font=("Arial", 17, "bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Seleccione un estudiante para revisar el archivo y colocar la nota.", text_color="gray").pack(pady=3)
        self.frame = ctk.CTkScrollableFrame(self, width=820, height=540)
        self.frame.pack(padx=15, pady=10, fill="both", expand=True)
        self.cargar()

    def cargar(self):
        for w in self.frame.winfo_children():
            w.destroy()
        from estructura.Almacenamiento_horario import GuardarHorarios
        estudiantes = GuardarHorarios().estudiantes_de_materia(
            self.paralelo.get("id"), self.actividad.get("materia")
        )
        filas = self.gestor.entregas_actividad(self.actividad.get("id"), estudiantes)
        for item in filas:
            cedula, entrega = item["cedula"], item["entrega"]
            fila = ctk.CTkFrame(self.frame)
            fila.pack(fill="x", pady=5)
            estado = "No ha subido" if not entrega else f"Subio: {entrega.get('estado_entrega')} | Nota: {entrega.get('nota') if entrega.get('nota') is not None else 'pendiente'}"
            ctk.CTkLabel(fila, text=f"{cedula}\n{estado}", justify="left", width=280).pack(side="left", padx=8, pady=8)
            if entrega and entrega.get("archivo"):
                ctk.CTkButton(fila, text="Abrir archivo", width=100, command=lambda e=entrega: self.abrir_archivo(e)).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(fila, text="Sin archivo", width=100, text_color="gray").pack(side="left", padx=5)
            nota = ctk.CTkEntry(fila, placeholder_text="Nota", width=80)
            if entrega and entrega.get("nota") is not None:
                nota.insert(0, str(entrega.get("nota")))
            nota.pack(side="left", padx=5)
            obs = ctk.CTkEntry(fila, placeholder_text="Observacion", width=190)
            if entrega and entrega.get("observacion"):
                obs.insert(0, entrega.get("observacion"))
            obs.pack(side="left", padx=5)
            ctk.CTkButton(fila, text="Calificar", width=90, command=lambda c=cedula, n=nota, o=obs: self.calificar(c, n, o)).pack(side="left", padx=5)

    def abrir_archivo(self, entrega):
        ruta = self.gestor.ruta_absoluta_archivo(entrega)
        if not os.path.exists(ruta):
            messagebox.showerror("Archivo", "El archivo no existe en la carpeta de entregas.")
            return
        try:
            if os.name == "nt":
                os.startfile(ruta)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", ruta])
            else:
                subprocess.Popen(["xdg-open", ruta])
        except Exception as e:
            messagebox.showerror("Archivo", str(e))

    def calificar(self, cedula, entry_nota, entry_obs):
        ok, msg = self.gestor.calificar_entrega(self.actividad.get("id"), cedula, entry_nota.get(), entry_obs.get())
        messagebox.showinfo("Calificacion" if ok else "Error", msg)
        if ok:
            self.cargar()
