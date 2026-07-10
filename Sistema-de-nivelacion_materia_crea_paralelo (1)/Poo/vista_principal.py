# Aqui se implementa la Vista (MVC)
# vista_principal.py
import customtkinter as ctk

class VentanaPrincipal(ctk.CTk):
    def __init__(self, servicio_autenticacion):
        super().__init__()
        self.auth = servicio_autenticacion
        self.usuario = self.auth.usuario_actual  # Objeto real (Docente/Estudiante/Personal)

        # Configuración de la Ventana
        self.title(f"Sistema de Nivelación - Panel de {self.usuario.rol}")
        self.geometry("900x580")
        self.resizable(False, False)

        # --- 1. BARRA LATERAL (SIDEBAR) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.lbl_rol = ctk.CTkLabel(self.sidebar, text=f"Bienvenido,\n{self.usuario.nombre}", font=("Arial", 16, "bold"))
        self.lbl_rol.pack(pady=(30, 20), padx=10)

        # --- 2. CONTENEDOR CENTRAL DINÁMICO (con scroll para paneles largos) ---
        self.contenedor_central = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.contenedor_central.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Aqui se hizo Polimorfismo
        # --- 3. CONSTRUCCIÓN AUTOMÁTICA DEL MENÚ (POLIMORFISMO) ---
        for opcion in self.usuario.opciones_menu:
            btn = ctk.CTkButton(
                self.sidebar,
                text=opcion,
                command=lambda opt=opcion: self.cargar_vista(opt)
            )
            btn.pack(pady=10, padx=15, fill="x")

        # Botón Universal de Cerrar Sesión al fondo
        btn_logout = ctk.CTkButton(self.sidebar, text="Cerrar Sesión", fg_color="#e74c3c", hover_color="#c0392b", command=self.ejecutar_logout)
        btn_logout.pack(side="bottom", pady=20, padx=15, fill="x")

        # Cargar la primera opción disponible por defecto en pantalla
        self.cargar_vista(self.usuario.opciones_menu[0])

    def cargar_vista(self, titulo_seccion):
        """Limpia el contenedor de la derecha y dibuja el nuevo contenido según el rol"""
        for widget in self.contenedor_central.winfo_children():
            widget.destroy()

        lbl = ctk.CTkLabel(self.contenedor_central, text=titulo_seccion, font=("Arial", 22, "bold"))
        lbl.pack(pady=(10, 15), anchor="w")

        # =====================================================================
        # 🛠️ VISTAS PARA EL ROL: PERSONAL (ADMIN)
        # =====================================================================
        if self.usuario.rol == "Personal":
            vista = Vista_Personal(self.contenedor_central, self)
            vista.renderizar(titulo_seccion)

        # =====================================================================
        # 👨‍🏫 VISTAS PARA EL ROL: DOCENTE
        # =====================================================================
        elif self.usuario.rol == "Docente":
            vista = Vista_Docente(self.contenedor_central, self)
            vista.renderizar(titulo_seccion)

        # =====================================================================
        # 👨‍🎓 VISTAS PARA EL ROL: ESTUDIANTE
        # =====================================================================
        elif self.usuario.rol == "Estudiante":
            vista = Vista_Estudiante(self.contenedor_central, self)
            vista.renderizar(titulo_seccion)

    # --- Métodos de apertura para subventanas del Personal (Admin) ---
    def abrir_formulario_registro(self):
        from vista_registro import VentanaRegistro
        VentanaRegistro(self.auth)

    def abrir_formulario_modificacion(self):
        from vista_editor_usuario import VentanaEditorUsuario
        VentanaEditorUsuario(self, self.auth)

    def abrir_lista_usuarios(self):
        from vista_lista_usuarios import VentanaListaUsuarios
        VentanaListaUsuarios(self, self.auth)

    def abrir_creador_carreras(self):
        from vista_crear_carrera import VentanaCrearCarrera
        VentanaCrearCarrera(self, self.auth)

    def abrir_creador_materias(self):
        from vista_crear_materias import VentanaCrearMateria
        VentanaCrearMateria(self, self.auth)

    def abrir_matricular_docente(self):
        from vista_matricular_docente import VentanaMatricularDocente
        VentanaMatricularDocente(self, self.auth)

    def abrir_creador_paralelos(self):
        from vista_crear_paralelo import VentanaCrearParalelo
        VentanaCrearParalelo(self, self.auth)

    def abrir_creador_horarios(self):
        from vista_crear_horarios import VentanaCrearHorarios
        VentanaCrearHorarios(self, self.auth)

    def abrir_configurar_evaluaciones(self):
        from vista_configurar_evaluaciones import VentanaConfigurarEvaluaciones
        VentanaConfigurarEvaluaciones(self, self.auth)

    def abrir_importar_usuarios(self):
        from vista_importar_cedulas import VentanaImportarCedulas
        VentanaImportarCedulas(self, self.auth)

    # --- Métodos de apertura para subventanas del Docente ---
    def abrir_calificar(self, paralelo):
        # Esta opcion ahora abre la gestion separada de actividades y calificaciones.
        from vista_gestion_actividades import VentanaGestionActividades
        VentanaGestionActividades(self, self.auth, paralelo)

    def abrir_actividades_estudiante(self):
        from vista_actividades_estudiante import VentanaActividadesEstudiante
        VentanaActividadesEstudiante(self, self.auth)

    def exportar_aprobados(self):
        from tkinter import filedialog, messagebox
        from estructura.Exportador_aprobados import ExportadorAprobados
        ruta = filedialog.asksaveasfilename(title="Guardar estudiantes aprobados", defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if not ruta:
            return
        ok, msg = ExportadorAprobados().generar(ruta)
        (messagebox.showinfo if ok else messagebox.showerror)("Exportacion", msg)

    def abrir_crear_tutoria(self):
        from vista_crear_tutoria import VentanaCrearTutoria
        VentanaCrearTutoria(self, self.auth)

    # --- Métodos de apertura para subventanas del Estudiante ---
    def abrir_matricularse(self):
        from vista_matricularse import VentanaMatricularse
        VentanaMatricularse(self, self.auth)

    def ejecutar_logout(self):
        self.auth.cerrar_sesion()
        self.destroy()
        from vista_login import VentanaLogin
        app_login = VentanaLogin(self.auth)
        app_login.mainloop()


class Vista_Personal:
    def __init__(self, contenedor_central, parent):
        self.contenedor = contenedor_central
        self.parent = parent

    def renderizar(self, titulo_seccion):
        if titulo_seccion == "Gestionar Usuarios":
            self._vista_usuarios()
        elif titulo_seccion == "Crear Carreras":
            self._vista_carreras()
        elif titulo_seccion == "Crear Materias":
            self._vista_materias()
        elif titulo_seccion == "Matricular Docentes":
            self._vista_matricular()
        elif titulo_seccion == "Crear Paralelos":
            self._vista_paralelos()
        elif titulo_seccion == "Crear Horarios":
            self._vista_horarios()
        elif titulo_seccion == "Configurar Evaluaciones":
            self._vista_evaluaciones()
        elif titulo_seccion == "Importar Usuarios":
            self._vista_importar()
        elif titulo_seccion == "Exportar Aprobados":
            self._vista_exportar_aprobados()

    def _vista_usuarios(self):
        ctk.CTkLabel(self.contenedor, text="Desde aquí el administrador crea usuarios Estudiante, Docente o Personal.", font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="+ Crear Usuario", fg_color="#2ecc71",
                      command=self.parent.abrir_formulario_registro).pack(pady=6, anchor="w")
        ctk.CTkButton(self.contenedor, text="📝 Modificar Datos", fg_color="#3498db",
                      command=self.parent.abrir_formulario_modificacion).pack(pady=6, anchor="w")
        ctk.CTkButton(self.contenedor, text="📋 Mostrar Todos los Usuarios", fg_color="#8e44ad",
                      command=self.parent.abrir_lista_usuarios).pack(pady=6, anchor="w")

        from estructura.AlmacenamietoUsuarios import Almacenamiento_Usuarios
        usuarios = Almacenamiento_Usuarios().json.repo.leer_todo()
        ctk.CTkLabel(self.contenedor, text="Usuarios registrados en el sistema:", font=("Arial", 13, "bold")).pack(pady=(18, 6), anchor="w")

        if not usuarios:
            ctk.CTkLabel(self.contenedor, text="No hay usuarios registrados.", text_color="gray").pack(anchor="w")
            return

        for rol in ["Personal", "Docente", "Estudiante"]:
            grupo = [u for u in usuarios if u.get("rol") == rol]
            ctk.CTkLabel(self.contenedor, text=f"{rol}: {len(grupo)}", font=("Arial", 12, "bold")).pack(pady=(8, 2), anchor="w")
            for u in grupo[:12]:
                texto = f"• {u.get('cedula','-')} | {u.get('nombre','')} {u.get('apellido','')} | {u.get('correo','')}"
                ctk.CTkLabel(self.contenedor, text=texto, wraplength=600, justify="left").pack(anchor="w")
            if len(grupo) > 12:
                ctk.CTkLabel(self.contenedor, text=f"  ... y {len(grupo) - 12} más", text_color="gray").pack(anchor="w")

    def _vista_carreras(self):
        ctk.CTkLabel(self.contenedor, text="Panel para dar de alta nuevas Carreras.", font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="🔨 Diseñar Nueva Carrera", fg_color="#9b59b6",
                      command=self.parent.abrir_creador_carreras).pack(pady=15, anchor="w")

        from estructura.Almacenamiento_carreras import Almacenamiento_Carreras
        carreras = Almacenamiento_Carreras().json.repo.leer_todo()
        if carreras:
            ctk.CTkLabel(self.contenedor, text="Carreras registradas:", font=("Arial", 13, "bold")).pack(pady=(10, 0), anchor="w")
            for c in carreras:
                ctk.CTkLabel(self.contenedor, text=f"• {c['nombre']} (ID {c['id']}, {c['duracion']} semestres)").pack(anchor="w")

    def _vista_materias(self):
        ctk.CTkLabel(self.contenedor, text="Crear materia y desde ahí crear su paralelo.", font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="📚 Crear Materia y Paralelo", fg_color="#f39c12",
                      command=self.parent.abrir_creador_materias).pack(pady=15, anchor="w")

    def _vista_matricular(self):
        ctk.CTkLabel(self.contenedor, text="Asignación de Docentes a Materias", font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="🎓 Matricular Docente", fg_color="#2980b9",
                      command=self.parent.abrir_matricular_docente).pack(pady=15, anchor="w")

    def _vista_paralelos(self):
        ctk.CTkLabel(self.contenedor, text="Consultar paralelos creados desde cada materia.",
                     font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="🗓️ Ver Paralelos", fg_color="#16a085",
                      command=self.parent.abrir_creador_paralelos).pack(pady=15, anchor="w")

        from estructura.Almacenamiento_horario import GuardarHorarios
        paralelos = GuardarHorarios().listar_paralelos()
        if paralelos:
            ctk.CTkLabel(self.contenedor, text="Paralelos existentes:", font=("Arial", 13, "bold")).pack(pady=(10, 0), anchor="w")
            for p in paralelos:
                materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
                materias_txt = ", ".join(materias) if materias else "Sin materias"
                texto = f"• {p['nombre']} ({p.get('jornada','')}) - Materias: {materias_txt} - {len(p.get('estudiantes', []))} inscrito(s)"
                ctk.CTkLabel(self.contenedor, text=texto, wraplength=560, justify="left").pack(anchor="w")

    def _vista_horarios(self):
        ctk.CTkLabel(self.contenedor, text="Generar horarios por materia tomando en cuenta la jornada del paralelo.",
                     font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="🗓️ Crear Horarios", fg_color="#16a085",
                      command=self.parent.abrir_creador_horarios).pack(pady=15, anchor="w")

        from estructura.Almacenamiento_horario import GuardarHorarios
        paralelos = GuardarHorarios().listar_paralelos()
        for p in paralelos:
            horarios = p.get("horarios_por_materia", {})
            if horarios:
                ctk.CTkLabel(self.contenedor, text=f"{p.get('nombre')} - {p.get('jornada')}", font=("Arial", 12, "bold")).pack(pady=(8, 2), anchor="w")
                for materia, h in horarios.items():
                    texto = f"• {materia}: {h.get('dia')} {h.get('hora_inicio')}-{h.get('hora_fin')} | {h.get('aula')}"
                    ctk.CTkLabel(self.contenedor, text=texto, wraplength=560, justify="left").pack(anchor="w")

    def _vista_evaluaciones(self):
        ctk.CTkLabel(self.contenedor, text="Configurar cómo se divide la nota final de la nivelación.",
                     font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="⚙️ Configurar Segmentos", fg_color="#34495e",
                      command=self.parent.abrir_configurar_evaluaciones).pack(pady=12, anchor="w")
        from estructura.Almacenamiento_evaluaciones import Almacenamiento_Evaluaciones
        config = Almacenamiento_Evaluaciones().obtener_configuracion()
        ctk.CTkLabel(self.contenedor, text=f"Nota final: {config.get('nota_final', 10)}", font=("Arial", 13, "bold")).pack(pady=(10, 4), anchor="w")
        for seg in config.get("segmentos", []):
            ctk.CTkLabel(self.contenedor, text=f"• {seg.get('nombre')}: {seg.get('porcentaje')}% = {seg.get('valor')} puntos").pack(anchor="w")

    def _vista_importar(self):
        ctk.CTkLabel(self.contenedor, text="Importación masiva de usuarios como usuarios del sistema (CSV / Excel).",
                     font=("Arial", 14)).pack(pady=10, anchor="w")
        ctk.CTkLabel(self.contenedor, text="Sirve para cargar estudiantes completos con correo y contraseña temporal. También puede crear usuarios manualmente desde Gestionar Usuarios.",
                     text_color="gray", wraplength=560, justify="left").pack(pady=(0, 10), anchor="w")
        ctk.CTkButton(self.contenedor, text="📥 Importar Archivo", fg_color="#8e44ad",
                      command=self.parent.abrir_importar_usuarios).pack(pady=15, anchor="w")

    def _vista_exportar_aprobados(self):
        ctk.CTkLabel(self.contenedor, text="Descarga un Excel con estudiantes que tienen minimo 7 en todas las materias de su paralelo.", wraplength=560, justify="left").pack(pady=10, anchor="w")
        ctk.CTkButton(self.contenedor, text="Descargar Excel de aprobados", fg_color="#27ae60", command=self.parent.exportar_aprobados).pack(pady=12, anchor="w")



class Vista_Docente:
    def __init__(self, contenedor_central, parent):
        self.contenedor = contenedor_central
        self.parent = parent
        self.docente = parent.usuario

    def renderizar(self, titulo_seccion):
        if titulo_seccion == "Mis Materias":
            self._vista_materias()
        elif titulo_seccion == "Gestionar Actividades":
            self._vista_calificar()
        elif titulo_seccion == "Tutorías":
            self._vista_tutorias()

    def _vista_materias(self):
        paralelos = self.docente.ver_materias_asignadas()
        if not paralelos:
            ctk.CTkLabel(self.contenedor, text="Aún no tiene paralelos/materias asignadas.", text_color="gray").pack(anchor="w")
            return
        for p in paralelos:
            materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
            asignadas = p.get("docentes_por_materia", {})
            horarios = p.get("horarios_por_materia", {})
            lineas = [f"📘 {p['nombre']} ({p.get('jornada','')})"]
            for materia in materias:
                if asignadas.get(materia) == self.docente.cedula or p.get("docente_cedula") == self.docente.cedula:
                    h = horarios.get(materia) or p.get("horario") or {}
                    lineas.append(f"   • {materia}: {h.get('dia','?')} {h.get('hora_inicio','?')}-{h.get('hora_fin','?')} | Aula: {h.get('aula','-')}")
            lineas.append(f"   Estudiantes inscritos: {len(p.get('estudiantes', []))}")
            ctk.CTkLabel(self.contenedor, text="\n".join(lineas), justify="left", anchor="w").pack(pady=8, anchor="w")

    def _vista_calificar(self):
        paralelos = self.docente.ver_materias_asignadas()
        if not paralelos:
            ctk.CTkLabel(self.contenedor, text="No tiene paralelos asignados todavía.", text_color="gray").pack(anchor="w")
            return
        ctk.CTkLabel(self.contenedor, text="Seleccione un paralelo para crear actividades o calificar entregas:").pack(pady=(0, 10), anchor="w")
        for p in paralelos:
            frame = ctk.CTkFrame(self.contenedor)
            frame.pack(pady=6, fill="x")
            materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
            ctk.CTkLabel(frame, text=f"{p['nombre']} - {', '.join(materias)} ({len(p.get('estudiantes', []))} estudiantes)").pack(side="left", padx=10, pady=8)
            ctk.CTkButton(frame, text="Actividades", width=110,
                          command=lambda par=p: self.parent.abrir_calificar(par)).pack(side="right", padx=10)

    def _vista_tutorias(self):
        ctk.CTkButton(self.contenedor, text="+ Programar Nueva Tutoría", fg_color="#2ecc71",
                      command=self.parent.abrir_crear_tutoria).pack(pady=(0, 15), anchor="w")
        tutorias = self.docente.ver_tutorias()
        if not tutorias:
            ctk.CTkLabel(self.contenedor, text="No ha programado tutorías aún.", text_color="gray").pack(anchor="w")
            return
        for t in tutorias:
            texto = f"📌 {t['tema']} - {t['fecha']} ({t['estado']}) - {len(t.get('estudiantes', []))} inscrito(s) | obligatorios: {len(t.get('obligatorios', []))}"
            ctk.CTkLabel(self.contenedor, text=texto, anchor="w").pack(pady=4, anchor="w")


class Vista_Estudiante:
    def __init__(self, contenedor_central, parent):
        self.contenedor = contenedor_central
        self.parent = parent
        self.estudiante = parent.usuario

    def renderizar(self, titulo_seccion):
        if titulo_seccion == "Ver Notas":
            self._vista_notas()
        elif titulo_seccion == "Actividades":
            self._vista_actividades()
        elif titulo_seccion == "Mis Horarios":
            self._vista_horario()
        elif titulo_seccion == "Matricularme":
            self._vista_matricularme()
        elif titulo_seccion == "Tutorías":
            self._vista_tutorias()

    def _vista_notas(self):
        notas = self.estudiante.ver_notas()
        if not notas:
            ctk.CTkLabel(self.contenedor, text="Aún no tiene calificaciones registradas.", text_color="gray").pack(anchor="w")
            return
        for n in notas:
            color = "#2ecc71" if n.get("aprobado") else "#e74c3c"
            ctk.CTkLabel(self.contenedor, text=f"📘 {n.get('materia')} - Nota final: {n.get('nota_final', 0)} ({'Aprobado' if n.get('aprobado') else 'Reprobado'})",
                         text_color=color, font=("Arial", 13, "bold")).pack(pady=(8, 2), anchor="w")
            resumen = n.get("resumen_segmentos", {})
            for nombre, r in resumen.items():
                ctk.CTkLabel(self.contenedor, text=f"   • {nombre}: promedio {r.get('promedio_10')} / aporte {r.get('aporte')} de {r.get('valor_segmento')}").pack(anchor="w")
            actividades = n.get("actividades", [])
            if actividades:
                ctk.CTkLabel(self.contenedor, text="   Actividades:", text_color="gray").pack(anchor="w")
                for a in actividades:
                    ctk.CTkLabel(self.contenedor, text=f"      - {a.get('segmento')} | {a.get('actividad')}: {a.get('nota')} ({a.get('fecha','')})", wraplength=590).pack(anchor="w")

    def _vista_actividades(self):
        actividades = self.estudiante.ver_actividades()
        pendientes = [a for a in actividades if not a.get("entrega")]
        ctk.CTkLabel(self.contenedor, text=f"Actividades asignadas: {len(actividades)} | Pendientes: {len(pendientes)}", font=("Arial", 13, "bold")).pack(pady=(0, 10), anchor="w")
        ctk.CTkButton(self.contenedor, text="Ver actividades y subir trabajos", fg_color="#2980b9", command=self.parent.abrir_actividades_estudiante).pack(pady=10, anchor="w")

    def _vista_horario(self):
        paralelos = self.estudiante.ver_horario()
        if not paralelos:
            ctk.CTkLabel(self.contenedor, text="No está matriculado en ningún paralelo todavía.", text_color="gray").pack(anchor="w")
            return
        for p in paralelos:
            materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
            horarios = p.get("horarios_por_materia", {})
            for materia in materias:
                h = horarios.get(materia) or p.get("horario") or {}
                texto = f"🗓️ {materia} - {p['nombre']} | {h.get('dia','?')} {h.get('hora_inicio','?')}-{h.get('hora_fin','?')} | Aula: {h.get('aula','-')}"
                ctk.CTkLabel(self.contenedor, text=texto, anchor="w").pack(pady=4, anchor="w")

    def _vista_matricularme(self):
        ctk.CTkLabel(self.contenedor, text="Inscríbase en un paralelo disponible (se valida choque de horarios).",
                     wraplength=560, justify="left").pack(pady=(0, 10), anchor="w")
        ctk.CTkButton(self.contenedor, text="📝 Matricularme", fg_color="#2980b9",
                      command=self.parent.abrir_matricularse).pack(pady=10, anchor="w")

    def _vista_tutorias(self):
        tutorias = self.estudiante.ver_tutorias_disponibles()
        if not tutorias:
            ctk.CTkLabel(self.contenedor, text="No hay tutorías programadas por el momento.", text_color="gray").pack(anchor="w")
            return
        for t in tutorias:
            frame = ctk.CTkFrame(self.contenedor)
            frame.pack(pady=6, fill="x")
            inscrito = self.estudiante.cedula in t.get("estudiantes", [])
            obligatorio = self.estudiante.cedula in t.get("obligatorios", [])
            texto = f"{t['tema']} - {t['fecha']} ({t['estado']})"
            if obligatorio:
                texto += " | Tutoría obligatoria"
            ctk.CTkLabel(frame, text=texto).pack(side="left", padx=10, pady=8)
            if inscrito:
                etiqueta = "Tutoría obligatoria ✔" if obligatorio else "Ya inscrito ✔"
                ctk.CTkLabel(frame, text=etiqueta, text_color="#2ecc71").pack(side="right", padx=10)
            else:
                ctk.CTkButton(frame, text="Inscribirme", width=100,
                              command=lambda tid=t["id"]: self._inscribirse(tid)).pack(side="right", padx=10)

    def _inscribirse(self, id_tutoria):
        self.estudiante.inscribirse_en_tutoria(id_tutoria)
        self.parent.cargar_vista("Tutorías")
