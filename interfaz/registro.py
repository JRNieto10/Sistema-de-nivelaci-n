import customtkinter as ctk
from validaciones.permitidos_cedula import encontrar_cedula


class Registro(ctk.CTkToplevel):
	def __init__(self,inicio):
		super().__init__(inicio)
		self.inicio = inicio
		self.geometry("900x500")
		self.title("Registro")

	def crear_boton_volver(self):
		self.bton_volver = ctk.CTkButton(self, text="Volver", command=self.volver_inicio)
		self.bton_volver.pack()

	def volver_inicio(self):
		self.destroy()
		self.inicio.deiconify()

	def input_cedula(self):
		self.label_cedula = ctk.CTkLabel(self, text="Ingrese su cédula:")
		self.label_cedula.pack()
		self.entry_cedula = ctk.CTkEntry(self,placeholder_text="Cédula")
		self.entry_cedula.pack()
	
	def boton_validar_cedula(self):
		self.bton_validar_cedula = ctk.CTkButton(self, text="Validar Cédula", command=self.validar_cedula)
		self.bton_validar_cedula.pack()

	def validar_cedula(self):

		cedula = self.entry_cedula.get()
		encontrar=encontrar_cedula(cedula)
		if encontrar.buscar_cedula() != "No encontrada":
			self.label_resultado = ctk.CTkLabel(self, text="Cédula válida")
			self.label_resultado.pack()
		else:
			self.label_resultado = ctk.CTkLabel(self, text="Cédula inválida")
			self.label_resultado.pack()
		