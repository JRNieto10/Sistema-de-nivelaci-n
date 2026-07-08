import customtkinter as ctk
# Importamos la clase que gestiona el almacenamiento

from estructura.Almacenamiento_materias import CreadorAcademico

class VentanaCrearMateria(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Añadir Materia a Carrera")
        self.geometry("300x400")
        self.grab_set()
        
        # 1. Instanciamos el controlador de datos directamente
        self.almacenador = CreadorAcademico()
        
        # 2. Cargar carreras usando el repositorio interno del almacenador
        self.todas_las_carreras = self.almacenador.json.repo.leer_todo()
        nombres_carreras = [c['nombre'] for c in self.todas_las_carreras]

        # 3. Selector (Combobox)
        ctk.CTkLabel(self, text="Seleccionar Carrera:").pack(pady=5)
        self.combo_carrera = ctk.CTkComboBox(self, values=nombres_carreras)
        self.combo_carrera.pack(pady=5)

        # 4. Datos materia
        self.entry_id = ctk.CTkEntry(self, placeholder_text="ID Materia")
        self.entry_id.pack(pady=5)
        
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre Materia")
        self.entry_nombre.pack(pady=5)
        
        self.btn_guardar = ctk.CTkButton(self, text="Guardar Materia", command=self.guardar_materia)
        self.btn_guardar.pack(pady=20)

    def guardar_materia(self):
        nombre_carrera = self.combo_carrera.get()
        
        nueva_materia = {
            "id": self.entry_id.get(),
            "nombre": self.entry_nombre.get(),
            "creditos": 0 
        }
        
        # Corregido: Asegúrate de que las comillas y llaves estén bien balanceadas
        if self.almacenador.agregar_materia_a_carrera(nombre_carrera, nueva_materia):
            print(f"Materia '{nueva_materia['nombre']}' añadida a '{nombre_carrera}'")
            self.destroy()
        else:
            print("Error: No se pudo guardar la materia.")