# Aqui se implementa la Vista (MVC)
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from estructura.Almacenamiento_actividades import Almacenamiento_Actividades


class VentanaActividadesEstudiante(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.gestor = Almacenamiento_Actividades()
        self.title("Mis actividades")
        self.geometry("760x610")
        self.grab_set()
        ctk.CTkLabel(self, text="Actividades pendientes y calificadas", font=("Arial", 18, "bold")).pack(pady=12)
        self.frame = ctk.CTkScrollableFrame(self, width=700, height=520)
        self.frame.pack(padx=15, pady=8, fill="both", expand=True)
        self.cargar()

    def cargar(self):
        for w in self.frame.winfo_children():
            w.destroy()
        actividades = self.gestor.listar_actividades_estudiante(self.auth.usuario_actual.cedula)
        if not actividades:
            ctk.CTkLabel(self.frame, text="No hay actividades asignadas.", text_color="gray").pack(anchor="w")
            return
        for a in actividades:
            entrega = a.get("entrega") or {}
            nota = entrega.get("nota")
            estado = "Calificada" if nota is not None else ("Entregada" if entrega else "Pendiente")
            texto = f"{a.get('materia')} | {a.get('nombre')} | {a.get('segmento')}\nPlazo: {a.get('fecha_limite')} | Cierre: {a.get('fecha_cierre')} | {estado}"
            fila = ctk.CTkFrame(self.frame)
            fila.pack(fill="x", pady=6)
            ctk.CTkLabel(fila, text=texto, justify="left", wraplength=540).pack(side="left", padx=10, pady=8)
            ctk.CTkButton(fila, text="Abrir", width=90, command=lambda act=a: self.abrir(act)).pack(side="right", padx=10)

    def abrir(self, actividad):
        DetalleActividadEstudiante(self, self.auth, actividad, self.cargar)


class DetalleActividadEstudiante(ctk.CTkToplevel):
    def __init__(self, master, auth, actividad, refrescar):
        super().__init__(master)
        self.auth = auth
        self.actividad = actividad
        self.refrescar = refrescar
        self.gestor = Almacenamiento_Actividades()
        self.title(actividad.get("nombre", "Actividad"))
        self.geometry("560x500")
        self.grab_set()
        entrega = actividad.get("entrega") or {}
        ctk.CTkLabel(self, text=actividad.get("nombre"), font=("Arial", 17, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self, text=f"Materia: {actividad.get('materia')} | Segmento: {actividad.get('segmento')}", wraplength=500).pack(pady=3)
        ctk.CTkLabel(self, text=actividad.get("descripcion") or "Sin descripcion", wraplength=500, justify="left").pack(pady=8)
        ctk.CTkLabel(self, text=f"Entrega puntual hasta: {actividad.get('fecha_limite')}\nCierre definitivo: {actividad.get('fecha_cierre')}\nEstado actual: {self.gestor.estado_plazo(actividad)}", justify="left").pack(pady=8)
        if entrega:
            ctk.CTkLabel(self, text=f"Archivo: {entrega.get('nombre_original')}\nEntregado: {entrega.get('fecha_entrega')} ({entrega.get('estado_entrega')})", justify="left").pack(pady=8)
        nota = entrega.get("nota") if entrega else None
        ctk.CTkLabel(self, text=f"Nota: {nota if nota is not None else 'Pendiente de calificar'}", font=("Arial", 14, "bold")).pack(pady=8)
        if entrega.get("observacion"):
            ctk.CTkLabel(self, text=f"Observacion: {entrega.get('observacion')}", wraplength=500).pack(pady=4)
        self.lbl = ctk.CTkLabel(self, text="", wraplength=500)
        self.lbl.pack(pady=6)
        ctk.CTkButton(self, text="Subir o reemplazar documento", command=self.subir, fg_color="#2980b9").pack(pady=10)

    def subir(self):
        ruta = filedialog.askopenfilename(title="Seleccionar trabajo")
        if not ruta:
            return
        ok, msg = self.gestor.subir_entrega(self.actividad.get("id"), self.auth.usuario_actual.cedula, ruta)
        self.lbl.configure(text_color="green" if ok else "red", text=msg)
        if ok:
            self.refrescar()
            self.after(900, self.destroy)
