import customtkinter as ctk


class Inside(ctk.CTkToplevel):
    def __init__(self,login):
        super().__init__(login)
        self.title("inside")
        self.login = login
        self.geometry("900x500")
        
    def boton_cerrarsesion(self):
        self.bton_cerrarsesion = ctk.CTkButton(
            self, text="Cerrar Sesión", command=self.cerrar_sesion
        )
        self.bton_cerrarsesion.pack()
        
    def cerrar_sesion(self):
        self.destroy()
        self.login.deiconify()
        self.login.entry_usuario.delete(0, ctk.END)  
        self.login.entry_contraseña.delete(0, ctk.END) 
        self.login.label_resultado.configure(text="") 
        
        
