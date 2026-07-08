# vista_principal.py
import customtkinter as ctk

class VentanaPrincipal(ctk.CTk):
    def __init__(self, servicio_autenticacion):
        super().__init__()
        self.auth = servicio_autenticacion
        self.usuario = self.auth.usuario_actual  # Objeto real (Docente/Estudiante/Personal)

        # Configuración de la Ventana
        self.title(f"Sistema de Nivelación - Panel de {self.usuario.rol}")
        self.geometry("850x550")
        self.resizable(False, False)
        
        # --- 1. BARRA LATERAL (SIDEBAR) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.lbl_rol = ctk.CTkLabel(self.sidebar, text=f"Bienvenido,\n{self.usuario.nombre}", font=("Arial", 16, "bold"))
        self.lbl_rol.pack(pady=(30, 20), padx=10)
        
        # --- 2. CONTENEDOR CENTRAL DINÁMICO ---
        self.contenedor_central = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_central.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
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
        lbl.pack(pady=(20, 10))
        
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
            if titulo_seccion == "Mis Cursos":
                ctk.CTkLabel(self.contenedor_central, text="Listado de paralelos y asignaturas bajo su tutoría:", font=("Arial", 14)).pack(pady=10)
                # Aquí se incrustará la lectura de tus JSON de Horarios más adelante

            elif titulo_seccion == "Calificaciones":
                ctk.CTkLabel(self.contenedor_central, text="Panel de Evaluación de Estudiantes", font=("Arial", 14)).pack(pady=10)

        # =====================================================================
        # 👨‍🎓 VISTAS PARA EL ROL: ESTUDIANTE
        # =====================================================================
        elif self.usuario.rol == "Estudiante":
            if titulo_seccion == "Ver Notas":
                ctk.CTkLabel(self.contenedor_central, text="Calificaciones correspondientes al ciclo actual:", font=("Arial", 14)).pack(pady=10)

            elif titulo_seccion == "Mis Horarios":
                ctk.CTkLabel(self.contenedor_central, text="🗓️ Cronograma Semanal de Clases", font=("Arial", 14)).pack(pady=10)

    # --- Métodos de apertura para subventanas del Personal (Admin) ---
    def abrir_formulario_registro(self):
        from vista_registro import VentanaRegistro
        ventana_reg = VentanaRegistro(self.auth)

    def abrir_formulario_modificacion(self):
        from vista_editor_usuario import VentanaEditorUsuario
        # Pasamos 'self' como master y 'self.auth' como servicio
        ventana_edit = VentanaEditorUsuario(self, self.auth)

    def abrir_creador_carreras(self):
        print("[Navegación] Abriendo creador de carreras...")

    def abrir_creador_materias(self):
        print("[Navegación] Abriendo creador de materias...")

    def abrir_creador_carreras(self):
        # Importación local: solo se carga cuando se hace clic en el botón
        from vista_crear_carrera import VentanaCrearCarrera
        VentanaCrearCarrera(self, self.auth)

    def abrir_creador_materias(self):
        from vista_crear_materias import VentanaCrearMateria
        VentanaCrearMateria(self, self.auth)

    def abrir_matricular_docente(self):
        from vista_matricular_docente import VentanaMatricularDocente
        VentanaMatricularDocente(self, self.auth)
        

    def ejecutar_logout(self):
        self.auth.cerrar_sesion()
        self.destroy()
        from vista_login import VentanaLogin
        app_login = VentanaLogin(self.auth)
        app_login.mainloop()


class Vista_Personal:
    def __init__(self, contenedor_central, parent):
        self.contenedor = contenedor_central
        self.parent = parent  # Esto es 'self' de tu VentanaPrincipal (para acceder a los command)

    def renderizar(self, titulo_seccion):
        # Limpiar
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        # Dibujar título
        ctk.CTkLabel(self.contenedor, text=titulo_seccion, font=("Arial", 22, "bold")).pack(pady=(20, 10))

        # Lógica de dibujo (Asegúrate de que estas líneas estén todas al mismo nivel)
        if titulo_seccion == "Gestionar Usuarios":
            self._vista_usuarios()
        elif titulo_seccion == "Crear Carreras":
            self._vista_carreras()
        elif titulo_seccion == "Crear Materias":
            self._vista_materias()
        elif titulo_seccion == "Matricular Docentes": # <--- Debe coincidir letra por letra con el string en usuarios.py
            self._vista_matricular()

    def _vista_usuarios(self):
        ctk.CTkLabel(self.contenedor, text="Gestión interna de cuentas.", font=("Arial", 14)).pack(pady=10)
        ctk.CTkButton(self.contenedor, text="+ Registrar Nuevo Usuario", fg_color="#2ecc71", 
                      command=self.parent.abrir_formulario_registro).pack(pady=10)
        ctk.CTkButton(self.contenedor, text="📝 Modificar Datos", fg_color="#3498db", 
                      command=self.parent.abrir_formulario_modificacion).pack(pady=10)

    def _vista_carreras(self):
        ctk.CTkLabel(self.contenedor, text="Panel para dar de alta nuevas Carreras.", font=("Arial", 14)).pack(pady=10)
        ctk.CTkButton(self.contenedor, text="🔨 Diseñar Nueva Carrera", fg_color="#9b59b6", 
                      command=self.parent.abrir_creador_carreras).pack(pady=15)

    def _vista_materias(self):
        ctk.CTkLabel(self.contenedor, text="Asignación de asignaturas.", font=("Arial", 14)).pack(pady=10)
        ctk.CTkButton(self.contenedor, text="📚 Añadir Materia Externa", fg_color="#f39c12", 
                      command=self.parent.abrir_creador_materias).pack(pady=15)
        
    def _vista_matricular(self):
        ctk.CTkLabel(self.contenedor, text="Asignación de Docentes", font=("Arial", 14)).pack(pady=10)
        ctk.CTkButton(self.contenedor, text="🎓 Matricular Docente", fg_color="#2980b9", 
                      command=self.parent.abrir_matricular_docente).pack(pady=15)