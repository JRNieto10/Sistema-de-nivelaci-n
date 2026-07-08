import customtkinter as ctk
from facade import FacadeSistemaAcademico
import tkinter.messagebox as messagebox
from tkinter import filedialog
from estructura.estrategias_importacion import (
    ImportacionCSV,
    ImportacionJSON,
    ImportacionExcel,
    ImportacionTXT,
    ImportacionAutomatica,
    FabricaEstrategias
)

class Permitidos_gestionar(ctk.CTkToplevel):
    def __init__(self, principal, carrera_actual=None):
        super().__init__(principal)
        self.title("Gestion de Cedulas Permitidas")
        self.principal = principal
        self.carrera_actual = carrera_actual
        self.sistema = FacadeSistemaAcademico()
        self.geometry("900x750")
        
        self.cedula_seleccionada = None
        self.tipo_seleccionado = None
        self.formato_actual = "csv"

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestion de Cedulas Permitidas",
            font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        if self.carrera_actual:
            self.label_carrera = ctk.CTkLabel(
                self.frame_principal,
                text=f"Carrera: {self.carrera_actual.nombre} (ID: {self.carrera_actual.id})",
                font=("Arial", 16),
                text_color="#3498db"
            )
            self.label_carrera.pack(pady=10)

        self.frame_agregar = ctk.CTkFrame(self.frame_principal)
        self.frame_agregar.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            self.frame_agregar,
            text="Agregar Nueva Cedula Permitida",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        frame_input = ctk.CTkFrame(self.frame_agregar, fg_color="transparent")
        frame_input.pack(pady=10)

        ctk.CTkLabel(frame_input, text="Cedula:").pack(side="left", padx=5)
        self.entry_cedula = ctk.CTkEntry(
            frame_input,
            placeholder_text="Ingrese la cedula",
            width=250,
            height=35
        )
        self.entry_cedula.pack(side="left", padx=5)

        ctk.CTkLabel(frame_input, text="Rol:").pack(side="left", padx=5)
        self.combobox_rol = ctk.CTkComboBox(
            frame_input,
            values=["Estudiante", "Docente", "Personal"],
            width=150,
            height=35
        )
        self.combobox_rol.pack(side="left", padx=5)
        self.combobox_rol.set("Seleccione rol")

        self.btn_agregar = ctk.CTkButton(
            frame_input,
            text="+ Agregar Cedula",
            command=self.agregar_cedula,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=150,
            height=35
        )
        self.btn_agregar.pack(side="left", padx=10)

        frame_formato = ctk.CTkFrame(self.frame_agregar, fg_color="transparent")
        frame_formato.pack(pady=5)

        ctk.CTkLabel(frame_formato, text="Formato de importacion:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.combobox_formato = ctk.CTkComboBox(
            frame_formato,
            values=["CSV", "JSON", "Excel", "TXT", "Automatico"],
            width=150,
            height=30,
            command=self.cambiar_formato
        )
        self.combobox_formato.pack(side="left", padx=5)
        self.combobox_formato.set("Automatico")

        frame_importar = ctk.CTkFrame(self.frame_agregar, fg_color="transparent")
        frame_importar.pack(pady=5)

        self.btn_importar = ctk.CTkButton(
            frame_importar,
            text="Importar Archivo",
            command=self.importar_archivo,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=180,
            height=35
        )
        self.btn_importar.pack(side="left", padx=5)

        self.btn_importar_masivo = ctk.CTkButton(
            frame_importar,
            text="Importar Masivo (Ejemplo)",
            command=self.importar_masivo_ejemplo,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            width=180,
            height=35
        )
        self.btn_importar_masivo.pack(side="left", padx=5)

        ctk.CTkFrame(self.frame_principal, height=2, fg_color="#ccc").pack(fill="x", padx=10, pady=10)

        self.frame_lista = ctk.CTkFrame(self.frame_principal)
        self.frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_lista = ctk.CTkLabel(
            self.frame_lista,
            text="Cedulas Permitidas Registradas:",
            font=("Arial", 14, "bold")
        )
        self.label_lista.pack(pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_lista)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_botones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botones.pack(pady=15)

        self.btn_eliminar = ctk.CTkButton(
            self.frame_botones,
            text="Eliminar Seleccionada",
            command=self.eliminar_cedula,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=200,
            height=40
        )
        self.btn_eliminar.pack(side="left", padx=10)

        self.btn_limpiar_todos = ctk.CTkButton(
            self.frame_botones,
            text="Limpiar Todas",
            command=self.limpiar_todas_cedulas,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=200,
            height=40
        )
        self.btn_limpiar_todos.pack(side="left", padx=10)

        self.btn_volver = ctk.CTkButton(
            self.frame_botones,
            text="Volver",
            command=self.volver_principal,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=150,
            height=40
        )
        self.btn_volver.pack(side="left", padx=10)

        self.label_mensaje = ctk.CTkLabel(
            self.frame_principal,
            text="",
            font=("Arial", 12)
        )
        self.label_mensaje.pack(pady=5)

        self.cargar_cedulas()

    def cambiar_formato(self, valor):
        formato_map = {
            "CSV": "csv",
            "JSON": "json",
            "Excel": "excel",
            "TXT": "txt",
            "Automatico": "auto"
        }
        self.formato_actual = formato_map.get(valor, "auto")
        self.sistema.set_estrategia_por_formato(self.formato_actual)
        self.label_mensaje.configure(
            text=f"Formato de importacion: {valor}",
            text_color="#3498db"
        )

    def importar_archivo(self):
        tipos_archivo = []
        
        if self.formato_actual == "csv":
            tipos_archivo = [("Archivos CSV", "*.csv")]
        elif self.formato_actual == "json":
            tipos_archivo = [("Archivos JSON", "*.json")]
        elif self.formato_actual == "excel":
            tipos_archivo = [("Archivos Excel", "*.xlsx")]
        elif self.formato_actual == "txt":
            tipos_archivo = [("Archivos TXT", "*.txt")]
        else:
            tipos_archivo = [
                ("Todos los archivos soportados", "*.csv;*.json;*.xlsx;*.txt"),
                ("Archivos CSV", "*.csv"),
                ("Archivos JSON", "*.json"),
                ("Archivos Excel", "*.xlsx"),
                ("Archivos TXT", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo para importar",
            filetypes=tipos_archivo
        )

        if not archivo:
            return

        try:
            resultado = self.sistema.importar_cedulas(archivo)
            
            mensaje = "=" * 50 + "\n"
            mensaje += "RESULTADO DE IMPORTACION\n"
            mensaje += "=" * 50 + "\n\n"
            mensaje += f"Cedulas agregadas: {resultado['exitosos']}\n"
            mensaje += f"Cedulas duplicadas: {resultado['duplicados']}\n"
            
            if resultado['errores']:
                mensaje += f"\nErrores ({len(resultado['errores'])}):\n"
                for error in resultado['errores'][:10]:
                    mensaje += f"   - {error}\n"
                if len(resultado['errores']) > 10:
                    mensaje += f"   ... y {len(resultado['errores']) - 10} errores mas"
            
            messagebox.showinfo("Resultado de Importacion", mensaje)
            self.cargar_cedulas()
            
            if resultado['exitosos'] > 0:
                self.label_mensaje.configure(
                    text=f"{resultado['exitosos']} cedulas importadas correctamente",
                    text_color="#2ecc71"
                )
            else:
                self.label_mensaje.configure(
                    text="No se importaron nuevas cedulas",
                    text_color="#f39c12"
                )
                
        except Exception as e:
            self.label_mensaje.configure(
                text=f"Error al importar: {str(e)}",
                text_color="red"
            )
            messagebox.showerror("Error", f"No se pudo importar el archivo:\n{str(e)}")

    def importar_desde_csv(self):
        self.importar_archivo()

    def importar_masivo_ejemplo(self):
        cedulas_ejemplo = [
            {"cedula": "1515151515", "tipo": "estudiante"},
            {"cedula": "1616161616", "tipo": "estudiante"},
            {"cedula": "1717171717", "tipo": "estudiante"},
            {"cedula": "1818181818", "tipo": "docente"},
            {"cedula": "1919191919", "tipo": "docente"},
            {"cedula": "2020202020", "tipo": "personal"}
        ]
        
        importados = []
        duplicados = []
        
        for item in cedulas_ejemplo:
            if self.sistema.agregar_cedula_permitida(item["cedula"], item["tipo"]):
                importados.append(f"{item['cedula']} ({item['tipo']})")
            else:
                duplicados.append(f"{item['cedula']} ({item['tipo']})")
        
        mensaje = f"Cedulas importadas: {len(importados)}\n"
        if importados:
            mensaje += "\nImportadas:\n" + "\n".join(f"   - {i}" for i in importados)
        if duplicados:
            mensaje += f"\n\nYa existian ({len(duplicados)}):\n" + "\n".join(f"   - {d}" for d in duplicados)
        
        messagebox.showinfo("Importacion Masiva", mensaje)
        self.cargar_cedulas()
        
        if importados:
            self.label_mensaje.configure(
                text=f"{len(importados)} cedulas importadas",
                text_color="#2ecc71"
            )
        else:
            self.label_mensaje.configure(
                text="Todas las cedulas ya existian",
                text_color="#f39c12"
            )

    def cargar_cedulas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        datos = self.sistema.obtener_todas_cedulas()

        total = len(datos["estudiantes"]) + len(datos["docentes"]) + len(datos["personal"])

        if total == 0:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay cedulas permitidas registradas",
                font=("Arial", 14),
                text_color="#666"
            ).pack(pady=20)
            return

        contador = 0

        if datos["estudiantes"]:
            ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Estudiantes ({len(datos['estudiantes'])}):",
                font=("Arial", 14, "bold"),
                text_color="#3498db"
            ).pack(anchor="w", padx=10, pady=5)

            for cedula in datos["estudiantes"]:
                contador += 1
                self._crear_item_cedula(contador, cedula, "estudiante")

        if datos["docentes"]:
            ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Docentes ({len(datos['docentes'])}):",
                font=("Arial", 14, "bold"),
                text_color="#f39c12"
            ).pack(anchor="w", padx=10, pady=5)

            for cedula in datos["docentes"]:
                contador += 1
                self._crear_item_cedula(contador, cedula, "docente")

        if datos["personal"]:
            ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Personal Administrativo ({len(datos['personal'])}):",
                font=("Arial", 14, "bold"),
                text_color="#9b59b6"
            ).pack(anchor="w", padx=10, pady=5)

            for cedula in datos["personal"]:
                contador += 1
                self._crear_item_cedula(contador, cedula, "personal")

    def _crear_item_cedula(self, numero, cedula, tipo):
        frame_item = ctk.CTkFrame(self.scrollable_frame)
        frame_item.pack(fill="x", padx=5, pady=3)

        frame_contenido = ctk.CTkFrame(frame_item, fg_color="transparent")
        frame_contenido.pack(fill="x", padx=10, pady=5)

        colores = {
            "estudiante": "#3498db",
            "docente": "#f39c12",
            "personal": "#9b59b6"
        }

        label_info = ctk.CTkLabel(
            frame_contenido,
            text=f"{numero}. {cedula} | {tipo.capitalize()}",
            font=("Arial", 13),
            text_color=colores.get(tipo, "#000000")
        )
        label_info.pack(side="left", padx=10)

        ctk.CTkButton(
            frame_contenido,
            text="Seleccionar",
            command=lambda: self.seleccionar_cedula(cedula, tipo),
            fg_color="#3498db",
            hover_color="#2980b9",
            width=100,
            height=30
        ).pack(side="right", padx=5)

        frame_contenido.bind("<Button-1>", lambda e, c=cedula, t=tipo: self.seleccionar_cedula(c, t))
        label_info.bind("<Button-1>", lambda e, c=cedula, t=tipo: self.seleccionar_cedula(c, t))

    def seleccionar_cedula(self, cedula, tipo):
        self.cedula_seleccionada = cedula
        self.tipo_seleccionado = tipo
        self.label_mensaje.configure(
            text=f"Cedula seleccionada: {cedula} (Rol: {tipo.capitalize()})",
            text_color="#2ecc71"
        )

    def agregar_cedula(self):
        cedula = self.entry_cedula.get().strip()
        rol = self.combobox_rol.get()

        if not cedula:
            self.label_mensaje.configure(text="Ingrese una cedula", text_color="red")
            return

        if rol == "Seleccione rol":
            self.label_mensaje.configure(text="Seleccione un rol", text_color="red")
            return

        if not cedula.isdigit():
            self.label_mensaje.configure(text="La cedula debe contener solo numeros", text_color="red")
            return

        if len(cedula) != 10:
            self.label_mensaje.configure(text="La cedula debe tener 10 digitos", text_color="red")
            return

        rol_dict = {
            "Estudiante": "estudiante",
            "Docente": "docente",
            "Personal": "personal"
        }

        existe = self.sistema.verificar_cedula(cedula)
        if existe:
            self.label_mensaje.configure(
                text=f"La cedula {cedula} ya esta registrada como {existe}",
                text_color="red"
            )
            return

        resultado = self.sistema.agregar_cedula_permitida(cedula, rol_dict[rol])

        if resultado:
            self.label_mensaje.configure(text=f"Cedula {cedula} agregada como {rol}", text_color="#2ecc71")
            self.entry_cedula.delete(0, 'end')
            self.combobox_rol.set("Seleccione rol")
            self.cargar_cedulas()
            self.cedula_seleccionada = None
            self.tipo_seleccionado = None
            messagebox.showinfo("Exito", f"Cedula {cedula} agregada exitosamente como {rol}")
        else:
            self.label_mensaje.configure(text="Error al agregar la cedula", text_color="red")

    def limpiar_todas_cedulas(self):
        respuesta = messagebox.askyesno(
            "Confirmar",
            "Esta seguro de eliminar TODAS las cedulas permitidas?\nEsta accion no se puede deshacer."
        )

        if respuesta:
            self.sistema.limpiar_todas_cedulas()
            self.cargar_cedulas()
            self.label_mensaje.configure(text="Todas las cedulas han sido eliminadas", text_color="#e74c3c")
            messagebox.showinfo("Limpiar", "Todas las cedulas permitidas han sido eliminadas")

    def eliminar_cedula(self):
        if not self.cedula_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una cedula para eliminar")
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Eliminar la cedula {self.cedula_seleccionada} (Rol: {self.tipo_seleccionado.capitalize()})?"
        )

        if respuesta:
            resultado = self.sistema.eliminar_cedula_permitida(
                self.cedula_seleccionada,
                self.tipo_seleccionado
            )

            if resultado:
                self.label_mensaje.configure(text=f"Cedula {self.cedula_seleccionada} eliminada", text_color="#2ecc71")
                cedula_eliminada = self.cedula_seleccionada
                self.cedula_seleccionada = None
                self.tipo_seleccionado = None
                self.cargar_cedulas()
                messagebox.showinfo("Exito", f"Cedula {cedula_eliminada} eliminada correctamente")
            else:
                self.label_mensaje.configure(text="Error al eliminar la cedula", text_color="red")

    def volver_principal(self):
        self.destroy()
        if self.principal and self.principal.winfo_exists():
            self.principal.deiconify()