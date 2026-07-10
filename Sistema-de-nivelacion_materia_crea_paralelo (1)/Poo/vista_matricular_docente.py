# Aqui se implementa la Vista (MVC)
import customtkinter as ctk
from estructura.Almacenamiento_materias import CreadorAcademico
from estructura.Almacenamiento_horario import GuardarHorarios
from estructura.AlmacenamietoUsuarios import Almacenamiento_Usuarios


class VentanaMatricularDocente(ctk.CTkToplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.almacenador = CreadorAcademico()
        self.gestor_paralelos = GuardarHorarios()
        self.usuarios = Almacenamiento_Usuarios()

        self.title("Matricular Docente en Materia y Paralelo")
        self.geometry("520x560")
        self.grab_set()

        self.carreras = self.almacenador.json.repo.leer_todo()
        self.paralelos = self.gestor_paralelos.listar_paralelos()
        self.docentes = [u for u in self.usuarios.json.repo.leer_todo() if u.get("rol") == "Docente"]

        ctk.CTkLabel(self, text="Matricular docente", font=("Arial", 17, "bold")).pack(pady=(15, 8))

        ctk.CTkLabel(self, text="Carrera:").pack(pady=(8, 0))
        self.combo_carreras = ctk.CTkComboBox(
            self,
            values=[c.get("nombre", "") for c in self.carreras] or ["Sin carreras"],
            width=360,
            command=lambda _=None: self.actualizar_materias(),
        )
        self.combo_carreras.pack(pady=5)

        ctk.CTkLabel(self, text="Paralelo:").pack(pady=(8, 0))
        self.combo_paralelos = ctk.CTkComboBox(
            self,
            values=[f"{p.get('id')} - {p.get('nombre')} ({p.get('jornada')})" for p in self.paralelos] or ["Sin paralelos"],
            width=360,
            command=lambda _=None: self.actualizar_materias(),
        )
        self.combo_paralelos.pack(pady=5)

        ctk.CTkLabel(self, text="Materia del paralelo:").pack(pady=(8, 0))
        self.combo_materias = ctk.CTkComboBox(self, values=["Seleccione carrera y paralelo"], width=360)
        self.combo_materias.pack(pady=5)

        ctk.CTkLabel(self, text="Docente:").pack(pady=(8, 0))
        self.combo_docentes = ctk.CTkComboBox(self, values=self._valores_docentes(), width=360)
        self.combo_docentes.pack(pady=5)

        ctk.CTkButton(self, text="Confirmar matrícula", fg_color="#2ecc71", command=self.guardar).pack(pady=16)

        self.lbl_mensaje = ctk.CTkLabel(self, text="", wraplength=440, justify="left")
        self.lbl_mensaje.pack(pady=6)

        ctk.CTkLabel(self, text="Asignaciones actuales", font=("Arial", 13, "bold")).pack(pady=(10, 4))
        self.txt_resumen = ctk.CTkTextbox(self, width=460, height=145)
        self.txt_resumen.pack(pady=5)

        self.actualizar_materias()
        self.cargar_resumen()

    def _valores_docentes(self):
        if not self.docentes:
            return ["Sin docentes registrados"]
        return [f"{d.get('cedula')} - {d.get('nombre')} {d.get('apellido')}" for d in self.docentes]

    def _id_paralelo_seleccionado(self):
        valor = self.combo_paralelos.get().strip()
        return valor.split(" - ")[0] if " - " in valor else valor

    def _cedula_docente_seleccionada(self):
        valor = self.combo_docentes.get().strip()
        return valor.split(" - ")[0] if " - " in valor else valor

    def actualizar_materias(self):
        nombre_carrera = self.combo_carreras.get().strip()
        id_paralelo = self._id_paralelo_seleccionado()

        materias_carrera = []
        for carrera in self.carreras:
            if carrera.get("nombre") == nombre_carrera:
                materias_carrera = [m.get("nombre") for m in carrera.get("materias", []) if m.get("nombre")]
                break

        paralelo = self.gestor_paralelos.obtener_paralelo(id_paralelo)
        materias_paralelo = []
        if paralelo:
            materias_paralelo = paralelo.get("materias") or ([] if not paralelo.get("materia") else [paralelo.get("materia")])

        # Solo se muestran materias que existan en la carrera y estén asignadas a ese paralelo.
        if materias_carrera and materias_paralelo:
            materias = [m for m in materias_paralelo if m in materias_carrera]
        else:
            materias = materias_paralelo or materias_carrera

        if not materias:
            materias = ["Sin materias disponibles"]

        self.combo_materias.configure(values=materias)
        self.combo_materias.set(materias[0])

    def guardar(self):
        id_paralelo = self._id_paralelo_seleccionado()
        cedula_docente = self._cedula_docente_seleccionada()
        materia = self.combo_materias.get().strip()
        carrera = self.combo_carreras.get().strip()

        if "Sin" in materia or "Sin" in cedula_docente or "Sin" in id_paralelo:
            self.lbl_mensaje.configure(text_color="red", text="Faltan datos: debe existir docente, paralelo y materia.")
            return

        # Guarda docente en la carrera/materia para compatibilidad con el modelo anterior.
        self.almacenador.matricular_docente(cedula_docente, carrera, materia)

        # Guarda docente en el paralelo y materia específica.
        ok, msg = self.gestor_paralelos.asignar_docente_a_materia(id_paralelo, materia, cedula_docente)
        self.lbl_mensaje.configure(text_color="green" if ok else "red", text=msg)
        self.cargar_resumen()

    def cargar_resumen(self):
        self.txt_resumen.delete("1.0", "end")
        paralelos = self.gestor_paralelos.listar_paralelos()
        if not paralelos:
            self.txt_resumen.insert("end", "No hay paralelos creados todavía.")
            return

        docentes_por_cedula = {d.get("cedula"): f"{d.get('nombre')} {d.get('apellido')}" for d in self.docentes}
        for p in paralelos:
            self.txt_resumen.insert("end", f"{p.get('nombre')} ({p.get('jornada')})\n")
            materias = p.get("materias") or ([] if not p.get("materia") else [p.get("materia")])
            asignaciones = p.get("docentes_por_materia", {})
            if not materias:
                self.txt_resumen.insert("end", "  Sin materias asignadas.\n\n")
                continue
            for mat in materias:
                ced = asignaciones.get(mat) or p.get("docente_cedula") or "-"
                nombre_doc = docentes_por_cedula.get(ced, "Sin docente") if ced != "-" else "Sin docente"
                self.txt_resumen.insert("end", f"  • {mat}: {nombre_doc} ({ced})\n")
            self.txt_resumen.insert("end", "\n")
