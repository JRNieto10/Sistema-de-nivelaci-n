import customtkinter as ctk
from interfaz_personal.creacion_carrera import Crear_carrera
from interfaz_personal.eleccion_carrera import Carrera_seleccionada
from facade import FacadeSistemaAcademico

class Gestionar_carrera(ctk.CTkToplevel):
    def __init__(self, principal):
        super().__init__(principal)
        self.title("Gestion de Carrera")
        self.principal = principal
        self.carrera = None
        self.avanzar = None
        self.geometry("900x500")
        self.sistema = FacadeSistemaAcademico()

        self.carrera_seleccionada = None

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestion de Carreras",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self.frame_principal,
            text="Volver",
            command=self.volver_principal,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150,
            height=40
        )
        self.bton_volver.pack(pady=10)

    def volver_principal(self):
        self.destroy()
        self.principal.deiconify()

    def boton_crear_carrera(self):
        self.bton = ctk.CTkButton(
            self.frame_principal,
            text="Crear Nueva Carrera",
            command=self.crear_carrera,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=200,
            height=40
        )
        self.bton.pack(pady=10)

    def crear_carrera(self):
        if self.carrera is None or not self.carrera.winfo_exists():
            self.carrera = Crear_carrera(self)
        else:
            self.carrera.deiconify()
        self.withdraw()

    def boton_seleccionar_carrera(self):
        frame_seleccion = ctk.CTkFrame(self.frame_principal)
        frame_seleccion.pack(pady=20, fill="x", padx=50)

        ctk.CTkLabel(
            frame_seleccion,
            text="Seleccionar Carrera:",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.combobox_carreras = ctk.CTkComboBox(
            frame_seleccion,
            values=["Cargando..."],
            width=400,
            height=45,
            font=("Arial", 14),
            command=self.on_carrera_seleccionada
        )
        self.combobox_carreras.pack(pady=10)

        ctk.CTkButton(
            frame_seleccion,
            text="Actualizar Lista",
            command=self.actualizar_lista_carreras,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=150,
            height=35
        ).pack(pady=5)

        self.label_info_carrera = ctk.CTkLabel(
            frame_seleccion,
            text="Seleccione una carrera para ver su informacion",
            font=("Arial", 12),
            text_color="#666"
        )
        self.label_info_carrera.pack(pady=10)

        frame_botones = ctk.CTkFrame(frame_seleccion, fg_color="transparent")
        frame_botones.pack(pady=15)

        self.btn_continuar = ctk.CTkButton(
            frame_botones,
            text="CONTINUAR",
            command=self.avanzar_carrera,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=250,
            height=50,
            font=("Arial", 16, "bold"),
            state="disabled"
        )
        self.btn_continuar.pack(side="left", padx=10)

        self.btn_ver_detalles = ctk.CTkButton(
            frame_botones,
            text="Ver Detalles",
            command=self.mostrar_detalles_carrera,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=150,
            height=50,
            font=("Arial", 14),
            state="disabled"
        )
        self.btn_ver_detalles.pack(side="left", padx=10)

        self.actualizar_lista_carreras()

    def actualizar_lista_carreras(self):
        carreras = self.sistema.obtener_todas_carreras()

        if carreras:
            lista_carreras = [f"{c.nombre} (ID: {c.id})" for c in carreras]
            self.combobox_carreras.configure(values=lista_carreras)
            self.combobox_carreras.set("Seleccione una carrera")
        else:
            self.combobox_carreras.configure(values=["No hay carreras registradas"])
            self.combobox_carreras.set("No hay carreras registradas")

        self.carrera_seleccionada = None
        self.btn_continuar.configure(state="disabled")
        self.btn_ver_detalles.configure(state="disabled")
        self.label_info_carrera.configure(
            text="Seleccione una carrera para continuar",
            text_color="#666"
        )

    def on_carrera_seleccionada(self, choice):
        if choice and choice != "No hay carreras registradas" and choice != "Seleccione una carrera":
            try:
                id_inicio = choice.find("ID: ") + 4
                id_fin = choice.find(")", id_inicio)
                id_carrera = choice[id_inicio:id_fin].strip()

                self.carrera_seleccionada = self.sistema.obtener_carrera_por_id(id_carrera)

                if self.carrera_seleccionada:
                    self.btn_continuar.configure(state="normal")
                    self.btn_ver_detalles.configure(state="normal")

                    self.label_info_carrera.configure(
                        text=f"Carrera seleccionada: {self.carrera_seleccionada.nombre}\nArea: {self.carrera_seleccionada.area} | Modalidad: {self.carrera_seleccionada.modalidad}",
                        text_color="#2ecc71"
                    )
                else:
                    self.btn_continuar.configure(state="disabled")
                    self.btn_ver_detalles.configure(state="disabled")
                    self.label_info_carrera.configure(
                        text="Error: No se pudo cargar la carrera",
                        text_color="red"
                    )
            except Exception:
                self.btn_continuar.configure(state="disabled")
                self.btn_ver_detalles.configure(state="disabled")
                self.label_info_carrera.configure(
                    text="Error al seleccionar la carrera",
                    text_color="red"
                )
        else:
            self.carrera_seleccionada = None
            self.btn_continuar.configure(state="disabled")
            self.btn_ver_detalles.configure(state="disabled")
            self.label_info_carrera.configure(
                text="Seleccione una carrera valida",
                text_color="#f39c12"
            )

    def mostrar_detalles_carrera(self):
        if self.carrera_seleccionada:
            info_text = f"""
            DETALLES DE LA CARRERA

            Nombre: {self.carrera_seleccionada.nombre}
            ID: {self.carrera_seleccionada.id}
            Area: {self.carrera_seleccionada.area}
            Modalidad: {self.carrera_seleccionada.modalidad}
            """

            if hasattr(self.carrera_seleccionada, 'asignaturas') and self.carrera_seleccionada.asignaturas:
                info_text += f"\nAsignaturas ({len(self.carrera_seleccionada.asignaturas)}):\n"
                for i, asig in enumerate(self.carrera_seleccionada.asignaturas, 1):
                    if isinstance(asig, dict):
                        info_text += f"  {i}. {asig.get('nombre', 'Sin nombre')} (Codigo: {asig.get('codigo', 'N/A')})\n"
                    else:
                        info_text += f"  {i}. {asig}\n"
            else:
                info_text += "\nNo hay asignaturas registradas aun."

            import tkinter.messagebox as messagebox
            messagebox.showinfo("Detalles de la Carrera", info_text)

    def avanzar_carrera(self):
        if self.carrera_seleccionada:
            if self.avanzar is None or not self.avanzar.winfo_exists():
                self.avanzar = Carrera_seleccionada(self)
                self.avanzar.carrera_actual = self.carrera_seleccionada

                self.avanzar.crear_boton_volver()
                self.avanzar.boton_crear_cursos()
                self.avanzar.boton_crear_asignaturas()
                self.avanzar.boton_gestionar_permitidos()

                self.avanzar.mostrar_info_carrera(self.carrera_seleccionada)
            else:
                self.avanzar.carrera_actual = self.carrera_seleccionada
                self.avanzar.mostrar_info_carrera(self.carrera_seleccionada)
                self.avanzar.deiconify()

            self.withdraw()
        else:
            import tkinter.messagebox as messagebox
            messagebox.showwarning("Advertencia", "Seleccione una carrera primero.")