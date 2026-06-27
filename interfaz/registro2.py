import customtkinter as ctk
from facade import FacadeSistemaAcademico

class Registro2(ctk.CTkToplevel):
    def __init__(self, registro1):
        super().__init__(registro1)
        self.registro1 = registro1
        self.geometry("900x500")
        self.title("registro2")
        self.sistema = FacadeSistemaAcademico()
        
        self.label_resultado = None 

    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_registro1
        )
        self.bton_volver.pack()

    def volver_registro1(self):
        self.destroy()
        self.registro1.variable_cedula.set("") 
        self.registro1.label_resultado.configure(text="")  
        self.registro1.entry_cedula.delete(0, ctk.END)  
        self.registro1.bton_siguiente_registro.pack_forget()
        self.registro1.deiconify()
        
    def entrada_contraseña1(self):
        self.label_contraseña1 = ctk.CTkLabel(self, text="Ingrese su contraseña:")
        self.label_contraseña1.pack()
        self.entry_contraseña1 = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_contraseña1.pack()  
        
    def entrada_contraseña2(self):
        self.label_contraseña2 = ctk.CTkLabel(self, text="Confirme su contraseña:")
        self.label_contraseña2.pack()
        self.entry_contraseña2 = ctk.CTkEntry(self, placeholder_text="Confirmar Contraseña", show="*")
        self.entry_contraseña2.pack()
        
    def boton_validar_contraseña(self):
        self.bton_validar_contraseña = ctk.CTkButton(self, text="Validar Contraseña", command=self.validar_contraseña)
        self.bton_validar_contraseña.pack()
        
    def validar_contraseña(self):
        contraseña1 = self.entry_contraseña1.get()
        contraseña2 = self.entry_contraseña2.get()
        if contraseña1 == contraseña2:
            self.mostrar_resultado("Contraseña válida", "green")
            self.boton_guardar()
         
            
        else:
            self.mostrar_resultado("Contraseña inválida", "red")

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
            
    def boton_guardar(self):
        self.bton_guardar = ctk.CTkButton(self, text="Guardar", command=self.guardar_datos)
        self.bton_guardar.pack()
        
    def guardar_datos(self):
        cedula = self.registro1.variable_cedula.get()
        contraseña = self.entry_contraseña1.get()
        rol = self.registro1.eleccion.combo_rol.get()
        self.sistema.registrar_usuario(cedula=cedula, contrasena=contraseña, rol=rol.lower())
        self.mostrar_resultado("Datos guardados correctamente", "green")