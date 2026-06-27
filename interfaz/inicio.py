import customtkinter as ctk
from interfaz.login import Login
from interfaz.registro import Registro


class Inicio(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.loginn = None
		self.registroo = None

		self.geometry("900x500")
		self.title("Principal")

	def crear_boton_login(self):
		self.bton = ctk.CTkButton(self, text="Iniciar Sesión", command=self.abrir_login)
		self.bton.pack()

	def abrir_login(self):
		if self.loginn is None or not self.loginn.winfo_exists():
			self.loginn = Login(self)
			self.loginn.crear_boton_volver()
		else:
			self.loginn.deiconify()
        
		self.withdraw() 
	

	def crear_boton_registro(self):
		self.bton_registro = ctk.CTkButton(self, text="Registrarse", command=self.abrir_registro)
		self.bton_registro.pack()

	def abrir_registro(self):
		if self.registroo is None or not self.registroo.winfo_exists():
			self.registroo = Registro(self)
			self.registroo.crear_boton_volver()
			self.registroo.input_cedula()
			self.registroo.boton_validar_cedula()
		else:
			self.registroo.deiconify()
		
		self.withdraw()
	
	def final(self):
		self.mainloop()