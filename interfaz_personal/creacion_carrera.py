import customtkinter as ctk
from tkinter import messagebox
from facade import FacadeSistemaAcademico

class Crear_carrera(ctk.CTkToplevel):
    def __init__(self, inicio):
        super().__init__(inicio)
        self.title("Creacion de Carrera")
        self.inicio = inicio
        self.geometry("600x500")
        self.sistema = FacadeSistemaAcademico()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self._crear_widgets()

    def _crear_widgets(self):
        ctk.CTkLabel(
            self,
            text="Registro de Nueva Carrera",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        ctk.CTkLabel(self, text="ID de la Carrera:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_id = ctk.CTkEntry(self, placeholder_text="Ej: INF-2024")
        self.entry_id.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Nombre de la Carrera:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Ej: Ingenieria en Sistemas")
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Area de Conocimiento:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_area = ctk.CTkEntry(self, placeholder_text="Ej: Tecnologia")
        self.entry_area.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Modalidad:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.entry_modalidad = ctk.CTkEntry(self, placeholder_text="Ej: Presencial / Virtual")
        self.entry_modalidad.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.grid(row=5, column=0, columnspan=2, pady=30)

        self.btn_crear = ctk.CTkButton(
            frame_botones,
            text="Crear Carrera",
            command=self.crear_carrera,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=150,
            height=40
        )
        self.btn_crear.pack(side="left", padx=10)

        self.btn_volver = ctk.CTkButton(
            frame_botones,
            text="Volver",
            command=self.volver_inicio,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150,
            height=40
        )
        self.btn_volver.pack(side="left", padx=10)

        self.label_mensaje = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12)
        )
        self.label_mensaje.grid(row=6, column=0, columnspan=2, pady=10)

        self.btn_ver_carreras = ctk.CTkButton(
            self,
            text="Ver Carreras Existentes",
            command=self.ver_carreras,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=200
        )
        self.btn_ver_carreras.grid(row=7, column=0, columnspan=2, pady=10)

    def crear_carrera(self):
        id_carrera = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        area = self.entry_area.get().strip()
        modalidad = self.entry_modalidad.get().strip()

        if not all([id_carrera, nombre, area, modalidad]):
            self.label_mensaje.configure(text="Todos los campos son obligatorios", text_color="red")
            return

        carrera, mensaje = self.sistema.crear_carrera(id_carrera, area, nombre, modalidad)

        if carrera:
            self.label_mensaje.configure(text=f"{mensaje}", text_color="green")
            self.entry_id.delete(0, 'end')
            self.entry_nombre.delete(0, 'end')
            self.entry_area.delete(0, 'end')
            self.entry_modalidad.delete(0, 'end')
            messagebox.showinfo("Exito", f"Carrera '{nombre}' creada exitosamente")
        else:
            self.label_mensaje.configure(text=f"{mensaje}", text_color="red")
            messagebox.showerror("Error", mensaje)

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()

    def ver_carreras(self):
        carreras = self.sistema.obtener_todas_carreras()

        if not carreras:
            messagebox.showinfo("Carreras", "No hay carreras registradas aun.")
            return

        texto = "CARRERAS REGISTRADAS:\n\n"
        for i, carrera in enumerate(carreras, 1):
            texto += f"{i}. {carrera.nombre} (ID: {carrera.id})\n"
            texto += f"   Area: {carrera.area} | Modalidad: {carrera.modalidad}\n"
            if hasattr(carrera, 'asignaturas') and carrera.asignaturas:
                texto += f"   Asignaturas: {len(carrera.asignaturas)}\n"
            texto += "\n"

        messagebox.showinfo("Carreras Registradas", texto)