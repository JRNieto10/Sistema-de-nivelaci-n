import customtkinter as ctk

class Login(ctk.CTkToplevel):
	def __init__(self,inicio):
		super().__init__(inicio)
		self.inicio = inicio
		self.geometry("900x500")
		self.title("login")

	def crear_boton_volver(self):
		self.bton_volver = ctk.CTkButton(self, text="Volver", command=self.volver_inicio)
		self.bton_volver.pack()

	def volver_inicio(self):
		self.destroy()
		self.inicio.deiconify()  