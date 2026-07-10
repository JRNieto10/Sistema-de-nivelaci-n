# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from estructura.Almacenamiento_materias import CreadorAcademico
from estructura.Almacenamiento_horario import GuardarHorarios


class VentanaCrearMateria(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Crear Materia con Paralelo")
        self.geometry("430x590")
        self.grab_set()

        self.almacenador = CreadorAcademico()
        self.gestor_paralelos = GuardarHorarios()

        self.todas_las_carreras = self.almacenador.json.repo.leer_todo()
        nombres_carreras = [c.get("nombre", "") for c in self.todas_las_carreras if c.get("nombre")]

        ctk.CTkLabel(self, text="Crear materia y su paralelo", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(
            self,
            text="Primero registre la materia y aquí mismo cree el paralelo donde se verá.",
            wraplength=360,
            text_color="gray",
        ).pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Seleccionar Carrera:").pack(pady=(8, 4))
        self.combo_carrera = ctk.CTkComboBox(self, values=nombres_carreras or ["-- No hay carreras --"], width=330)
        self.combo_carrera.pack(pady=4)

        ctk.CTkLabel(self, text="Datos de la Materia", font=("Arial", 13, "bold")).pack(pady=(15, 4))
        self.entry_id = ctk.CTkEntry(self, placeholder_text="ID Materia", width=330)
        self.entry_id.pack(pady=6)

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre Materia", width=330)
        self.entry_nombre.pack(pady=6)

        ctk.CTkLabel(self, text="Datos del Paralelo", font=("Arial", 13, "bold")).pack(pady=(15, 4))
        self.entry_id_paralelo = ctk.CTkEntry(self, placeholder_text="ID Paralelo (ej: POO-A-M)", width=330)
        self.entry_id_paralelo.pack(pady=6)

        self.entry_nombre_paralelo = ctk.CTkEntry(self, placeholder_text="Nombre Paralelo (ej: POO Primero A)", width=330)
        self.entry_nombre_paralelo.pack(pady=6)

        ctk.CTkLabel(self, text="Jornada:").pack(pady=(6, 2))
        self.combo_jornada = ctk.CTkComboBox(self, values=["Matutina", "Vespertina", "Nocturna"], width=330)
        self.combo_jornada.pack(pady=4)

        self.lbl_mensaje = ctk.CTkLabel(self, text="", text_color="red", wraplength=360)
        self.lbl_mensaje.pack(pady=8)

        self.btn_guardar = ctk.CTkButton(
            self,
            text="Guardar Materia y Crear Paralelo",
            command=self.guardar_materia,
            fg_color="#2ecc71",
            width=260,
        )
        self.btn_guardar.pack(pady=12)

    def guardar_materia(self):
        nombre_carrera = self.combo_carrera.get().strip()
        id_materia = self.entry_id.get().strip()
        nombre_materia = self.entry_nombre.get().strip()
        id_paralelo = self.entry_id_paralelo.get().strip()
        nombre_paralelo = self.entry_nombre_paralelo.get().strip()
        jornada = self.combo_jornada.get().strip()

        if nombre_carrera.startswith("--") or not nombre_carrera:
            self.lbl_mensaje.configure(text_color="red", text="Primero debe existir una carrera válida.")
            return

        if not id_materia or not nombre_materia:
            self.lbl_mensaje.configure(text_color="red", text="ID y nombre de la materia son obligatorios.")
            return

        if not id_paralelo or not nombre_paralelo:
            self.lbl_mensaje.configure(text_color="red", text="ID y nombre del paralelo son obligatorios.")
            return

        if not jornada:
            self.lbl_mensaje.configure(text_color="red", text="Debe seleccionar una jornada.")
            return

        if self.gestor_paralelos.obtener_paralelo(id_paralelo):
            self.lbl_mensaje.configure(text_color="red", text="Ya existe un paralelo con ese ID. Use otro ID.")
            return

        nueva_materia = {
            "id": id_materia,
            "nombre": nombre_materia,
            "creditos": 0,
            "paralelo_id": id_paralelo,
            "paralelo_nombre": nombre_paralelo,
            "jornada": jornada,
        }

        exito = self.almacenador.agregar_materia_a_carrera(nombre_carrera, nueva_materia)
        if not exito:
            self.lbl_mensaje.configure(text_color="red", text="Error: no se pudo guardar la materia en la carrera.")
            return

        # Aqui se hizo Clases y Objetos
        # Se crea el paralelo desde la misma ventana de materia.
        self.auth.usuario_actual.crear_paralelo(id_paralelo, nombre_paralelo, jornada, materia=nombre_materia)

        self.lbl_mensaje.configure(
            text_color="green",
            text="Materia creada correctamente y paralelo creado para esa materia.",
        )
        self.after(1200, self.destroy)
