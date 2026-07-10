# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from estructura.AlmacenamietoUsuarios import Almacenamiento_Usuarios


class VentanaListaUsuarios(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Todos los usuarios registrados")
        self.geometry("760x560")
        self.grab_set()

        ctk.CTkLabel(self, text="Usuarios registrados en el sistema", font=("Arial", 18, "bold")).pack(pady=(15, 8))
        self.entry_buscar = ctk.CTkEntry(self, placeholder_text="Buscar por cédula, nombre, correo o rol", width=520)
        self.entry_buscar.pack(pady=5)
        ctk.CTkButton(self, text="Buscar / Actualizar", command=self.cargar).pack(pady=6)

        self.txt = ctk.CTkTextbox(self, width=700, height=420)
        self.txt.pack(pady=8)
        self.cargar()

    def cargar(self):
        self.txt.delete("1.0", "end")
        filtro = self.entry_buscar.get().strip().lower() if hasattr(self, "entry_buscar") else ""
        usuarios = Almacenamiento_Usuarios().listar_usuarios()
        if filtro:
            usuarios = [u for u in usuarios if filtro in " ".join(str(v).lower() for v in u.values())]
        if not usuarios:
            self.txt.insert("end", "No se encontraron usuarios.")
            return
        for rol in ["Personal", "Docente", "Estudiante"]:
            grupo = [u for u in usuarios if u.get("rol") == rol]
            if not grupo:
                continue
            self.txt.insert("end", f"\n=== {rol} ({len(grupo)}) ===\n")
            for u in grupo:
                self.txt.insert("end", f"{u.get('cedula','-')} | {u.get('nombre','')} {u.get('apellido','')} | {u.get('correo','')}\n")
