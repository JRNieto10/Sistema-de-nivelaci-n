# Aqui se implementa la Vista (MVC)

# vista_login.py
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VentanaLogin(ctk.CTk):
    def __init__(self, servicio_autenticacion):
        super().__init__()
        self.auth = servicio_autenticacion

        self.title("Sistema de Nivelación - Login")
        # Tamaño ligeramente ajustado al quitar elementos
        self.geometry("450x450") 
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(self, width=360, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # --- Componentes ---
        self.lbl_titulo = ctk.CTkLabel(self.frame, text="Sistema de Nivelación", font=("Arial", 24, "bold"))
        self.lbl_titulo.pack(pady=(40, 10))
        
        self.lbl_subtitulo = ctk.CTkLabel(self.frame, text="Iniciar Sesión", font=("Arial", 16), text_color="gray")
        self.lbl_subtitulo.pack(pady=(0, 30))

        self.entry_correo = ctk.CTkEntry(self.frame, placeholder_text="Correo Electrónico", width=260, height=40)
        self.entry_correo.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Contraseña", show="*", width=260, height=40)
        self.entry_password.pack(pady=10)

        self.btn_ingresar = ctk.CTkButton(self.frame, text="Ingresar", command=self.intentar_login, width=260, height=40, font=("Arial", 14, "bold"))
        self.btn_ingresar.pack(pady=(25, 10))

        self.lbl_mensaje = ctk.CTkLabel(self.frame, text="", text_color="red", font=("Arial", 13))
        self.lbl_mensaje.pack(pady=5)

    def intentar_login(self):
        correo = self.entry_correo.get()
        contrasena = self.entry_password.get()

        if not correo or not contrasena:
            self.lbl_mensaje.configure(text_color="red", text="Por favor, llene todos los campos.")
            return

        login_exitoso = self.auth.iniciar_sesion(correo, contrasena)

        if login_exitoso:
            usuario = self.auth.usuario_actual
            self.lbl_mensaje.configure(text_color="green", text=f"¡Bienvenido, {usuario.nombre}!")
            self.update()
            self.after(1000, self.abrir_menu_principal)
        else:
            self.lbl_mensaje.configure(text_color="red", text="Credenciales incorrectas.")

    def abrir_menu_principal(self):
        self.destroy()
        # Nota: Asegúrate de que este import sea correcto en tu proyecto
        from vista_principal import VentanaPrincipal
        menu_principal = VentanaPrincipal(self.auth)
        menu_principal.mainloop()
