import customtkinter as ctk
from interfaz_personal.crear_asignatura import CrearAsignatura
from facade import FacadeSistemaAcademico

class Asignaturas_crear(ctk.CTkToplevel):
    def __init__(self, principal, carrera_actual=None):
        super().__init__(principal)
        self.title("Gestion de Asignaturas")
        self.principal = principal
        self.carrera_actual = carrera_actual
        self.crear_asignatura_ventana = None
        self.sistema = FacadeSistemaAcademico()
        self.geometry("900x500")

        self.radio_var = ctk.StringVar(value="")

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestion de Asignaturas",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        if self.carrera_actual:
            self.label_carrera = ctk.CTkLabel(
                self.frame_principal,
                text=f"Carrera: {self.carrera_actual.nombre} (ID: {self.carrera_actual.id})",
                font=("Arial", 16)
            )
            self.label_carrera.pack(pady=10)

        self.frame_lista = ctk.CTkFrame(self.frame_principal)
        self.frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_asignaturas = ctk.CTkLabel(
            self.frame_lista,
            text="Asignaturas registradas:",
            font=("Arial", 14, "bold")
        )
        self.label_asignaturas.pack(pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_lista)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_botones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botones.pack(pady=15)

        self.bton_volver = ctk.CTkButton(
            self.frame_botones,
            text="Volver",
            command=self.volver_principal,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150,
            height=40
        )
        self.bton_volver.pack(side="left", padx=10)

        self.bton_crear = ctk.CTkButton(
            self.frame_botones,
            text="+ Crear Asignatura",
            command=self.crear_asignatura,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=200,
            height=40
        )
        self.bton_crear.pack(side="left", padx=10)

        self.bton_eliminar = ctk.CTkButton(
            self.frame_botones,
            text="Eliminar Asignatura",
            command=self.eliminar_asignatura,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=200,
            height=40
        )
        self.bton_eliminar.pack(side="left", padx=10)

        self.cargar_asignaturas()

    def cargar_asignaturas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.carrera_actual:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay carrera seleccionada",
                font=("Arial", 14)
            ).pack(pady=10)
            return

        asignaturas = self.sistema.obtener_asignaturas_carrera(self.carrera_actual.id)

        if not asignaturas:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay asignaturas registradas",
                font=("Arial", 14),
                text_color="#666"
            ).pack(pady=10)
            return

        for i, asignatura in enumerate(asignaturas, 1):
            frame_asignatura = ctk.CTkFrame(self.scrollable_frame)
            frame_asignatura.pack(fill="x", padx=5, pady=5)

            if isinstance(asignatura, dict):
                nombre_asig = asignatura.get('nombre', 'Sin nombre')
                codigo_asig = asignatura.get('codigo', 'N/A')
                creditos_asig = asignatura.get('creditos', 0)
                horas_asig = asignatura.get('horas', 0)
                texto = f"{i}. {nombre_asig} (Codigo: {codigo_asig})"
                texto += f"\n   Creditos: {creditos_asig} | Horas: {horas_asig}"
            else:
                texto = f"{i}. {asignatura}"

            ctk.CTkRadioButton(
                frame_asignatura,
                text="",
                variable=self.radio_var,
                value=str(i)
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                frame_asignatura,
                text=texto,
                font=("Arial", 12),
                justify="left"
            ).pack(side="left", padx=5, fill="x", expand=True)

    def crear_asignatura(self):
        if not self.carrera_actual:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "No hay una carrera seleccionada")
            return

        if self.crear_asignatura_ventana is None or not self.crear_asignatura_ventana.winfo_exists():
            self.crear_asignatura_ventana = CrearAsignatura(self, self.carrera_actual)
        else:
            self.crear_asignatura_ventana.deiconify()

        self.withdraw()

    def eliminar_asignatura(self):
        seleccion = self.radio_var.get()
        if not seleccion:
            import tkinter.messagebox as messagebox
            messagebox.showwarning("Advertencia", "Seleccione una asignatura")
            return

        asignaturas = self.sistema.obtener_asignaturas_carrera(self.carrera_actual.id)

        try:
            index = int(seleccion) - 1
            if 0 <= index < len(asignaturas):
                asignatura = asignaturas[index]
                nombre_asig = asignatura.get('nombre', 'Sin nombre') if isinstance(asignatura, dict) else str(asignatura)

                import tkinter.messagebox as messagebox
                respuesta = messagebox.askyesno(
                    "Confirmar eliminacion",
                    f"Eliminar la asignatura '{nombre_asig}'?"
                )

                if respuesta:
                    asignaturas.pop(index)
                    self.sistema.almacenamiento_carreras.guardar_carrera(self.carrera_actual)
                    self.cargar_asignaturas()
                    self.radio_var.set("")
                    messagebox.showinfo("Exito", "Asignatura eliminada correctamente")
        except (ValueError, IndexError):
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "Error al eliminar la asignatura")

    def volver_principal(self):
        self.radio_var.set("")
        self.destroy()
        if self.principal and self.principal.winfo_exists():
            self.principal.deiconify()

    def actualizar_lista(self):
        self.cargar_asignaturas()