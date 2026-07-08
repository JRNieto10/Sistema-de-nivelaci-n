import customtkinter as ctk
from interfaz_personal.creacion_cursos2 import Cursos_crear2
from facade import FacadeSistemaAcademico

class Cursos_crear(ctk.CTkToplevel):
    def __init__(self, principal, carrera_actual=None):
        super().__init__(principal)
        self.title("Gestion de Cursos")
        self.principal = principal
        self.carrera_actual = carrera_actual
        self.cursos_ventana2 = None
        self.sistema = FacadeSistemaAcademico()
        self.geometry("1000x750")

        self.asignaciones = []
        self.asignaturas_vars = {}
        self.docentes_vars = {}
        self.asignacion_seleccionada = None

        self.frame_principal = ctk.CTkScrollableFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Creacion de Cursos",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        if self.carrera_actual:
            self.label_carrera = ctk.CTkLabel(
                self.frame_principal,
                text=f"Carrera: {self.carrera_actual.nombre}",
                font=("Arial", 16)
            )
            self.label_carrera.pack(pady=10)

        self.frame_asignaturas = ctk.CTkFrame(self.frame_principal)
        self.frame_asignaturas.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(
            self.frame_asignaturas,
            text="1. Seleccione Asignaturas:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.scroll_asignaturas = ctk.CTkScrollableFrame(self.frame_asignaturas, height=150)
        self.scroll_asignaturas.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_docentes = ctk.CTkFrame(self.frame_principal)
        self.frame_docentes.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(
            self.frame_docentes,
            text="2. Seleccione Docentes (un docente no puede estar en dos materias del mismo curso):",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.scroll_docentes = ctk.CTkScrollableFrame(self.frame_docentes, height=150)
        self.scroll_docentes.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_asignaciones = ctk.CTkFrame(self.frame_principal)
        self.frame_asignaciones.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(
            self.frame_asignaciones,
            text="3. Asignaciones Creadas:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.scroll_asignaciones = ctk.CTkScrollableFrame(self.frame_asignaciones, height=150)
        self.scroll_asignaciones.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_accion = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_accion.pack(pady=10)

        self.btn_agregar = ctk.CTkButton(
            self.frame_accion,
            text="+ Agregar Asignacion",
            command=self.agregar_asignacion,
            width=180,
            height=35
        )
        self.btn_agregar.pack(side="left", padx=10)

        self.btn_eliminar = ctk.CTkButton(
            self.frame_accion,
            text="X Eliminar Seleccionada",
            command=self.eliminar_asignacion,
            width=180,
            height=35
        )
        self.btn_eliminar.pack(side="left", padx=10)

        self.btn_limpiar = ctk.CTkButton(
            self.frame_accion,
            text="Limpiar Todo",
            command=self.limpiar_todo,
            width=180,
            height=35
        )
        self.btn_limpiar.pack(side="left", padx=10)

        self.frame_botones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botones.pack(pady=15)

        self.bton_volver = ctk.CTkButton(
            self.frame_botones,
            text="Volver",
            command=self.volver_principal,
            width=150,
            height=40
        )
        self.bton_volver.pack(side="left", padx=10)

        self.bton_finalizar = ctk.CTkButton(
            self.frame_botones,
            text="Finalizar Curso",
            command=self.finalizar_cursos,
            width=200,
            height=40
        )
        self.bton_finalizar.pack(side="left", padx=10)

        self.label_mensaje = ctk.CTkLabel(
            self.frame_principal,
            text="",
            font=("Arial", 12)
        )
        self.label_mensaje.pack(pady=5)

        self.cargar_asignaturas()
        self.cargar_docentes()
        self.actualizar_lista_asignaciones()

    def cargar_asignaturas(self):
        for widget in self.scroll_asignaturas.winfo_children():
            widget.destroy()

        if self.carrera_actual:
            asignaturas = self.sistema.obtener_asignaturas_carrera(self.carrera_actual.id)
            if not asignaturas:
                ctk.CTkLabel(
                    self.scroll_asignaturas,
                    text="No hay asignaturas registradas",
                    font=("Arial", 12)
                ).pack(pady=10)
                return

            self.asignaturas_vars = {}
            for asignatura in asignaturas:
                if isinstance(asignatura, dict):
                    nombre = asignatura.get('nombre', 'Sin nombre')
                    codigo = asignatura.get('codigo', '')
                    texto = f"{nombre} ({codigo})"
                    var = ctk.BooleanVar(value=False)
                    ctk.CTkCheckBox(
                        self.scroll_asignaturas,
                        text=texto,
                        variable=var,
                        font=("Arial", 12),
                        command=self.validar_seleccion
                    ).pack(anchor="w", padx=10, pady=2)
                    self.asignaturas_vars[nombre] = var

    def cargar_docentes(self):
        for widget in self.scroll_docentes.winfo_children():
            widget.destroy()

        docentes = self.sistema.datos.cargar_docentes_desde_json()

        if not docentes:
            ctk.CTkLabel(
                self.scroll_docentes,
                text="No hay docentes registrados",
                font=("Arial", 12)
            ).pack(pady=10)
            return

        self.docentes_vars = {}
        for docente in docentes:
            nombre = docente.get('nombre', 'Sin nombre')
            apellido = docente.get('apellido', '')
            cedula = docente.get('cedula', '')
            texto = f"{nombre} {apellido} (Cedula: {cedula})"
            var = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(
                self.scroll_docentes,
                text=texto,
                variable=var,
                font=("Arial", 12),
                command=self.validar_seleccion
            ).pack(anchor="w", padx=10, pady=2)
            self.docentes_vars[cedula] = {
                "var": var,
                "datos": docente,
                "nombre": nombre,
                "apellido": apellido
            }

    def validar_seleccion(self):
        docentes_seleccionados = []
        for cedula, info in self.docentes_vars.items():
            if info["var"].get():
                docentes_seleccionados.append(cedula)

        materias_seleccionadas = []
        for nombre, var in self.asignaturas_vars.items():
            if var.get():
                materias_seleccionadas.append(nombre)

        if len(materias_seleccionadas) > 1 and len(docentes_seleccionados) > 1:
            docentes_ocupados = set()
            for asignacion in self.asignaciones:
                docentes_ocupados.add(asignacion["docente"]["cedula"])

            for cedula in docentes_seleccionados:
                if cedula in docentes_ocupados:
                    self.docentes_vars[cedula]["var"].set(False)
                    nombre = self.docentes_vars[cedula]["nombre"]
                    apellido = self.docentes_vars[cedula]["apellido"]
                    self.label_mensaje.configure(
                        text=f"El docente {nombre} {apellido} ya esta asignado a otra materia en este curso",
                        text_color="red"
                    )

    def agregar_asignacion(self):
        materias_seleccionadas = []
        for nombre, var in self.asignaturas_vars.items():
            if var.get():
                materias_seleccionadas.append(nombre)

        docentes_seleccionados = []
        for cedula, info in self.docentes_vars.items():
            if info["var"].get():
                docentes_seleccionados.append(info["datos"])

        if not materias_seleccionadas:
            self.label_mensaje.configure(text="Seleccione al menos una asignatura", text_color="red")
            return

        if not docentes_seleccionados:
            self.label_mensaje.configure(text="Seleccione al menos un docente", text_color="red")
            return

        docentes_asignados = set()
        for asignacion in self.asignaciones:
            docentes_asignados.add(asignacion["docente"]["cedula"])

        docentes_repetidos = []
        for docente in docentes_seleccionados:
            if docente["cedula"] in docentes_asignados:
                docentes_repetidos.append(f"{docente['nombre']} {docente['apellido']}")

        if docentes_repetidos:
            self.label_mensaje.configure(
                text=f"Estos docentes ya estan asignados a otra materia: {', '.join(docentes_repetidos)}",
                text_color="red"
            )
            return

        nuevas_asignaciones = 0
        for materia in materias_seleccionadas:
            for docente in docentes_seleccionados:
                existe = any(
                    a["materia"] == materia and a["docente"]["cedula"] == docente["cedula"]
                    for a in self.asignaciones
                )
                if not existe:
                    self.asignaciones.append({
                        "materia": materia,
                        "docente": docente
                    })
                    nuevas_asignaciones += 1

        if nuevas_asignaciones > 0:
            self.label_mensaje.configure(text=f"Se agregaron {nuevas_asignaciones} asignaciones", text_color="green")
            for var in self.asignaturas_vars.values():
                var.set(False)
            for info in self.docentes_vars.values():
                info["var"].set(False)
            self.actualizar_lista_asignaciones()
        else:
            self.label_mensaje.configure(text="Las combinaciones ya existen", text_color="orange")

    def eliminar_asignacion(self):
        if not hasattr(self, 'asignacion_seleccionada') or self.asignacion_seleccionada is None:
            self.label_mensaje.configure(text="Seleccione una asignacion para eliminar", text_color="red")
            return

        import tkinter.messagebox as messagebox
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"Eliminar asignacion de {self.asignacion_seleccionada['docente']['nombre']} en {self.asignacion_seleccionada['materia']}?"
        )

        if respuesta:
            self.asignaciones.remove(self.asignacion_seleccionada)
            self.asignacion_seleccionada = None
            self.label_mensaje.configure(text="Asignacion eliminada", text_color="green")
            self.actualizar_lista_asignaciones()

    def limpiar_todo(self):
        if not self.asignaciones:
            self.label_mensaje.configure(text="No hay asignaciones para limpiar", text_color="orange")
            return

        import tkinter.messagebox as messagebox
        respuesta = messagebox.askyesno("Confirmar", "Eliminar todas las asignaciones?")

        if respuesta:
            self.asignaciones = []
            self.asignacion_seleccionada = None
            self.label_mensaje.configure(text="Todas las asignaciones eliminadas", text_color="green")
            self.actualizar_lista_asignaciones()

    def actualizar_lista_asignaciones(self):
        for widget in self.scroll_asignaciones.winfo_children():
            widget.destroy()

        if not self.asignaciones:
            ctk.CTkLabel(
                self.scroll_asignaciones,
                text="No hay asignaciones creadas",
                font=("Arial", 12)
            ).pack(pady=20)
            return

        materias_agrupadas = {}
        for asignacion in self.asignaciones:
            materia = asignacion["materia"]
            if materia not in materias_agrupadas:
                materias_agrupadas[materia] = []
            materias_agrupadas[materia].append(asignacion["docente"])

        for materia, docentes in materias_agrupadas.items():
            frame_materia = ctk.CTkFrame(self.scroll_asignaciones)
            frame_materia.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(
                frame_materia,
                text=f"{materia} ({len(docentes)} docentes)",
                font=("Arial", 13, "bold")
            ).pack(anchor="w", padx=10, pady=5)

            for docente in docentes:
                frame_docente = ctk.CTkFrame(frame_materia, fg_color="transparent")
                frame_docente.pack(fill="x", padx=20, pady=2)

                var = ctk.BooleanVar(value=False)
                ctk.CTkRadioButton(
                    frame_docente,
                    text="",
                    variable=var,
                    command=lambda d=docente, m=materia, v=var: self.seleccionar_asignacion(d, m, v)
                ).pack(side="left", padx=5)

                ctk.CTkLabel(
                    frame_docente,
                    text=f"{docente['nombre']} {docente['apellido']} (Cedula: {docente['cedula']})",
                    font=("Arial", 12)
                ).pack(side="left", padx=5)

    def seleccionar_asignacion(self, docente, materia, var):
        if var.get():
            self.asignacion_seleccionada = {
                "materia": materia,
                "docente": docente
            }
            self.label_mensaje.configure(text=f"Seleccionado: {docente['nombre']} en {materia}", text_color="green")
        else:
            self.asignacion_seleccionada = None
            self.label_mensaje.configure(text="")

    def finalizar_cursos(self):
        if not self.asignaciones:
            self.label_mensaje.configure(text="Debe crear al menos una asignacion", text_color="red")
            return

        materias_con_docentes = {}
        for asignacion in self.asignaciones:
            materia = asignacion["materia"]
            if materia not in materias_con_docentes:
                materias_con_docentes[materia] = []
            materias_con_docentes[materia].append(asignacion["docente"])

        curso_nombre = f"Curso_{len(self.sistema.lista_cursos) + 1}"
        carrera_nombre = self.carrera_actual.nombre if self.carrera_actual else "Sin_Carrera"

        self.sistema.datos.guardar_curso(carrera_nombre, curso_nombre, materias_con_docentes)

        self.label_mensaje.configure(text=f"Curso '{curso_nombre}' creado y guardado", text_color="green")

        curso = self.sistema.crear_curso(curso_nombre)
        for materia, docentes in materias_con_docentes.items():
            materia_obj = None
            for m in self.sistema.lista_materias:
                if m.nombre == materia:
                    materia_obj = m
                    break
            if materia_obj:
                self.sistema.agregar_materia_a_curso(curso, materia_obj)
                for docente_data in docentes:
                    docente_obj = None
                    for u in self.sistema.lista_usuarios:
                        if hasattr(u, 'cedula') and u.cedula == docente_data["cedula"] and u.rol == "docente":
                            docente_obj = u
                            break
                    if docente_obj:
                        curso.agregar_docente(docente_obj, materia)

        if self.cursos_ventana2 is None or not self.cursos_ventana2.winfo_exists():
            self.cursos_ventana2 = Cursos_crear2(
                self,
                curso,
                self.carrera_actual,
                curso_nombre,
                materias_con_docentes
            )
        else:
            self.cursos_ventana2.deiconify()

        self.withdraw()

    def volver_principal(self):
        self.destroy()
        if self.principal and self.principal.winfo_exists():
            self.principal.deiconify()