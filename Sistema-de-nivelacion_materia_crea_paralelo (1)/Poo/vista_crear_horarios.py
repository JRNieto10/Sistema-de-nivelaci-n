# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from estructura.Almacenamiento_horario import GuardarHorarios


class VentanaCrearHorarios(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.gestor = GuardarHorarios()
        self.title("Crear Horarios por Paralelo")
        self.geometry("520x520")
        self.grab_set()

        ctk.CTkLabel(self, text="Crear horarios automáticos", font=("Arial", 17, "bold")).pack(pady=(15, 8))
        ctk.CTkLabel(
            self,
            text="Seleccione un paralelo. El sistema generará horarios para sus materias según la jornada: matutina, vespertina o nocturna.",
            wraplength=440,
            justify="left",
            text_color="gray",
        ).pack(pady=(0, 10))

        self.paralelos = self.gestor.listar_paralelos()
        self.combo_paralelos = ctk.CTkComboBox(self, values=self._valores_paralelos(), width=390)
        self.combo_paralelos.pack(pady=8)

        ctk.CTkButton(self, text="Generar horarios", fg_color="#16a085", command=self.generar).pack(pady=12)

        self.lbl_mensaje = ctk.CTkLabel(self, text="", wraplength=430)
        self.lbl_mensaje.pack(pady=5)

        ctk.CTkLabel(self, text="Horarios actuales", font=("Arial", 13, "bold")).pack(pady=(10, 4))
        self.txt_horarios = ctk.CTkTextbox(self, width=460, height=255)
        self.txt_horarios.pack(pady=5)
        self.cargar_resumen()

    def _valores_paralelos(self):
        if not self.paralelos:
            return ["Sin paralelos"]
        return [f"{p.get('id')} - {p.get('nombre')} ({p.get('jornada')})" for p in self.paralelos]

    def _id_paralelo_seleccionado(self):
        valor = self.combo_paralelos.get().strip()
        return valor.split(" - ")[0] if " - " in valor else valor

    def generar(self):
        id_paralelo = self._id_paralelo_seleccionado()
        if not id_paralelo or id_paralelo == "Sin paralelos":
            self.lbl_mensaje.configure(text_color="red", text="Primero debe crear un paralelo.")
            return
        ok, msg = self.gestor.generar_horarios_paralelo(id_paralelo)
        self.lbl_mensaje.configure(text_color="green" if ok else "red", text=msg)
        self.paralelos = self.gestor.listar_paralelos()
        self.cargar_resumen()

    def cargar_resumen(self):
        self.txt_horarios.delete("1.0", "end")
        paralelos = self.gestor.listar_paralelos()
        if not paralelos:
            self.txt_horarios.insert("end", "No hay paralelos creados todavía.")
            return
        for p in paralelos:
            self.txt_horarios.insert("end", f"{p.get('nombre')} - Jornada {p.get('jornada')}\n")
            horarios = p.get("horarios_por_materia", {})
            if not horarios:
                self.txt_horarios.insert("end", "  Sin horarios generados.\n\n")
                continue
            for materia, h in horarios.items():
                self.txt_horarios.insert(
                    "end",
                    f"  • {materia}: {h.get('dia')} {h.get('hora_inicio')}-{h.get('hora_fin')} | {h.get('aula')}\n",
                )
            self.txt_horarios.insert("end", "\n")
