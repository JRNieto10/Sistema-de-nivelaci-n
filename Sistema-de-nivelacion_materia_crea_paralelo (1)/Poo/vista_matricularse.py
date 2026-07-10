import customtkinter as ctk


class VentanaMatricularse(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Matricularme por Materia")
        self.geometry("520x330")
        self.grab_set()

        paralelos = self.auth.usuario_actual.listar_paralelos_disponibles()
        self.opciones = {}
        textos = []
        for paralelo in paralelos:
            materias = paralelo.get("materias") or ([paralelo.get("materia")] if paralelo.get("materia") else [])
            horarios = paralelo.get("horarios_por_materia", {})
            for materia in materias:
                horario = horarios.get(materia)
                if not horario and len(materias) == 1:
                    horario = paralelo.get("horario")
                if not horario:
                    detalle = "sin horario"
                else:
                    detalle = f"{horario.get('dia', '?')} {horario.get('hora_inicio', '?')}-{horario.get('hora_fin', '?')}"
                texto = f"{materia} | {paralelo.get('nombre')} ({paralelo.get('id')}) | {detalle}"
                textos.append(texto)
                self.opciones[texto] = (paralelo.get("id"), materia)

        ctk.CTkLabel(self, text="Matricula por materia", font=("Arial", 18, "bold")).pack(pady=(18, 5))
        ctk.CTkLabel(
            self,
            text="Puede escoger un paralelo diferente para cada materia, siempre que los horarios no choquen.",
            wraplength=460,
            text_color="gray",
        ).pack(pady=(0, 12))

        ctk.CTkLabel(self, text="Materia y paralelo disponibles:").pack(pady=(5, 3))
        self.combo = ctk.CTkComboBox(self, values=textos or ["-- No hay materias con horario --"], width=460)
        self.combo.pack(pady=6)

        self.lbl_mensaje = ctk.CTkLabel(self, text="", wraplength=460)
        self.lbl_mensaje.pack(pady=12)
        ctk.CTkButton(self, text="Matricularme", fg_color="#2ecc71", command=self.inscribirse).pack(pady=8)

    def inscribirse(self):
        seleccion = self.opciones.get(self.combo.get())
        if not seleccion:
            self.lbl_mensaje.configure(text_color="red", text="Seleccione una materia y paralelo validos.")
            return
        id_paralelo, materia = seleccion
        exito, mensaje = self.auth.usuario_actual.matricularse(id_paralelo, materia)
        self.lbl_mensaje.configure(text_color="#2ecc71" if exito else "red", text=mensaje)
