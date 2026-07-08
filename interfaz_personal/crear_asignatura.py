import customtkinter as ctk
from facade import FacadeSistemaAcademico

class CrearAsignatura(ctk.CTkToplevel):
    def __init__(self, principal, carrera_actual):
        super().__init__(principal)
        self.title("Crear Asignatura")
        self.principal = principal
        self.carrera_actual = carrera_actual
        self.sistema = FacadeSistemaAcademico()
        self.geometry("600x550")

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Crear Nueva Asignatura",
            font=("Arial", 20, "bold")
        )
        self.titulo.pack(pady=20)

        if self.carrera_actual:
            self.label_carrera = ctk.CTkLabel(
                self.frame_principal,
                text=f"Carrera: {self.carrera_actual.nombre} (ID: {self.carrera_actual.id})",
                font=("Arial", 14),
                text_color="#3498db"
            )
            self.label_carrera.pack(pady=5)

        self.frame_campos = ctk.CTkFrame(self.frame_principal)
        self.frame_campos.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_campos.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_campos, text="Nombre de la Asignatura:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_nombre = ctk.CTkEntry(self.frame_campos, placeholder_text="Ej: Programacion Avanzada", width=300)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.frame_campos, text="Codigo:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_codigo = ctk.CTkEntry(self.frame_campos, placeholder_text="Ej: PROG-2024", width=300)
        self.entry_codigo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.frame_campos, text="Creditos:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_creditos = ctk.CTkEntry(self.frame_campos, placeholder_text="Ej: 4", width=300)
        self.entry_creditos.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.frame_campos, text="Horas:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_horas = ctk.CTkEntry(self.frame_campos, placeholder_text="Ej: 60", width=300)
        self.entry_horas.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.frame_campos, text="Modalidad:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.combobox_modalidad = ctk.CTkComboBox(
            self.frame_campos,
            values=["Presencial", "Virtual", "Mixta"],
            width=300
        )
        self.combobox_modalidad.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.combobox_modalidad.set("Seleccione modalidad")

        self.label_mensaje = ctk.CTkLabel(
            self.frame_principal,
            text="",
            font=("Arial", 12)
        )
        self.label_mensaje.pack(pady=10)

        self.frame_botones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botones.pack(pady=15)

        self.btn_guardar = ctk.CTkButton(
            self.frame_botones,
            text="Guardar Asignatura",
            command=self.guardar_asignatura,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botones,
            text="Cancelar",
            command=self.cancelar,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150,
            height=40
        )
        self.btn_cancelar.pack(side="left", padx=10)

    def guardar_asignatura(self):
        nombre = self.entry_nombre.get().strip()
        codigo = self.entry_codigo.get().strip()
        creditos = self.entry_creditos.get().strip()
        horas = self.entry_horas.get().strip()
        modalidad = self.combobox_modalidad.get()

        if not all([nombre, codigo, creditos, horas]):
            self.label_mensaje.configure(text="Todos los campos son obligatorios", text_color="red")
            return

        if modalidad == "Seleccione modalidad":
            self.label_mensaje.configure(text="Seleccione una modalidad", text_color="red")
            return

        try:
            creditos = int(creditos)
            horas = int(horas)
        except ValueError:
            self.label_mensaje.configure(text="Creditos y Horas deben ser numeros", text_color="red")
            return

        self.sistema.crear_asignatura(nombre, codigo, creditos, horas, modalidad)

        if self.carrera_actual:
            asignatura_dict = {
                "nombre": nombre,
                "codigo": codigo,
                "creditos": creditos,
                "horas": horas,
                "modalidad": modalidad
            }

            resultado = self.sistema.agregar_asignatura_a_carrera(
                self.carrera_actual.id,
                asignatura_dict
            )

            if resultado:
                self.label_mensaje.configure(text=f"Asignatura '{nombre}' creada exitosamente", text_color="green")
                self.entry_nombre.delete(0, 'end')
                self.entry_codigo.delete(0, 'end')
                self.entry_creditos.delete(0, 'end')
                self.entry_horas.delete(0, 'end')
                self.combobox_modalidad.set("Seleccione modalidad")

                import tkinter.messagebox as messagebox
                messagebox.showinfo("Exito", f"Asignatura '{nombre}' creada exitosamente")

                if self.principal and self.principal.winfo_exists():
                    if hasattr(self.principal, 'actualizar_lista'):
                        self.principal.actualizar_lista()
            else:
                self.label_mensaje.configure(text="Error al guardar la asignatura", text_color="red")
        else:
            self.label_mensaje.configure(text="No hay carrera seleccionada", text_color="red")

    def cancelar(self):
        self.destroy()
        if self.principal and self.principal.winfo_exists():
            self.principal.deiconify()