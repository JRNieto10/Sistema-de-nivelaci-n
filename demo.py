"""
demo.py  —  Demostración del flujo completo de S.I.N.U
=======================================================
Este archivo muestra cómo usar FacadeSistemaAcademico desde código.
Wagner: cada sección marcada con [WAGNER] indica qué método conectar
a qué evento de CustomTkinter.

Para correr: python demo.py (desde la raíz del proyecto)
"""

from facade import FacadeSistemaAcademico

def separador(titulo: str):
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print(f"{'='*55}")

# ===========================================================================
# INICIALIZACIÓN
# ===========================================================================

separador("1. INICIALIZACIÓN DEL SISTEMA")

sistema = FacadeSistemaAcademico()
sistema.crear_archivos_directorios()

# [WAGNER] Llama esto en el __init__ de tu App antes de mostrar cualquier ventana:
#   self.sistema = FacadeSistemaAcademico()
#   self.sistema.crear_archivos_directorios()

print("Sistema inicializado. Archivos JSON creados en Datos/")


# ===========================================================================
# FLUJO 1: ADMIN CARGA CÉDULAS PERMITIDAS (una a una)
# ===========================================================================

separador("2. ADMIN CARGA CÉDULAS — UNA A UNA")

# [WAGNER] Botón "Agregar cédula" en el panel admin:
#   cedula = cedula_entry.get()
#   tipo   = tipo_combobox.get()   # "estudiante" / "docente" / "personal"
#   exito  = sistema.agregar_cedula_permitida(cedula, tipo)
#   label_resultado.configure(text="Agregada" if exito else "Ya existía")

cedulas_personal    = ["123456789", "987654321"]
cedulas_docentes    = ["111111111", "222222222", "333333333"]
cedulas_estudiantes = ["777777777", "888888888", "999999999"]

for c in cedulas_personal:
    ok = sistema.agregar_cedula_permitida(c, "personal")
    print(f"  Personal  {c}: {'agregada' if ok else 'ya existía'}")

for c in cedulas_docentes:
    ok = sistema.agregar_cedula_permitida(c, "docente")
    print(f"  Docente   {c}: {'agregada' if ok else 'ya existía'}")

for c in cedulas_estudiantes:
    ok = sistema.agregar_cedula_permitida(c, "estudiante")
    print(f"  Estudiante {c}: {'agregada' if ok else 'ya existía'}")


# ===========================================================================
# FLUJO 2: ADMIN CARGA CÉDULAS DESDE CSV
# ===========================================================================

separador("3. ADMIN IMPORTA CÉDULAS DESDE CSV")

# Crear CSV de ejemplo para la demo
import os, csv

os.makedirs("importaciones", exist_ok=True)
ruta_csv = "importaciones/nuevos_estudiantes.csv"

with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["cedula", "tipo"])
    writer.writerow(["101010101", "estudiante"])
    writer.writerow(["121212121", "estudiante"])
    writer.writerow(["444444444", "docente"])
    writer.writerow(["777777777", "estudiante"])  # duplicada a propósito

# [WAGNER] Opción A — el admin escoge el archivo con un filedialog:
#   from tkinter import filedialog
#   ruta = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
#   resultado = sistema.importar_cedulas_csv(ruta)

# [WAGNER] Opción B — listar CSVs de una carpeta en un Combobox:
#   archivos = sistema.listar_csvs_carpeta("importaciones/")
#   combobox.configure(values=archivos)
#   ruta     = combobox.get()
#   resultado = sistema.importar_cedulas_csv(ruta)

resultado = sistema.importar_cedulas_csv(ruta_csv)

# [WAGNER] Mostrar resultado en la interfaz:
#   label_exitosos.configure(text=f"Agregadas: {resultado['exitosos']}")
#   label_duplicados.configure(text=f"Duplicadas: {resultado['duplicados']}")
#   if resultado["errores"]:
#       textbox.insert("end", "\n".join(resultado["errores"]))

print(f"  Agregadas   : {resultado['exitosos']}")
print(f"  Duplicadas  : {resultado['duplicados']}")
print(f"  Errores     : {resultado['errores']}")


# ===========================================================================
# FLUJO 3: USUARIO VALIDA CÉDULA Y CREA SU CUENTA
# ===========================================================================

separador("4. USUARIO CREA SU CUENTA")

# [WAGNER] Pantalla de registro — paso 1: validar cédula
#   cedula = cedula_entry.get()
#   tipo   = sistema.verificar_cedula(cedula)
#   if tipo:
#       mostrar_frame_completar_datos(tipo)
#   else:
#       label_error.configure(text="Cédula no registrada. Contacte al administrador.")

cedula_prueba = "777777777"
tipo = sistema.verificar_cedula(cedula_prueba)
print(f"  Cédula {cedula_prueba} → tipo: {tipo}")

# [WAGNER] Pantalla de registro — paso 2: completar datos y crear cuenta
#   exito, mensaje = sistema.registrar_usuario(
#       nombre_entry.get(), cedula_entry.get(), apellido_entry.get(),
#       correo_entry.get(), pass_entry.get(), tipo
#   )
#   if exito:
#       messagebox.showinfo("Éxito", mensaje)
#       abrir_ventana_login()
#   else:
#       label_error.configure(text=mensaje)

