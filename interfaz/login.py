import customtkinter as ctk
from validaciones.login_estudiantes import login_estudiantes
from validaciones.login_personal import login_personal
from validaciones.login_docentes import login_docentes
from interfaz_estudiantes.principal_estudiantes import inicial_estudiantes
from interfaz_docente.principa_docente import inicial_docente
from interfaz_personal.principal_personal import inicial_personal

class Login(ctk.CTkToplevel):
    def __init__(self, inicio):
        super().__init__(inicio)
        self.inicio = inicio
        self.geometry("900x500")
        self.inside_estudiante = None
        self.inside_docente=None
        self.inside_personal =None
        self.title("login")
        self.label_resultado = None 
        self.labe=None 
    
    
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
        

     

    def combox_rol(self):
        self.label_rol = ctk.CTkLabel(self, text="Seleccione su rol:")
        self.label_rol.pack()
        self.combo_rol = ctk.CTkComboBox(self, values=["Estudiante", "Docente", "Administrador"])
        self.combo_rol.pack()
    
    def mostrar_resultado(self, mensaje, color="green", errrpr=False):
        if self.label_resultado is None:
            self.label_resultado = ctk.CTkLabel(self, text="")
        
        if self.label_resultado.winfo_ismapped():
            self.label_resultado.pack_forget()
        
        if errrpr:
            self.label_resultado.configure(
                text=mensaje,
                text_color=color,
                font=("Arial", 13, "bold")
            )
        else:
            self.label_resultado.configure(
                text=mensaje,
                text_color=color,
                font=("Arial", 13, "bold")
            )
        
        self.label_resultado.pack(pady=10)

    def enviar(self):
        cedula = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        validar = None
        
        if not cedula or not contraseña:
            self.mostrar_resultado("Complete todos los campos", "red", True)
            return
        
        if self.combo_rol.get() == "Estudiante":
            pase = self.combo_rol.get()
            validar = login_estudiantes(cedula, contraseña)
            if validar.validar_login():
                self.siguiente_ventana(pase)
            else:
                self.mostrar_resultado("Usuario o contraseña incorrectos", "red", True)
                
        elif self.combo_rol.get() == "Docente":
            pase=self.combo_rol.get()
            validar = login_docentes(cedula, contraseña)
            if validar.validar_login():
                self.siguiente_ventana(pase)
            else:
                self.mostrar_resultado("Usuario o contraseña incorrectos","red", True)
                
        elif self.combo_rol.get() == "Administrador":
            pase=self.combo_rol.get()
            validar = login_personal(cedula, contraseña)
            if validar.validar_login():
                self.siguiente_ventana(pase)
            else:
                self.mostrar_resultado("Usuario o contraseña incorrectos","red", True)
        else:
            self.mostrar_resultado("Seleccione un rol válido", "orange", True)
    def siguiente_ventana(self,pase):
        self.withdraw()
        if pase == "Estudiante":
            self.inside_estudiante = inicial_estudiantes(self)
            self.inside_estudiante.crear_boton_volver()
            self.inside_estudiante.mainloop()
        elif pase == "Docente":
            self.inside_docente = inicial_docente(self)
            self.inside_docente.crear_boton_volver()
            self.inside_docente.boton_asignaturas()
            self.inside_docente.boton_horarios()
            self.inside_docente.boton_perfil()
            self.inside_docente.mainloop()
        elif pase == "Administrador":
            self.inside_personal = inicial_personal(self)
            self.inside_personal.crear_boton_volver()
            self.inside_personal.boton_gestionar_carreras()
            self.inside_personal.mainloop()

        