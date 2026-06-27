import customtkinter as ctk
from validaciones.permitidos_cedula import encontrar_cedula
from interfaz.registro2 import Registro2

class Registro(ctk.CTkToplevel):
    def __init__(self, inicio):
        super().__init__(inicio)
        self.inicio = inicio
        self.geometry("900x500")
        self.title("Registro")


        self.registroo2 = None
        self.variable_cedula = ctk.StringVar() 

        self.label_resultado = None
        self.entry_cedula = None
        self.bton_siguiente_registro = ctk.CTkButton(self, text="Siguiente", command=self.siguiente_registro)

        self.label_resultado = ctk.CTkLabel(self, text="")
    
    
    
    def crear_boton_volver(self):
        self.bton_volver = ctk.CTkButton(self, text="Volver", command=self.volver_inicio)
        self.bton_volver.pack()

    def volver_inicio(self):
        self.destroy()
        self.inicio.deiconify()

    def input_cedula(self):
        self.label_cedula = ctk.CTkLabel(self, text="Ingrese su cédula:")
        self.label_cedula.pack()
        self.entry_cedula = ctk.CTkEntry(self, placeholder_text="Cédula", textvariable=self.variable_cedula)
        self.entry_cedula.pack()

    def boton_validar_cedula(self):
        self.bton_validar_cedula = ctk.CTkButton(self, text="Validar Cédula", command=self.validar_cedula)
        self.bton_validar_cedula.pack()

    def validar_cedula(self):
        cedula = self.entry_cedula.get()
        encontrar = encontrar_cedula(cedula)
        if encontrar.buscar_cedula() != "No encontrada":
            self.mostrar_resultado("Cédula válida", "green")
            self.boton_siguiente_registro()  
            self.mostrar_resultado("Cédula inválida", "red")

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
    
            
            
    def boton_siguiente_registro(self):
        self.bton_siguiente_registro.pack()
        
    def siguiente_registro(self):
        if self.registroo2 is None or not self.registroo2.winfo_exists():
            self.registroo2 = Registro2(self)
            self.registroo2.crear_boton_volver()
            self.registroo2.entrada_contraseña1()
            self.registroo2.entrada_contraseña2()
            self.registroo2.boton_validar_contraseña()
        else:
            self.registroo2.deiconify()
        
        self.withdraw()