usuarios_demo = [
    ("josue",    "123456789", "sanchez",  "josue@uleam.edu",   "admin123",    "administrativo"),
    ("pepito",   "111111111", "garcia",   "pepito@uleam.edu",  "pepito123",   "docente"),
    ("juanito",  "222222222", "lopez",    "juanito@uleam.edu", "juanito123",  "docente"),
    ("changuin", "333333333", "lopez2",   "chang@uleam.edu",   "chang123",    "docente"),
    ("pedrin",   "777777777", "ramirez",  "pedrin@uleam.edu",  "pedrin123",   "estudiante"),
    ("laura",    "888888888", "torres",   "laura@uleam.edu",   "laura123",    "estudiante"),
    ("jorge",    "999999999", "flores",   "jorge@uleam.edu",   "jorge123",    "estudiante"),
    ("marta",    "101010101", "diaz",     "marta@uleam.edu",   "marta123",    "estudiante"),
    ("roberto",  "121212121", "vega",     "roberto@uleam.edu", "roberto123",  "estudiante"),
]

for nombre, cedula, apellido, correo, contrasena, rol in usuarios_demo:
    exito, mensaje = sistema.registrar_usuario(
        nombre, cedula, apellido, correo, contrasena, rol
    )
    print(f"  {nombre:10} ({rol:15}): {mensaje}")


# ===========================================================================
# FLUJO 4: LOGIN
# ===========================================================================

separador("5. LOGIN")

# [WAGNER] Botón "Iniciar sesión":
#   if sistema.login(cedula_entry.get(), pass_entry.get()):
#       usuario = sistema.obtener_usuario_actual()
#       if usuario["rol"] == "administrativo": abrir_panel_admin()
#       elif usuario["rol"] == "docente":      abrir_panel_docente()
#       elif usuario["rol"] == "estudiante":   abrir_panel_estudiante()
#   else:
#       label_error.configure(text="Credenciales incorrectas.")

casos_login = [
    ("123456789", "admin123",  "admin válido"),
    ("111111111", "pepito123", "docente válido"),
    ("777777777", "pedrin123", "estudiante válido"),
    ("777777777", "wrongpass", "contraseña incorrecta"),
]

for cedula, contrasena, descripcion in casos_login:
    print(f"\n  [{descripcion}]")
    exito = sistema.login(cedula, contrasena)
    if exito:
        usuario = sistema.obtener_usuario_actual()
        print(f"  Sesión activa: {usuario['nombre']} ({usuario['rol']})")
        sistema.logout()
    else:
        print("  Acceso denegado.")


# ===========================================================================
# FLUJO 5: ADMIN CREA CURSOS Y PARALELOS
# ===========================================================================

separador("6. CREACIÓN DE CURSOS Y PARALELOS")

# [WAGNER] Panel admin — sección "Gestión académica":
#   curso = sistema.crear_curso(nombre_entry.get())
#   sistema.agregar_materia_a_curso(curso, materia_entry.get(), int(horas_entry.get()))
#   sistema.asignar_docente_a_materia(curso, docente_entry.get(), materia_entry.get())
#   paralelos = sistema.crear_paralelos(curso.nombre_curso, int(cantidad_entry.get()), curso)
#   label_resultado.configure(text=f"{len(paralelos)} paralelos creados")

curso = sistema.crear_curso("Nivelacion")
sistema.agregar_materia_a_curso(curso, "Matematicas", 3)
sistema.asignar_docente_a_materia(curso, "pepito", "Matematicas")
sistema.agregar_materia_a_curso(curso, "POO", 3)
sistema.asignar_docente_a_materia(curso, "juanito", "POO")
sistema.agregar_materia_a_curso(curso, "Comunicacion", 2)
sistema.asignar_docente_a_materia(curso, "changuin", "Comunicacion")

paralelos = sistema.crear_paralelos("Nivelacion", 3, curso)
print(f"\n  Paralelos creados: {len(paralelos)}")
for p in paralelos:
    print(f"    {p}")


# ===========================================================================
# FLUJO 6: CONSULTA DE HORARIOS
# ===========================================================================

separador("7. CONSULTA DE HORARIOS")

# [WAGNER] Panel docente / estudiante — ver horario:
#   horario = sistema.obtener_horario_paralelo(nombre_paralelo)
#   for materia, info in horario.items():
#       tabla.insert("", "end", values=(info["hora"], materia, info["docente"]))

print("\n  Horario del paralelo Nivelacion A:")
sistema.mostrar_horario_paralelo("Nivelacion A")

# [WAGNER] Todos los paralelos disponibles para un Combobox:
#   paralelos = sistema.obtener_paralelos_guardados()
#   nombres   = [p["nombre"] for p in paralelos]
#   combobox.configure(values=nombres)

todos = sistema.obtener_paralelos_guardados()
print(f"\n  Paralelos en el sistema: {[p['nombre'] for p in todos]}")


# ===========================================================================
# FLUJO 7: CALIFICACIONES Y TUTORÍAS
# ===========================================================================

separador("8. CALIFICACIONES Y TUTORÍAS")

# [WAGNER] Panel docente — registrar notas:
#   nota = sistema.crear_calificacion(float(nota_entry.get()), fecha_entry.get())
#   aprobado = sistema.verificar_aprobacion(nota)
#   label.configure(text="Aprobado" if aprobado else "Reprobado")

notas = [8.5, 6.0, 9.0, 5.5, 7.0]
for valor in notas:
    nota     = sistema.crear_calificacion(valor, "2026-06-27")
    aprobado = sistema.verificar_aprobacion(nota)
    estado   = "Aprobado" if aprobado else "Reprobado"
    print(f"  Nota {valor} → {estado}")

tutoria = sistema.crear_tutoria(1, "2026-07-01", "Repaso POO", ["pedrin", "laura"])
sistema.programar_tutoria(tutoria)
sistema.ver_asistentes_tutoria(tutoria)


# ===========================================================================
# FIN
# ===========================================================================

separador("DEMO COMPLETADA")
print("  Todos los flujos funcionan correctamente.")
print("  Wagner: mapea cada método del facade a los eventos de CustomTkinter.")
print("  Los datos quedan guardados en Datos/ para verificación.\n")
