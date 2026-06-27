import customtkinter as ctk
from validaciones.login_estudiantes import login_estudiantes
from interfaz.inside import Inside
class Login(ctk.CTkToplevel):
    def __init__(self, inicio):
        super().__init__(inicio)
        self.inicio = inicio
        self.geometry("900x500")
        self.inside = None
        self.title("login")
        self.label_resultado = None  
    
    
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_inicio
        )
        self.bton_volver.pack()

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()
        
    def crear_entrada_cedula(self):
        self.label_usuario = ctk.CTkLabel(self, text="Ingrese su cedula:")
        self.label_usuario.pack()
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Cedula")
        self.entry_usuario.pack()
        
        
    def crear_entrada_contraseña(self):
        self.label_contraseña = ctk.CTkLabel(self, text="Ingrese su contraseña:")
        self.label_contraseña.pack()
        self.entry_contraseña = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_contraseña.pack()
        
    def boton_enviar(self):
        self.bton_enviar = ctk.CTkButton(self, text="Enviar", command=self.enviar)
        self.bton_enviar.pack()
        
    def enviar(self):
        cedula = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        validar = login_estudiantes(cedula, contraseña)
        if validar.validar_login():
            self.mostrar_resultado("Login exitoso", "green")
            if self.inside is None or not self.inside.winfo_exists():
                self.inside = Inside(self)
                self.inside.boton_cerrarsesion()
                
            else:
                self.inside.deiconify()

            self.withdraw()
                
      
    
    def mostrar_resultado(self, mensaje, color):
        if self.label_resultado is None:
            self.label_resultado = ctk.CTkLabel(self, text="")

        self.label_resultado.configure(
            text=mensaje,
            text_color=color,
            font=("Arial", 13, "bold")
        )


        if not self.label_resultado.winfo_ismapped():
            self.label_resultado.pack(pady=10)
    
            