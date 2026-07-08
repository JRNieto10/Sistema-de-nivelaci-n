import customtkinter as ctk
from facade import FacadeSistemaAcademico
import tkinter.messagebox as messagebox

class Permitidos_gestionar(ctk.CTkToplevel):
    def __init__(self, principal, carrera_actual=None):
        super().__init__(principal)
        self.title("Gestion de Cedulas Permitidas")
        self.principal = principal
        self.carrera_actual = carrera_actual
        self.sistema = FacadeSistemaAcademico()
        self.geometry("900x600")

        self.cedula_seleccionada = None
        self.tipo_seleccionado = None

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestion de Cedulas Permitidas",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        if self.carrera_actual:
            self.label_carrera = ctk.CTkLabel(
                self.frame_principal,
                text=f"Carrera: {self.carrera_actual.nombre} (ID: {self.carrera_actual.id})",
                font=("Arial", 16),
                text_color="#3498db"
            )
            self.label_carrera.pack(pady=10)

        self.frame_agregar = ctk.CTkFrame(self.frame_principal)
        self.frame_agregar.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            self.frame_agregar,
            text="Agregar Nueva Cedula Permitida",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        frame_input = ctk.CTkFrame(self.frame_agregar, fg_color="transparent")
        frame_input.pack(pady=10)

        ctk.CTkLabel(frame_input, text="Cedula:").pack(side="left", padx=5)
        self.entry_cedula = ctk.CTkEntry(
            frame_input,
            placeholder_text="Ingrese la cedula",
            width=250,
            height=35
        )
        self.entry_cedula.pack(side="left", padx=5)

        ctk.CTkLabel(frame_input, text="Rol:").pack(side="left", padx=5)
        self.combobox_rol = ctk.CTkComboBox(
            frame_input,
            values=["Estudiante", "Docente", "Personal"],
            width=150,
            height=35
        )
        self.combobox_rol.pack(side="left", padx=5)
        self.combobox_rol.set("Seleccione rol")

        self.btn_agregar = ctk.CTkButton(
            frame_input,
            text="+ Agregar Cedula",
            command=self.agregar_cedula,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=150,
            height=35
        )
        self.btn_agregar.pack(side="left", padx=10)

        ctk.CTkFrame(self.frame_principal, height=2, fg_color="#ccc").pack(fill="x", padx=10, pady=10)

        self.frame_lista = ctk.CTkFrame(self.frame_principal)
        self.frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_lista = ctk.CTkLabel(
            self.frame_lista,
            text="Cedulas Permitidas Registradas:",
            font=("Arial", 14, "bold")
        )
        self.label_lista.pack(pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_lista)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_botones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botones.pack(pady=15)

        self.btn_eliminar = ctk.CTkButton(
            self.frame_botones,
            text="Eliminar Seleccionada",
            command=self.eliminar_cedula,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=200,
            height=40
        )
        self.btn_eliminar.pack(side="left", padx=10)

        self.btn_volver = ctk.CTkButton(
            self.frame_botones,
            text="Volver",
            command=self.volver_principal,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=150,
            height=40
        )
        self.btn_volver.pack(side="left", padx=10)

        self.label_mensaje = ctk.CTkLabel(
            self.frame_principal,
            text="",
            font=("Arial", 12)
        )
        self.label_mensaje.pack(pady=5)

        self.cargar_cedulas()

    def cargar_cedulas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        datos = self.sistema.datos.listar_cedulas()

        total = len(datos["estudiantes"]) + len(datos["docentes"]) + len(datos["personal"])

        if total == 0:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay cedulas permitidas registradas",
                font=("Arial", 14),
                text_color="#666"
            ).pack(pady=20)
            return

        contador = 0

        if datos["estudiantes"]:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="Estudiantes:",
                font=("Arial", 14, "bold"),
                text_color="#3498db"
            ).pack(anchor="w", padx=10, pady=5)

            for cedula in datos["estudiantes"]:
                contador += 1
                self._crear_item_cedula(contador, cedula, "estudiante")

        if datos["docentes"]:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="Docentes:",
                font=("Arial", 14, "bold"),
                text_color="#f39c12"
            ).pack(anchor="w", padx=10, pady=5)

            for cedula in datos["docentes"]:
                contador += 1
                self._crear_item_cedula(contador, cedula, "docente")

        if datos["personal"]:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="Personal Administrativo:",
                font=("Arial", 14, "bold"),
                text_color="#9b59b6"
            ).pack(anchor="w", padx=10, pady=5)

            for cedula in datos["personal"]:
                contador += 1
                self._crear_item_cedula(contador, cedula, "personal")

    def _crear_item_cedula(self, numero, cedula, tipo):
        frame_item = ctk.CTkFrame(self.scrollable_frame)
        frame_item.pack(fill="x", padx=5, pady=3)

        frame_contenido = ctk.CTkFrame(frame_item, fg_color="transparent")
        frame_contenido.pack(fill="x", padx=10, pady=5)

        colores = {
            "estudiante": "#3498db",
            "docente": "#f39c12",
            "personal": "#9b59b6"
        }

        label_info = ctk.CTkLabel(
            frame_contenido,
            text=f"{numero}. Cedula: {cedula} | Rol: {tipo.capitalize()}",
            font=("Arial", 13),
            text_color=colores.get(tipo, "#000000")
        )
        label_info.pack(side="left", padx=10)

        ctk.CTkButton(
            frame_contenido,
            text="Seleccionar",
            command=lambda: self.seleccionar_cedula(cedula, tipo),
            fg_color="#3498db",
            hover_color="#2980b9",
            width=100,
            height=30
        ).pack(side="right", padx=5)

        frame_contenido.bind("<Button-1>", lambda e, c=cedula, t=tipo: self.seleccionar_cedula(c, t))
        label_info.bind("<Button-1>", lambda e, c=cedula, t=tipo: self.seleccionar_cedula(c, t))

    def seleccionar_cedula(self, cedula, tipo):
        self.cedula_seleccionada = cedula
        self.tipo_seleccionado = tipo
        self.label_mensaje.configure(
            text=f"Cedula seleccionada: {cedula} (Rol: {tipo.capitalize()})",
            text_color="#2ecc71"
        )

    def agregar_cedula(self):
        cedula = self.entry_cedula.get().strip()
        rol = self.combobox_rol.get()

        if not cedula:
            self.label_mensaje.configure(text="Ingrese una cedula", text_color="red")
            return

        if rol == "Seleccione rol":
            self.label_mensaje.configure(text="Seleccione un rol", text_color="red")
            return

        if not cedula.isdigit():
            self.label_mensaje.configure(text="La cedula debe contener solo numeros", text_color="red")
            return

        if len(cedula) != 10:
            self.label_mensaje.configure(text="La cedula debe tener 10 digitos", text_color="red")
            return

        rol_dict = {
            "Estudiante": "estudiante",
            "Docente": "docente",
            "Personal": "personal"
        }

        existe = self.sistema.datos.verificar_cedula(cedula)
        if existe:
            self.label_mensaje.configure(
                text=f"La cedula {cedula} ya esta registrada como {existe}",
                text_color="red"
            )
            return

        resultado = self.sistema.datos.agregar_cedula_permitida(cedula, rol_dict[rol])

        if resultado:
            self.label_mensaje.configure(text=f"Cedula {cedula} agregada como {rol}", text_color="#2ecc71")
            self.entry_cedula.delete(0, 'end')
            self.combobox_rol.set("Seleccione rol")
            self.cargar_cedulas()
            self.cedula_seleccionada = None
            self.tipo_seleccionado = None
            messagebox.showinfo("Exito", f"Cedula {cedula} agregada exitosamente como {rol}")
        else:
            self.label_mensaje.configure(text="Error al agregar la cedula", text_color="red")

    def eliminar_cedula(self):
        if not self.cedula_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una cedula para eliminar")
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Eliminar la cedula {self.cedula_seleccionada} (Rol: {self.tipo_seleccionado.capitalize()})?"
        )

        if respuesta:
            resultado = self.sistema.datos.eliminar_cedula_permitida(
                self.cedula_seleccionada,
                self.tipo_seleccionado
            )

            if resultado:
                self.label_mensaje.configure(text=f"Cedula {self.cedula_seleccionada} eliminada", text_color="#2ecc71")
                cedula_eliminada = self.cedula_seleccionada
                self.cedula_seleccionada = None
                self.tipo_seleccionado = None
                self.cargar_cedulas()
                messagebox.showinfo("Exito", f"Cedula {cedula_eliminada} eliminada correctamente")
            else:
                self.label_mensaje.configure(text="Error al eliminar la cedula", text_color="red")

    def volver_principal(self):
        self.destroy()
        if self.principal and self.principal.winfo_exists():
            self.principal.deiconify()