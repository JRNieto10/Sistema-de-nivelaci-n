# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from tkinter import filedialog
import os


class VentanaImportarCedulas(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Importar Usuarios")
        self.geometry("520x390")
        self.grab_set()

        ctk.CTkLabel(self, text="Importación masiva de usuarios (CSV / Excel)", font=("Arial", 14, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self, text="Acepta usuarios completos: cedula,nombres,apellidos,correo,contrasena,tipo_usuario", text_color="gray", wraplength=460).pack()

        self.entry_ruta = ctk.CTkEntry(self, width=430, placeholder_text="Ruta del archivo")
        self.entry_ruta.pack(pady=10)

        fila_botones = ctk.CTkFrame(self, fg_color="transparent")
        fila_botones.pack(pady=5)
        ctk.CTkButton(fila_botones, text="Usar CSV de ejemplo", width=145, command=self.usar_csv_ejemplo).grid(row=0, column=0, padx=5)
        ctk.CTkButton(fila_botones, text="Usar Excel de ejemplo", width=145, command=self.usar_excel_ejemplo).grid(row=0, column=1, padx=5)
        ctk.CTkButton(fila_botones, text="Examinar...", width=110, command=self.examinar).grid(row=0, column=2, padx=5)

        ctk.CTkButton(self, text="Importar", fg_color="#2ecc71", command=self.importar).pack(pady=15)

        self.lbl_resultado = ctk.CTkLabel(self, text="", wraplength=470, justify="left")
        self.lbl_resultado.pack(pady=10)

        self.usar_csv_ejemplo()


    def _ruta_importacion(self, nombre_archivo):
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(carpeta_actual, "importaciones", nombre_archivo)

    def _poner_ruta(self, ruta):
        self.entry_ruta.delete(0, "end")
        self.entry_ruta.insert(0, ruta)

    def usar_csv_ejemplo(self):
        self._poner_ruta(self._ruta_importacion("estudiantes_300_nivelacion.csv"))

    def usar_excel_ejemplo(self):
        self._poner_ruta(self._ruta_importacion("estudiantes_300_nivelacion.xlsx"))

    def examinar(self):
        ruta = filedialog.askopenfilename(filetypes=[("CSV/Excel", "*.csv *.xlsx *.xls"), ("Todos", "*.*")])
        if ruta:
            self.entry_ruta.delete(0, "end")
            self.entry_ruta.insert(0, ruta)

    def importar(self):
        ruta = self.entry_ruta.get()
        if not ruta:
            self.lbl_resultado.configure(text_color="red", text="Seleccione un archivo primero.")
            return

        resultado = self.auth.usuario_actual.importar_usuarios(ruta)
        texto = (
            f"Total leídos: {resultado.get('total', resultado['exitosos'] + resultado['duplicados'] + len(resultado['errores']))}\n"
            f"✔ Importados: {resultado['exitosos']}\n"
            f"⚠ Duplicados/Ignorados: {resultado['duplicados']}\n"
            f"✘ Errores: {len(resultado['errores'])}"
        )
        if resultado["errores"]:
            texto += "\n\nPrimeros errores:\n" + "\n".join(resultado["errores"][:8])
        self.lbl_resultado.configure(text_color="white", text=texto)
