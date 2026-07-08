import customtkinter as ctk
from facade import FacadeSistemaAcademico

class Cursos_crear2(ctk.CTkToplevel):
    def __init__(self, principal, curso_actual=None, carrera_actual=None,
                 curso_nombre=None, materias_con_docentes=None):
        super().__init__(principal)
        self.title("Gestion de Paralelos")
        self.principal = principal
        self.curso_actual = curso_actual
        self.carrera_actual = carrera_actual
        self.curso_nombre = curso_nombre
        self.materias_con_docentes = materias_con_docentes
        self.sistema = FacadeSistemaAcademico()
        self.paralelos_generados = []
        self.paralelos_seleccionados = []
        self.geometry("1000x750")

        self.frame_principal = ctk.CTkScrollableFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestion de Paralelos",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        if self.curso_actual:
            self.nombre_curso = self.curso_actual.nombre
        elif self.curso_nombre:
            self.nombre_curso = self.curso_nombre
        else:
            self.nombre_curso = "Curso_sin_nombre"

        if self.carrera_actual:
            self.nombre_carrera = self.carrera_actual.nombre
        else:
            self.nombre_carrera = "Sin_Carrera"

        self.label_curso = ctk.CTkLabel(
            self.frame_principal,
            text=f"Curso: {self.nombre_curso}",
            font=("Arial", 16)
        )
        self.label_curso.pack(pady=5)

        self.label_carrera = ctk.CTkLabel(
            self.frame_principal,
            text=f"Carrera: {self.nombre_carrera}",
            font=("Arial", 14)
        )
        self.label_carrera.pack(pady=5)

        self.cargar_estructura_desde_json()

    def cargar_estructura_desde_json(self):
        try:
            datos = self.sistema.datos.cargar_curso(self.nombre_carrera, self.nombre_curso)

            if datos:
                self.generar_y_mostrar_paralelos(datos)
            elif self.materias_con_docentes:
                self.generar_y_mostrar_paralelos_desde_dict(self.materias_con_docentes)
            elif self.curso_actual and hasattr(self.curso_actual, 'materias'):
                self.generar_y_mostrar_paralelos_desde_curso()
            else:
                ctk.CTkLabel(
                    self.frame_principal,
                    text="No se encontro estructura del curso",
                    font=("Arial", 14)
                ).pack(pady=50)

        except Exception:
            ctk.CTkLabel(
                self.frame_principal,
                text="Error al cargar la estructura del curso",
                font=("Arial", 14)
            ).pack(pady=50)

    def generar_paralelos(self, materias_con_docentes):
        if not materias_con_docentes:
            return []

        nombres_materias = list(materias_con_docentes.keys())
        listas_docentes = []

        for materia in nombres_materias:
            docentes = materias_con_docentes[materia]
            docentes_list = []
            for d in docentes:
                if isinstance(d, dict):
                    docentes_list.append({
                        'cedula': d.get('cedula', ''),
                        'nombre': d.get('nombre', ''),
                        'apellido': d.get('apellido', ''),
                        'datos': d
                    })
                else:
                    docentes_list.append({
                        'cedula': d.cedula if hasattr(d, 'cedula') else str(d),
                        'nombre': d.nombre if hasattr(d, 'nombre') else str(d),
                        'apellido': d.apellido if hasattr(d, 'apellido') else '',
                        'datos': d
                    })
            listas_docentes.append(docentes_list)

        if not listas_docentes:
            return []

        max_docentes = max(len(lista) for lista in listas_docentes)
        paralelos_validos = []

        for i in range(max_docentes):
            paralelo = {}
            docentes_en_paralelo = set()
            valido = True

            for j, materia in enumerate(nombres_materias):
                docentes_list = listas_docentes[j]

                if i < len(docentes_list):
                    docente_info = docentes_list[i]
                    cedula = docente_info['cedula']

                    if cedula in docentes_en_paralelo:
                        valido = False
                        break

                    docentes_en_paralelo.add(cedula)
                    paralelo[materia] = docente_info['datos']
                else:
                    paralelo[materia] = None

            if valido:
                paralelos_validos.append(paralelo)

        return paralelos_validos

    def generar_y_mostrar_paralelos(self, datos):
        if not datos or 'materias' not in datos:
            self.mostrar_error("El JSON no tiene materias definidas")
            return

        materias_data = datos['materias']

        if not materias_data:
            self.mostrar_error("No hay materias en este curso")
            return

        materias_con_docentes = {}
        for materia in materias_data:
            nombre = materia.get('nombre', 'Sin nombre')
            docentes = materia.get('docentes', [])
            materias_con_docentes[nombre] = docentes

        self.generar_y_mostrar_paralelos_desde_dict(materias_con_docentes)

    def generar_y_mostrar_paralelos_desde_dict(self, materias_con_docentes):
        if not materias_con_docentes:
            self.mostrar_error("No hay materias con docentes")
            return

        self.paralelos_generados = self.generar_paralelos(materias_con_docentes)

        if not self.paralelos_generados:
            self.mostrar_error("No se pudieron generar paralelos validos")
            return

        self.mostrar_paralelos_en_interfaz()

    def generar_y_mostrar_paralelos_desde_curso(self):
        if not self.curso_actual or not hasattr(self.curso_actual, 'materias'):
            self.mostrar_error("El curso no tiene materias asignadas")
            return

        materias_con_docentes = {}
        for materia, docentes in self.curso_actual.materias.items():
            if isinstance(docentes, list):
                docentes_dict = []
                for d in docentes:
                    if hasattr(d, 'nombre'):
                        docentes_dict.append({
                            'nombre': d.nombre,
                            'apellido': d.apellido if hasattr(d, 'apellido') else '',
                            'cedula': d.cedula if hasattr(d, 'cedula') else '',
                            'correo': d.correo if hasattr(d, 'correo') else ''
                        })
                    else:
                        docentes_dict.append(d)
                materias_con_docentes[materia] = docentes_dict
            else:
                d = docentes
                if hasattr(d, 'nombre'):
                    materias_con_docentes[materia] = [{
                        'nombre': d.nombre,
                        'apellido': d.apellido if hasattr(d, 'apellido') else '',
                        'cedula': d.cedula if hasattr(d, 'cedula') else '',
                        'correo': d.correo if hasattr(d, 'correo') else ''
                    }]
                else:
                    materias_con_docentes[materia] = [d]

        self.generar_y_mostrar_paralelos_desde_dict(materias_con_docentes)

    def mostrar_paralelos_en_interfaz(self):
        if not self.paralelos_generados:
            self.mostrar_error("No hay paralelos generados")
            return

        frame_info = ctk.CTkFrame(self.frame_principal)
        frame_info.pack(fill="x", padx=10, pady=10)

        total_paralelos = len(self.paralelos_generados)

        ctk.CTkLabel(
            frame_info,
            text=f"Se generaron {total_paralelos} paralelos",
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        if self.paralelos_generados:
            primer_paralelo = self.paralelos_generados[0]
            info_materias = ""
            for materia in primer_paralelo.keys():
                docentes_count = 0
                for p in self.paralelos_generados:
                    if materia in p and p[materia] is not None:
                        docentes_count += 1
                info_materias += f"{materia}: {docentes_count} docentes | "

            ctk.CTkLabel(
                frame_info,
                text=info_materias,
                font=("Arial", 12)
            ).pack(pady=5)

        scroll_paralelos = ctk.CTkScrollableFrame(self.frame_principal, height=400)
        scroll_paralelos.pack(fill="both", expand=True, padx=10, pady=10)

        self.paralelos_seleccionados = []

        for i, paralelo in enumerate(self.paralelos_generados, 1):
            frame_paralelo = ctk.CTkFrame(scroll_paralelos)
            frame_paralelo.pack(fill="x", padx=5, pady=5)

            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(
                frame_paralelo,
                text=f"Paralelo {i}",
                variable=var,
                font=("Arial", 14, "bold")
            ).pack(anchor="w", padx=10, pady=5)

            frame_materias = ctk.CTkFrame(frame_paralelo, fg_color="transparent")
            frame_materias.pack(fill="x", padx=30, pady=5)

            for materia, docente in paralelo.items():
                if docente is None:
                    ctk.CTkLabel(
                        frame_materias,
                        text=f"  {materia}: SIN DOCENTE ASIGNADO",
                        font=("Arial", 12),
                        text_color="red"
                    ).pack(anchor="w", padx=10, pady=2)
                elif isinstance(docente, dict):
                    nombre = docente.get('nombre', 'Sin nombre')
                    apellido = docente.get('apellido', '')
                    cedula = docente.get('cedula', '')
                    ctk.CTkLabel(
                        frame_materias,
                        text=f"  {materia}: {nombre} {apellido} (Cedula: {cedula})",
                        font=("Arial", 12)
                    ).pack(anchor="w", padx=10, pady=2)
                else:
                    nombre = docente.nombre if hasattr(docente, 'nombre') else str(docente)
                    apellido = docente.apellido if hasattr(docente, 'apellido') else ''
                    cedula = docente.cedula if hasattr(docente, 'cedula') else ''
                    ctk.CTkLabel(
                        frame_materias,
                        text=f"  {materia}: {nombre} {apellido} (Cedula: {cedula})",
                        font=("Arial", 12)
                    ).pack(anchor="w", padx=10, pady=2)

            self.paralelos_seleccionados.append({
                "paralelo": paralelo,
                "var": var,
                "nombre": f"Paralelo {i}"
            })

        frame_acciones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        frame_acciones.pack(pady=15)

        ctk.CTkButton(
            frame_acciones,
            text="Crear Todos los Paralelos",
            command=self.crear_todos_paralelos,
            width=200,
            height=40
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_acciones,
            text="Crear Seleccionados",
            command=self.crear_seleccionados,
            width=200,
            height=40
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_acciones,
            text="Editar Asignaciones",
            command=self.editar_asignaciones,
            width=200,
            height=40
        ).pack(side="left", padx=10)

        self.label_mensaje = ctk.CTkLabel(
            self.frame_principal,
            text=f"Total: {len(self.paralelos_generados)} paralelos disponibles",
            font=("Arial", 12)
        )
        self.label_mensaje.pack(pady=5)

    def mostrar_error(self, mensaje):
        ctk.CTkLabel(
            self.frame_principal,
            text=mensaje,
            font=("Arial", 14)
        ).pack(pady=50)

    def crear_todos_paralelos(self):
        if hasattr(self, 'paralelos_seleccionados') and self.paralelos_seleccionados:
            for paralelo in self.paralelos_seleccionados:
                paralelo["var"].set(True)
            self.guardar_paralelos()
            self.label_mensaje.configure(text=f"{len(self.paralelos_seleccionados)} paralelos creados", text_color="green")

    def crear_seleccionados(self):
        if not hasattr(self, 'paralelos_seleccionados') or not self.paralelos_seleccionados:
            self.label_mensaje.configure(text="No hay paralelos disponibles", text_color="red")
            return

        seleccionados = [p for p in self.paralelos_seleccionados if p["var"].get()]

        if not seleccionados:
            self.label_mensaje.configure(text="No ha seleccionado ningun paralelo", text_color="red")
            return

        self.guardar_paralelos(seleccionados)
        self.label_mensaje.configure(text=f"{len(seleccionados)} paralelos creados", text_color="green")

    def guardar_paralelos(self, paralelos=None):
        if paralelos is None:
            paralelos = [p for p in self.paralelos_seleccionados if p["var"].get()]

        if not paralelos:
            import tkinter.messagebox as messagebox
            messagebox.showwarning("Advertencia", "No hay paralelos seleccionados")
            return

        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
        paralelos_data = []

        for i, paralelo_info in enumerate(paralelos):
            letra = letras[i % len(letras)]
            paralelo = paralelo_info["paralelo"]

            materias_paralelo = []
            for materia_nombre, docente in paralelo.items():
                if docente is None:
                    materias_paralelo.append({
                        "nombre": materia_nombre,
                        "docente": None,
                        "aula": f"Lab-{101 + i}"
                    })
                elif isinstance(docente, dict):
                    materias_paralelo.append({
                        "nombre": materia_nombre,
                        "docente": {
                            "nombre": docente.get('nombre', ''),
                            "apellido": docente.get('apellido', ''),
                            "cedula": docente.get('cedula', ''),
                            "correo": docente.get('correo', '')
                        },
                        "aula": f"Lab-{101 + i}"
                    })
                else:
                    materias_paralelo.append({
                        "nombre": materia_nombre,
                        "docente": {
                            "nombre": docente.nombre if hasattr(docente, 'nombre') else str(docente),
                            "apellido": docente.apellido if hasattr(docente, 'apellido') else '',
                            "cedula": docente.cedula if hasattr(docente, 'cedula') else '',
                            "correo": docente.correo if hasattr(docente, 'correo') else ''
                        },
                        "aula": f"Lab-{101 + i}"
                    })

            paralelo_data = {
                "letra": letra,
                "aula": f"Aula-{101 + i}",
                "horario": "Matutino" if i % 2 == 0 else "Vespertino",
                "materias": materias_paralelo
            }
            paralelos_data.append(paralelo_data)

        archivo = self.sistema.datos.guardar_paralelos(
            self.nombre_carrera,
            self.nombre_curso,
            paralelos_data
        )

        import tkinter.messagebox as messagebox
        messagebox.showinfo(
            "Exito",
            f"Se han creado {len(paralelos_data)} paralelos\nGuardado en: {archivo}"
        )

    def editar_asignaciones(self):
        self.destroy()
        if self.principal and self.principal.winfo_exists():
            self.principal.deiconify()