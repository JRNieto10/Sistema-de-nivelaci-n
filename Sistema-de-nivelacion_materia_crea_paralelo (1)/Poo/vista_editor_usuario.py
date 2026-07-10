# vista_editor_usuario.py
import customtkinter as ctk

class VentanaEditorUsuario(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Modificar Datos de Usuario")
        self.geometry("400x450")
        self.grab_set()
        
        self.usuario_encontrado = None 

        # --- Interfaz ---
        ctk.CTkLabel(self, text="Buscar usuario por cédula:", font=("Arial", 14)).pack(pady=10)
        
        self.entry_cedula = ctk.CTkEntry(self, placeholder_text="Cédula", width=250)
        self.entry_cedula.pack(pady=5)

        self.btn_buscar = ctk.CTkButton(self, text="Buscar", command=self.buscar_usuario)
        self.btn_buscar.pack(pady=10)

        # Campos para editar
        ctk.CTkLabel(self, text="Datos a modificar:").pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nuevo Nombre", width=250)
        self.entry_nombre.pack(pady=5)
        
        self.entry_correo = ctk.CTkEntry(self, placeholder_text="Nuevo Correo", width=250)
        self.entry_correo.pack(pady=5)
        
        self.btn_guardar = ctk.CTkButton(self, text="Guardar Cambios", fg_color="#2ecc71", command=self.guardar_cambios)
        self.btn_guardar.pack(pady=20)

    def buscar_usuario(self):
        cedula_buscada = self.entry_cedula.get()
        # Llamamos al método que implementamos en Almacenamiento
        datos = self.auth.almacenamiento.obtener_usuario_por_cedula(cedula_buscada)
        
        if datos:
            self.usuario_encontrado = self.auth.fabrica.crear_usuario(datos)
            # Rellenar campos con los datos actuales
            self.entry_nombre.delete(0, 'end')
            self.entry_nombre.insert(0, self.usuario_encontrado.nombre)
            self.entry_correo.delete(0, 'end')
            self.entry_correo.insert(0, self.usuario_encontrado.correo)
        else:
            print("No se encontró usuario con esa cédula.")
            
    def guardar_cambios(self):
        if self.usuario_encontrado:
            # 1. Preparar los nuevos datos
            nuevos_datos = {
                "nombre": self.entry_nombre.get(),
                "correo": self.entry_correo.get()
            }
            
            # 2. Actualizar el objeto en memoria
            self.auth.usuario_actual.actualizar_datos_usuario(self.usuario_encontrado, nuevos_datos)
            
            # 3. PERSISTENCIA: Aquí es donde guardamos el cambio en el JSON
            # Debemos actualizar el archivo con la lista completa de usuarios
            datos_completos = self.auth.almacenamiento.json.repo.leer_todo()
            
            for u in datos_completos:
                if u["cedula"] == self.usuario_encontrado.cedula:
                    u["nombre"] = self.usuario_encontrado.nombre
                    u["correo"] = self.usuario_encontrado.correo
                    break
            
            self.auth.almacenamiento.json.repo.guardar_todo(datos_completos)
            print("Cambios guardados exitosamente.")
            self.destroy()