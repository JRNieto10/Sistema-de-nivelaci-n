import customtkinter as ctk
from interfaz_personal.creacion_asignaturas import Asignaturas_crear
from interfaz_personal.gestionar_permitidos import Permitidos_gestionar
from interfaz_personal.creacion_cursos import Cursos_crear
from facade import FacadeSistemaAcademico

class Carrera_seleccionada(ctk.CTkToplevel):
    def __init__(self, principal):
        super().__init__(principal)
        self.title("Carrera Seleccionada")
        self.principal = principal
        self.carrera_actual = None
        self.asignaturas_ventana = None
        self.permitidos_ventana = None
        self.cursos_ventana = None
        self.sistema = FacadeSistemaAcademico()
        self.geometry("900x500")

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Informacion de la Carrera",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        self.label_info = ctk.CTkLabel(
            self.frame_principal,
            text="",
            font=("Arial", 14),
            justify="left"
        )
        self.label_info.pack(pady=20)

        self.frame_botones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botones.pack(pady=10)

    def mostrar_info_carrera(self, carrera):
        if carrera:
            info_text = f"""
            CARRERA SELECCIONADA

            Nombre: {carrera.nombre}
            ID: {carrera.id}
            Area: {carrera.area}
            Modalidad: {carrera.modalidad}

            Asignaturas: {len(carrera.asignaturas) if hasattr(carrera, 'asignaturas') else 0}
            """

            if hasattr(carrera, 'asignaturas') and carrera.asignaturas:
                info_text += "\nAsignaturas registradas:\n"
                for i, asig in enumerate(carrera.asignaturas, 1):
                    if isinstance(asig, dict):
                        info_text += f"  {i}. {asig.get('nombre', 'Sin nombre')}\n"
                    else:
                        info_text += f"  {i}. {asig}\n"

            self.label_info.configure(text=info_text)

    def crear_boton_volver(self):
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

    def volver_principal(self):
        self.destroy()
        if self.principal and self.principal.winfo_exists():
            self.principal.deiconify()

    def boton_crear_cursos(self):
        self.bton_cursos = ctk.CTkButton(
            self.frame_botones,
            text="Gestionar Cursos",
            command=self.gestionar_cursos,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=200,
            height=40
        )
        self.bton_cursos.pack(side="left", padx=10)

    def gestionar_cursos(self):
        if not self.carrera_actual:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "No hay una carrera seleccionada")
            return

        asignaturas = self.sistema.obtener_asignaturas_carrera(self.carrera_actual.id)

        if not asignaturas:
            import tkinter.messagebox as messagebox
            messagebox.showwarning(
                "Advertencia",
                "Esta carrera no tiene asignaturas registradas.\nPrimero debe crear asignaturas para poder crear cursos."
            )
            return

        docentes = self.sistema.datos.cargar_docentes_desde_json()

        if not docentes:
            import tkinter.messagebox as messagebox
            messagebox.showwarning(
                "Advertencia",
                "No hay docentes registrados en el sistema.\nPrimero debe registrar docentes para poder crear cursos."
            )
            return

        if self.cursos_ventana is None or not self.cursos_ventana.winfo_exists():
            self.cursos_ventana = Cursos_crear(self, self.carrera_actual)
        else:
            self.cursos_ventana.deiconify()
            if hasattr(self.cursos_ventana, 'cargar_asignaturas'):
                self.cursos_ventana.cargar_asignaturas()
                self.cursos_ventana.cargar_docentes()

        self.withdraw()

    def boton_crear_asignaturas(self):
        self.bton_asignaturas = ctk.CTkButton(
            self.frame_botones,
            text="Gestionar Asignaturas",
            command=self.gestionar_asignaturas,
            fg_color="#f39c12",
            hover_color="#e67e22",
            width=200,
            height=40
        )
        self.bton_asignaturas.pack(side="left", padx=10)

    def gestionar_asignaturas(self):
        if not self.carrera_actual:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "No hay una carrera seleccionada")
            return

        if self.asignaturas_ventana is None or not self.asignaturas_ventana.winfo_exists():
            self.asignaturas_ventana = Asignaturas_crear(self, self.carrera_actual)
        else:
            self.asignaturas_ventana.deiconify()
            if hasattr(self.asignaturas_ventana, 'cargar_asignaturas'):
                self.asignaturas_ventana.cargar_asignaturas()

        self.withdraw()

    def boton_gestionar_permitidos(self):
        self.bton_permitidos = ctk.CTkButton(
            self.frame_botones,
            text="Gestionar Permitidos",
            command=self.gestionar_permitidos,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            width=200,
            height=40
        )
        self.bton_permitidos.pack(side="left", padx=10)

    def gestionar_permitidos(self):
        if not self.carrera_actual:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "No hay una carrera seleccionada")
            return

        if self.permitidos_ventana is None or not self.permitidos_ventana.winfo_exists():
            self.permitidos_ventana = Permitidos_gestionar(self, self.carrera_actual)
        else:
            self.permitidos_ventana.deiconify()
            if hasattr(self.permitidos_ventana, 'cargar_cedulas'):
                self.permitidos_ventana.cargar_cedulas()

        self.withdraw()