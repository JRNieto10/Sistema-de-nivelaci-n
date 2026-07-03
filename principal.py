from facade import FacadeSistemaAcademico
from facade_datos import FacadeDatos

sistema = FacadeSistemaAcademico()
datos = FacadeDatos()

sistema.crear_archivos_directorios()
david = sistema.crear_administrador("david", "987654321", "apellido", "david@uleam.edu", "admin321")

# Agregar cédulas permitidas
datos.agregar_cedula_permitida("77777777", "estudiante")
datos.agregar_cedula_permitida("888888888", "estudiante")
datos.agregar_cedula_permitida("999999999", "estudiante")
datos.agregar_cedula_permitida("101010101", "estudiante")
datos.agregar_cedula_permitida("121212121", "estudiante")
datos.agregar_cedula_permitida("111111111", "docente")
datos.agregar_cedula_permitida("222222222", "docente")
datos.agregar_cedula_permitida("333333333", "docente")
datos.agregar_cedula_permitida("444444444", "docente")
datos.agregar_cedula_permitida("666666666", "docente")
datos.agregar_cedula_permitida("123456789", "personal")
datos.agregar_cedula_permitida("987654321", "personal")
datos.agregar_cedula_permitida("555555555", "personal")

# Crear usuarios
josue = sistema.crear_administrador("josue", "123456789", "apellido", "josue@uleam.edu", "admin123")
jessica = sistema.crear_administrador("jessica", "555555555", "apellido", "jessica@uleam.edu", "admin132")

pepito = sistema.crear_docente("pepito", "111111111", "garcia", "pepito@uleam.edu", "pepito123")
juanito = sistema.crear_docente("juanito", "222222222", "lopez1", "juanito@uleam.edu", "juanito123")
changuin = sistema.crear_docente("changuin", "333333333", "lopez2", "changuin@uleam.edu", "changuin123")
mari = sistema.crear_docente("mari", "444444444", "fernandez", "mari@uleam.edu", "mari123")
carlitos = sistema.crear_docente("carlitos", "666666666", "sanchez", "carlitos@uleam.edu", "carlitos123")

laura = sistema.crear_estudiante("laura", "888888888", "torres", "laura@uleam.edu", "laura123")
jorge = sistema.crear_estudiante("jorge", "999999999", "flores", "jorge@uleam.edu", "jorge123")
marta = sistema.crear_estudiante("marta", "101010101", "diaz", "marta@uleam.edu", "marta123")
roberto = sistema.crear_estudiante("roberto", "121212121", "vega", "roberto@uleam.edu", "roberto123")

# Crear carreras
carrera_uno = sistema.crear_carrera(1, "Ciencias de la vida", "software1", "presencial")
carrera_dos = sistema.crear_carrera(2, "Ciencias de la vida", "software2", "presencial")
carrera_tres = sistema.crear_carrera(3, "tecnologia", "ti", "virtual")

# Crear materias
materia_moo = sistema.crear_asignatura("moo", "Moo123", 4, 5, "Presencial")
materia_poo = sistema.crear_asignatura("poo", "Poo123", 4, 5, "Presencial")
materia_bd = sistema.crear_asignatura("basede datos", "bd123", 4, 4, "Presencial")
materia_redes = sistema.crear_asignatura("redes", "red123", 3, 3, "Virtual")
materia_estructuras = sistema.crear_asignatura("estructuras", "ed145", 4, 5, "Presencial")
materia_sistemas = sistema.crear_asignatura("sistemas", "s333", 3, 3, "Virtual")

# Crear cursos
curso_a = sistema.crear_curso("Tercero")
curso_b = sistema.crear_curso("Cuarto")
curso_c = sistema.crear_curso("Quinto")

# Configurar curso A
sistema.agregar_materia_a_curso(curso_a, materia_poo, 3)
sistema.asignar_docente_a_materia(curso_a, pepito, materia_poo)
sistema.agregar_materia_a_curso(curso_a, materia_moo, 2)
sistema.asignar_docente_a_materia(curso_a, juanito, materia_moo)  # <--- CORREGIDO
sistema.agregar_materia_a_curso(curso_a, materia_bd, 3)
sistema.asignar_docente_a_materia(curso_a, changuin, materia_bd)
sistema.agregar_materia_a_curso(curso_a, materia_redes, 2)
sistema.asignar_docente_a_materia(curso_a, mari, materia_redes)
sistema.agregar_materia_a_curso(curso_a, materia_estructuras, 2)
sistema.asignar_docente_a_materia(curso_a, carlitos, materia_estructuras)

