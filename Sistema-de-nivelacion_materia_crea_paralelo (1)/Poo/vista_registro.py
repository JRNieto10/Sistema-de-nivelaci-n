# Aqui se implementa la Vista (MVC)
# vista_registro.py
import customtkinter as ctk
from estructura.usuarios import Docente, Estudiante, Personal

class VentanaRegistro(ctk.CTkToplevel): # 💡 Cambiado a CTkToplevel para que sea una ventana emergente/hija
    def __init__(self, servicio_autenticacion):
        super().__init__()
        self.auth = servicio_autenticacion
        self.almacenamiento = servicio_autenticacion.almacenamiento

        self.title("Administrador - Crear Usuario")
        self.geometry("450x640")
        self.resizable(False, False)
        
        # Esto hace que la ventana de registro se quede al frente obligatoriamente
        self.transient(self.master)
        self.grab_set()

        self.frame = ctk.CTkFrame(self, width=380, height=580, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_titulo = ctk.CTkLabel(self.frame, text="Crear Usuario", font=("Arial", 22, "bold"))
        self.lbl_titulo.pack(pady=(20, 15))

        self.entry_cedula = ctk.CTkEntry(self.frame, placeholder_text="Número de Cédula", width=280, height=35)
        self.entry_cedula.pack(pady=6)

        self.entry_nombre = ctk.CTkEntry(self.frame, placeholder_text="Nombres", width=280, height=35)
        self.entry_nombre.pack(pady=6)

        self.entry_apellido = ctk.CTkEntry(self.frame, placeholder_text="Apellidos", width=280, height=35)
        self.entry_apellido.pack(pady=6)

        self.entry_correo = ctk.CTkEntry(self.frame, placeholder_text="Correo Electrónico", width=280, height=35)
        self.entry_correo.pack(pady=6)

        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Contraseña Temporal", show="*", width=280, height=35)
        self.entry_password.pack(pady=6)

        self.lbl_rol = ctk.CTkLabel(self.frame, text="Asignar Rol:", font=("Arial", 12), text_color="gray")
        self.lbl_rol.pack(pady=(5, 2))
        self.option_rol = ctk.CTkOptionMenu(self.frame, values=["Estudiante", "Docente", "Personal"], width=280, height=35)
        self.option_rol.pack(pady=5)

        self.btn_registrar = ctk.CTkButton(self.frame, text="Crear Usuario", command=self.ejecutar_registro, width=280, height=40, font=("Arial", 14, "bold"), fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_registrar.pack(pady=15)

        self.btn_cerrar = ctk.CTkButton(self.frame, text="Cancelar", command=self.destroy, width=280, height=30, fg_color="transparent", border_width=1, text_color="white")
        self.btn_cerrar.pack(pady=5)

        self.lbl_mensaje = ctk.CTkLabel(self.frame, text="", text_color="red", font=("Arial", 13))
        self.lbl_mensaje.pack(pady=5)

    # vista_registro.py

    def ejecutar_registro(self):
        # ... (asegúrate de obtener la variable cedula correctamente)
        cedula = self.entry_cedula.get().strip().replace(" ", "")
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        correo = self.entry_correo.get().strip().lower()
        contrasena = self.entry_password.get()
        rol = self.option_rol.get()

        if not all([cedula, nombre, apellido, correo, contrasena]):
            self.lbl_mensaje.configure(text_color="red", text="Todos los campos son obligatorios.")
            return

        if not (cedula.isdigit() and len(cedula) == 10):
            self.lbl_mensaje.configure(text_color="red", text="La cédula debe tener exactamente 10 dígitos.")
            return

        # Esta ventana es exclusiva del administrador.
        # Por eso el administrador puede crear usuarios de cualquiera de los tres roles
        # sin depender de la importación previa de cédulas.
        if not self.auth.usuario_actual or self.auth.usuario_actual.rol != "Personal":
            self.lbl_mensaje.configure(text_color="red", text="Solo el administrador puede crear usuarios.")
            return

        # Pasamos la cédula a los constructores.
        if rol == "Docente":
            nuevo_usuario = Docente(nombre, apellido, correo, contrasena, rol, cedula)
        elif rol == "Estudiante":
            nuevo_usuario = Estudiante(nombre, apellido, correo, contrasena, rol, cedula)
        elif rol == "Personal":
            nuevo_usuario = Personal(nombre, apellido, correo, contrasena, rol, cedula)

        # Ahora el objeto tendrá la cédula y guardará correctamente
        exito = self.almacenamiento.guardar_usuario_objeto(nuevo_usuario)
        # ...

        if exito:
            self.lbl_mensaje.configure(text_color="green", text="¡Usuario creado correctamente!")
            self.update()
            self.after(1500, self.destroy)
        else:
            self.lbl_mensaje.configure(text_color="red", text="Error: El correo ya existe.")