# Aqui se implementa la Vista (MVC)
# Aqui se hizo configuracion dinamica de segmentos de evaluacion
import customtkinter as ctk
from estructura.Almacenamiento_evaluaciones import Almacenamiento_Evaluaciones


class VentanaConfigurarEvaluaciones(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.gestor = Almacenamiento_Evaluaciones()
        self.title("Configurar evaluaciones")
        self.geometry("560x620")
        self.grab_set()
        self.filas = []

        config = self.gestor.obtener_configuracion()

        ctk.CTkLabel(self, text="Configurar segmentos de calificación", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self, text="La suma de porcentajes debe ser 100%. La nota final por defecto es 10.", wraplength=480, text_color="gray").pack(pady=(0, 10))

        self.entry_nota_final = ctk.CTkEntry(self, placeholder_text="Nota final", width=160)
        self.entry_nota_final.insert(0, str(config.get("nota_final", 10)))
        self.entry_nota_final.pack(pady=6)

        self.frame = ctk.CTkScrollableFrame(self, width=500, height=360)
        self.frame.pack(pady=10)

        for seg in config.get("segmentos", []):
            self.agregar_fila(seg.get("nombre", ""), seg.get("porcentaje", ""))

        ctk.CTkButton(self, text="+ Agregar segmento", command=lambda: self.agregar_fila("", ""), fg_color="#3498db").pack(pady=5)
        self.lbl_mensaje = ctk.CTkLabel(self, text="", wraplength=480)
        self.lbl_mensaje.pack(pady=6)
        ctk.CTkButton(self, text="Guardar configuración", command=self.guardar, fg_color="#2ecc71").pack(pady=10)

    def agregar_fila(self, nombre, porcentaje):
        fila = ctk.CTkFrame(self.frame)
        fila.pack(fill="x", pady=5)
        e_nombre = ctk.CTkEntry(fila, placeholder_text="Segmento", width=260)
        e_nombre.insert(0, str(nombre))
        e_nombre.pack(side="left", padx=5)
        e_porcentaje = ctk.CTkEntry(fila, placeholder_text="%", width=90)
        e_porcentaje.insert(0, str(porcentaje))
        e_porcentaje.pack(side="left", padx=5)
        ctk.CTkButton(fila, text="X", width=40, fg_color="#e74c3c", command=lambda: self.eliminar_fila(fila)).pack(side="left", padx=5)
        self.filas.append((fila, e_nombre, e_porcentaje))

    def eliminar_fila(self, fila):
        self.filas = [f for f in self.filas if f[0] != fila]
        fila.destroy()

    def guardar(self):
        try:
            nota_final = float(self.entry_nota_final.get())
            segmentos = []
            for _, e_nombre, e_porcentaje in self.filas:
                if e_nombre.winfo_exists() and e_porcentaje.winfo_exists():
                    segmentos.append({"nombre": e_nombre.get().strip(), "porcentaje": float(e_porcentaje.get())})
        except ValueError:
            self.lbl_mensaje.configure(text_color="red", text="La nota final y los porcentajes deben ser numéricos.")
            return
        ok, msg = self.auth.usuario_actual.configurar_evaluaciones(segmentos, nota_final)
        self.lbl_mensaje.configure(text_color="green" if ok else "red", text=msg)