print(curso_a.materias)

# Configurar curso B
sistema.agregar_materia_a_curso(curso_b, materia_poo, 3)
sistema.asignar_docente_a_materia(curso_b, pepito, materia_poo)
sistema.agregar_materia_a_curso(curso_b, materia_moo, 2)
sistema.asignar_docente_a_materia(curso_b, juanito, materia_moo)
sistema.agregar_materia_a_curso(curso_b, materia_bd, 3)
sistema.asignar_docente_a_materia(curso_b, changuin, materia_bd)
sistema.agregar_materia_a_curso(curso_b, materia_redes, 2)
sistema.asignar_docente_a_materia(curso_b, mari, materia_redes)
sistema.agregar_materia_a_curso(curso_b, materia_estructuras, 2)
sistema.asignar_docente_a_materia(curso_b, carlitos, materia_estructuras)

print(curso_b.materias)

# Configurar curso C
sistema.agregar_materia_a_curso(curso_c, materia_poo, 3)
sistema.asignar_docente_a_materia(curso_c, pepito, materia_poo)
sistema.agregar_materia_a_curso(curso_c, materia_moo, 2)
sistema.asignar_docente_a_materia(curso_c, juanito, materia_moo)
sistema.agregar_materia_a_curso(curso_c, materia_bd, 3)
sistema.asignar_docente_a_materia(curso_c, changuin, materia_bd)
sistema.agregar_materia_a_curso(curso_c, materia_redes, 2)
sistema.asignar_docente_a_materia(curso_c, mari, materia_redes)
sistema.agregar_materia_a_curso(curso_c, materia_estructuras, 2)
sistema.asignar_docente_a_materia(curso_c, carlitos, materia_estructuras)

cursos = [curso_a, curso_b, curso_c]

# Guardar horarios de docentes
datos.guardar_horario_docente(pepito, cursos)
datos.guardar_horario_docente(juanito, cursos)
datos.guardar_horario_docente(changuin, cursos)
datos.guardar_horario_docente(mari, cursos)
datos.guardar_horario_docente(carlitos, cursos)

# Crear paralelos
paralelo_a1 = datos.crear_horario_paralelo(curso_a, "Tercero_A")
paralelo_b1 = datos.crear_horario_paralelo(curso_a, "Tercero_B")
paralelo_c1 = datos.crear_horario_paralelo(curso_a, "Tercero_C")

paralelo_a2 = datos.crear_horario_paralelo(curso_b, "Cuarto_A")
paralelo_b2 = datos.crear_horario_paralelo(curso_b, "Cuarto_B")
paralelo_c2 = datos.crear_horario_paralelo(curso_b, "Cuarto_C")

paralelo_a3 = datos.crear_horario_paralelo(curso_c, "Quinto_A")
paralelo_b3 = datos.crear_horario_paralelo(curso_c, "Quinto_B")
paralelo_c3 = datos.crear_horario_paralelo(curso_c, "Quinto_C")

# Mostrar horarios
datos.mostrar_horario_paralelo(paralelo_a1)
datos.mostrar_horario_paralelo(paralelo_b1)
datos.mostrar_horario_paralelo(paralelo_c1)

# Inscribir estudiante
sistema.inscribir_estudiante_en_paralelo(paralelo_a1, laura)
sistema.inscribir_estudiante_en_paralelo(paralelo_a1, pepito)

# Verificar que el estudiante se inscribió correctamente
print(f"\nEstudiantes en {paralelo_a1.nombre}:")
for est in paralelo_a1.estudiantes:
    print(f"- {est.nombre} (Cédula: {est.cedula})")
    
    
tutoria_poo = sistema.crear_tutoria(1, "2026-06-20", materia_poo, ["pedro", "laura"])
tutoria_bd = sistema.crear_tutoria(2, "2026-06-21", materia_bd, ["jorge", "marta", "roberto"])
tutoria_estructuras = sistema.crear_tutoria(3, "2026-06-22", materia_estructuras, ["pedro", "marta"])

