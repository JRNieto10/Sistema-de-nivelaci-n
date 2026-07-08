from facade import FacadeSistemaAcademico
from facade_datos import FacadeDatos

sistema = FacadeSistemaAcademico()
datos = FacadeDatos()

print("=" * 60)
print("PRUEBA COMPLETA DE TODOS LOS METODOS DE LAS FACHADAS")
print("=" * 60)

print("\n1. GESTION DE PERMITIDOS")
print("-" * 40)

cedulas_estudiantes = ["77777777", "888888888", "999999999", "101010101", "121212121"]
cedulas_docentes = ["111111111", "222222222", "333333333", "444444444", "666666666"]
cedulas_personal = ["123456789", "987654321", "555555555"]

for cedula in cedulas_estudiantes:
    resultado = datos.agregar_cedula_permitida(cedula, "estudiante")
    print(f"Agregar estudiante {cedula}: {resultado}")

for cedula in cedulas_docentes:
    resultado = datos.agregar_cedula_permitida(cedula, "docente")
    print(f"Agregar docente {cedula}: {resultado}")

for cedula in cedulas_personal:
    resultado = datos.agregar_cedula_permitida(cedula, "personal")
    print(f"Agregar personal {cedula}: {resultado}")

print("\nLista de cedulas permitidas:")
cedulas_lista = datos.listar_cedulas()
print(f"  Estudiantes: {cedulas_lista.get('cedulas_estudiantes', [])}")
print(f"  Docentes: {cedulas_lista.get('cedulas_docentes', [])}")
print(f"  Personal: {cedulas_lista.get('cedulas_personal', [])}")

print("\nVerificando cedulas:")
print(f"  ?77777777 es valida? {datos.verificar_cedula('77777777')}")
print(f"  ?999999999 es valida? {datos.verificar_cedula('999999999')}")
print(f"  ?000000000 es valida? {datos.verificar_cedula('000000000')}")

print("\nEliminando cedula 77777777...")
resultado_eliminar = datos.eliminar_cedula_permitida("77777777", "estudiante")
print(f"  Resultado: {resultado_eliminar}")
print(f"  ?77777777 sigue valida? {datos.verificar_cedula('77777777')}")

datos.agregar_cedula_permitida("77777777", "estudiante")

print("\n2. CREACION DE USUARIOS")
print("-" * 40)

david = sistema.crear_administrador("david", "987654321", "apellido", "david@uleam.edu", "admin321")
josue = sistema.crear_administrador("josue", "123456789", "apellido", "josue@uleam.edu", "admin123")
jessica = sistema.crear_administrador("jessica", "555555555", "apellido", "jessica@uleam.edu", "admin132")
print("Administradores creados")

pepito = sistema.crear_docente("pepito", "111111111", "garcia", "pepito@uleam.edu", "pepito123")
juanito = sistema.crear_docente("juanito", "222222222", "lopez1", "juanito@uleam.edu", "juanito123")
changuin = sistema.crear_docente("changuin", "333333333", "lopez2", "changuin@uleam.edu", "changuin123")
mari = sistema.crear_docente("mari", "444444444", "fernandez", "mari@uleam.edu", "mari123")
carlitos = sistema.crear_docente("carlitos", "666666666", "sanchez", "carlitos@uleam.edu", "carlitos123")
print("Docentes creados")

laura = sistema.crear_estudiante("laura", "888888888", "torres", "laura@uleam.edu", "laura123")
jorge = sistema.crear_estudiante("jorge", "999999999", "flores", "jorge@uleam.edu", "jorge123")
marta = sistema.crear_estudiante("marta", "101010101", "diaz", "marta@uleam.edu", "marta123")
roberto = sistema.crear_estudiante("roberto", "121212121", "vega", "roberto@uleam.edu", "roberto123")
print("Estudiantes creados")

print("\nProbando _registrar_usuario (metodo interno):")
resultado_registro, mensaje = sistema._registrar_usuario(
    "pedro", "77777777", "perez", "pedro@uleam.edu", "pedro123", "estudiante"
)
print(f"  Registro: {resultado_registro}, Mensaje: {mensaje}")

print("\n3. VERIFICACION DE USUARIOS")
print("-" * 40)

print(f"  ?Estudiante 888888888 existe? {datos.verificar_estudiante_existe('888888888')}")
print(f"  ?Docente 111111111 existe? {datos.verificar_docente_existe('111111111')}")
print(f"  ?Personal 987654321 existe? {datos.verificar_personal_existe('987654321')}")
print(f"  ?Usuario 999999999 (estudiante) existe? {datos.verificar_usuario_existe('999999999', 'estudiante')}")
print(f"  ?Usuario 222222222 (docente) existe? {datos.verificar_usuario_existe('222222222', 'docente')}")

print("\nObteniendo usuarios por cedula:")
estudiante_obtenido = datos.obtener_estudiante("888888888")
print(f"  Estudiante: {estudiante_obtenido}")
docente_obtenido = datos.obtener_docente("111111111")
print(f"  Docente: {docente_obtenido}")
personal_obtenido = datos.obtener_personal("987654321")
print(f"  Personal: {personal_obtenido}")

usuario_obtenido = datos.obtener_usuario_por_cedula("888888888", "estudiante")
print(f"  Usuario por rol: {usuario_obtenido}")

print("\n4. CREACION DE CARRERAS")
print("-" * 40)

carrera_uno, msg1 = sistema.crear_carrera(1, "Ciencias de la vida", "software1", "presencial")
carrera_dos, msg2 = sistema.crear_carrera(2, "Ciencias de la vida", "software2", "presencial")
carrera_tres, msg3 = sistema.crear_carrera(3, "tecnologia", "ti", "virtual")
print(f"  Carrera 1: {msg1}")
print(f"  Carrera 2: {msg2}")
print(f"  Carrera 3: {msg3}")

carrera_duplicada, msg_dup = sistema.crear_carrera(1, "Duplicada", "duplicada", "presencial")
print(f"  Intento duplicado: {msg_dup}")

print("\nTodas las carreras:")
for c in sistema.obtener_todas_carreras():
    print(f"  - ID: {c.id}, Nombre: {c.nombre}, Area: {c.area}")

carrera_encontrada = sistema.obtener_carrera_por_id(1)
print(f"\nCarrera encontrada ID 1: {carrera_encontrada.nombre if carrera_encontrada else 'No encontrada'}")

print("\n5. CREACION DE ASIGNATURAS")
print("-" * 40)

materia_moo = sistema.crear_asignatura("moo", "Moo123", 4, 5, "Presencial")
materia_poo = sistema.crear_asignatura("poo", "Poo123", 4, 5, "Presencial")
materia_bd = sistema.crear_asignatura("basede datos", "bd123", 4, 4, "Presencial")
materia_redes = sistema.crear_asignatura("redes", "red123", 3, 3, "Virtual")
materia_estructuras = sistema.crear_asignatura("estructuras", "ed145", 4, 5, "Presencial")
materia_sistemas = sistema.crear_asignatura("sistemas", "s333", 3, 3, "Virtual")
print("Asignaturas creadas")

print("\nAgregando asignaturas a carreras:")
resultado_add = sistema.agregar_asignatura_a_carrera(1, materia_poo)
print(f"  Agregar POO a carrera 1: {resultado_add}")
resultado_add2 = sistema.agregar_asignatura_a_carrera(1, materia_moo)
print(f"  Agregar MOO a carrera 1: {resultado_add2}")

asignaturas = sistema.obtener_asignaturas_carrera(1)
print(f"\nAsignaturas de carrera 1:")
for asig in asignaturas:
    print(f"  - {asig.nombre} ({asig.codigo})")

print("\n6. CREACION DE CURSOS")
print("-" * 40)

curso_a = sistema.crear_curso("Tercero")
curso_b = sistema.crear_curso("Cuarto")
curso_c = sistema.crear_curso("Quinto")
print("Cursos creados")

print(f"Cursos en memoria: {[c.nombre for c in sistema.lista_cursos]}")

print("\n7. CONFIGURACION DE CURSOS")
print("-" * 40)

sistema.agregar_materia_a_curso(curso_a, materia_poo, 3)
sistema.asignar_docente_a_materia(curso_a, pepito, materia_poo)
sistema.agregar_materia_a_curso(curso_a, materia_moo, 2)
sistema.asignar_docente_a_materia(curso_a, juanito, materia_moo)
sistema.agregar_materia_a_curso(curso_a, materia_bd, 3)
sistema.asignar_docente_a_materia(curso_a, changuin, materia_bd)
sistema.agregar_materia_a_curso(curso_a, materia_redes, 2)
sistema.asignar_docente_a_materia(curso_a, mari, materia_redes)
sistema.agregar_materia_a_curso(curso_a, materia_estructuras, 2)
sistema.asignar_docente_a_materia(curso_a, carlitos, materia_estructuras)
print("Curso A configurado")

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
print("Curso B configurado")

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
print("Curso C configurado")

cursos = [curso_a, curso_b, curso_c]

materias_a = [m.nombre if hasattr(m, 'nombre') else m for m in curso_a.materias]
materias_b = [m.nombre if hasattr(m, 'nombre') else m for m in curso_b.materias]
materias_c = [m.nombre if hasattr(m, 'nombre') else m for m in curso_c.materias]
print(f"\nMaterias curso A: {materias_a}")
print(f"Materias curso B: {materias_b}")
print(f"Materias curso C: {materias_c}")

print("\n8. GUARDADO DE CURSOS")
print("-" * 40)

materias_con_docentes_dict = {}
for materia in curso_a.materias:
    nombre_materia = materia.nombre if hasattr(materia, 'nombre') else str(materia)
    materias_con_docentes_dict[nombre_materia] = ["pepito"]

resultado_guardar_curso = datos.guardar_curso("software1", "Tercero", materias_con_docentes_dict)
print(f"  Guardar curso: {resultado_guardar_curso}")

curso_cargado = datos.cargar_curso("software1", "Tercero")
print(f"  Curso cargado: {curso_cargado}")

print("\n9. GUARDADO DE HORARIOS")
print("-" * 40)

print("Guardando horarios de docentes:")
datos.guardar_horario_docente(pepito, cursos)
datos.guardar_horario_docente(juanito, cursos)
datos.guardar_horario_docente(changuin, cursos)
datos.guardar_horario_docente(mari, cursos)
datos.guardar_horario_docente(carlitos, cursos)
print("Horarios guardados")

print("\n10. CREACION DE PARALELOS")
print("-" * 40)

paralelo_a1 = datos.crear_horario_paralelo(curso_a, "Tercero_A")
paralelo_b1 = datos.crear_horario_paralelo(curso_a, "Tercero_B")
paralelo_c1 = datos.crear_horario_paralelo(curso_a, "Tercero_C")
paralelo_a2 = datos.crear_horario_paralelo(curso_b, "Cuarto_A")
paralelo_b2 = datos.crear_horario_paralelo(curso_b, "Cuarto_B")
paralelo_c2 = datos.crear_horario_paralelo(curso_b, "Cuarto_C")
paralelo_a3 = datos.crear_horario_paralelo(curso_c, "Quinto_A")
paralelo_b3 = datos.crear_horario_paralelo(curso_c, "Quinto_B")
paralelo_c3 = datos.crear_horario_paralelo(curso_c, "Quinto_C")
print("Paralelos creados")

print("\nGuardando paralelos:")
paralelos_data = [
    {"letra": "A", "aula": "101", "horario": "Lunes 8-10", "materias": []},
    {"letra": "B", "aula": "102", "horario": "Martes 8-10", "materias": []}
]
resultado_guardar_paralelos = datos.guardar_paralelos("software1", "Tercero", paralelos_data)
print(f"  Resultado: {resultado_guardar_paralelos}")

print("\nTodos los paralelos:")
datos.mostrar_todos_los_paralelos()

print("\n11. MOSTRAR HORARIOS")
print("-" * 40)

print("Horario de Tercero_A:")
try:
    datos.mostrar_horario_paralelo(paralelo_a1)
except Exception as e:
    print(f"  Nota: {e}")

print("\nHorario de pepito:")
datos.mostrar_horario_docente(pepito)

print("\n12. INSCRIPCION DE ESTUDIANTES")
print("-" * 40)

sistema.inscribir_estudiante_en_paralelo(paralelo_a1, laura)
sistema.inscribir_estudiante_en_paralelo(paralelo_a1, jorge)
sistema.inscribir_estudiante_en_paralelo(paralelo_b1, marta)
sistema.inscribir_estudiante_en_paralelo(paralelo_c1, roberto)
print("Estudiantes inscritos")

print(f"\nEstudiantes en Tercero_A:")
if hasattr(paralelo_a1, 'estudiantes'):
    for est in paralelo_a1.estudiantes:
        print(f"  - {est.nombre} (Cedula: {est.cedula})")

print(f"\nEstudiantes en Tercero_B:")
if hasattr(paralelo_b1, 'estudiantes'):
    for est in paralelo_b1.estudiantes:
        print(f"  - {est.nombre} (Cedula: {est.cedula})")

print("\n13. GESTION DE MATRICULAS")
print("-" * 40)

datos_estudiante = {
    "cedula": "888888888",
    "nombre": "laura",
    "apellido": "torres",
    "carrera": "software1",
    "paralelo": "Tercero_A",
    "materias_inscritas": ["poo", "moo", "bd"]
}
datos.guardar_estado_matricula(datos_estudiante)
print("Matricula guardada")

matricula_cargada = datos.cargar_estado_matricula("888888888")
print(f"Matricula cargada: {matricula_cargada}")

print("\n14. CARGA DE DATOS")
print("-" * 40)

docentes_json = datos.cargar_docentes_desde_json()
print(f"  Docentes en JSON: {len(docentes_json)}")
estudiantes_json = datos.cargar_estudiantes_desde_json()
print(f"  Estudiantes en JSON: {len(estudiantes_json)}")
personal_json = datos.cargar_personal_desde_json()
print(f"  Personal en JSON: {len(personal_json)}")

print("\n15. BUSQUEDA DE PARALELOS")
print("-" * 40)

print(f"  ?Carrera 'software1' existe? {datos.carrera_existe('software1')}")
print(f"  ?Carrera 'inexistente' existe? {datos.carrera_existe('inexistente')}")

paralelos_encontrados = datos.buscar_paralelos("software1")
print(f"\nParalelos encontrados en software1:")
for p in paralelos_encontrados:
    print(f"  - {p['nombre']}")

print("\n16. CREACION DE TUTORIAS")
print("-" * 40)

tutoria_poo = sistema.crear_tutoria(1, "2026-06-20", materia_poo, ["pedro", "laura"])
tutoria_bd = sistema.crear_tutoria(2, "2026-06-21", materia_bd, ["jorge", "marta", "roberto"])
tutoria_estructuras = sistema.crear_tutoria(3, "2026-06-22", materia_estructuras, ["pedro", "marta"])
print("Tutorias creadas")

print(f"\nTutorias en memoria: {len(sistema.lista_tutorias)}")

print("\n17. ELIMINACION DE CARRERAS")
print("-" * 40)

print("Eliminando carrera ID 3...")
resultado_eliminar_carrera = sistema.eliminar_carrera(3)
print(f"  Resultado: {resultado_eliminar_carrera}")

carreras_restantes = sistema.obtener_todas_carreras()
print(f"Carreras restantes: {[c.id for c in carreras_restantes]}")

print("\n18. COMPROBACION DE DUPLICADOS")
print("-" * 40)

print(f"  ?Cedula 888888888 como estudiante esta duplicada? {datos.comprobar_duplicados('888888888', 'estudiante')}")
print(f"  ?Cedula 999999999 como estudiante esta duplicada? {datos.comprobar_duplicados('999999999', 'estudiante')}")

print("\n19. VERIFICACION DE ASIGNATURAS")
print("-" * 40)

print(f"  POO: {materia_poo.nombre}, Creditos: {materia_poo.creditos}, Horas: {materia_poo.horas}")
print(f"  MOO: {materia_moo.nombre}, Creditos: {materia_moo.creditos}, Horas: {materia_moo.horas}")
print(f"  Base de Datos: {materia_bd.nombre}, Creditos: {materia_bd.creditos}, Horas: {materia_bd.horas}")

print("\n20. ACCESO A ATRIBUTOS DE LA FACHADA")
print("-" * 40)

print(f"  lista_cursos: {len(sistema.lista_cursos)} cursos")
print(f"  lista_materias: {len(sistema.lista_materias)} materias")
print(f"  lista_usuarios: {len(sistema.lista_usuarios)} usuarios")
print(f"  lista_paralelos (facade): {len(sistema.lista_paralelos)} paralelos")
print(f"  lista_paralelos (datos): {len(datos.lista_paralelos)} paralelos")

print("\n" + "=" * 60)
print("RESUMEN DE EJECUCION COMPLETA")
print("=" * 60)
print(f"Usuarios creados: {len(sistema.lista_usuarios)}")
print(f"Carreras creadas: {len(sistema.lista_carreras)}")
print(f"Asignaturas creadas: {len(sistema.lista_materias)}")
print(f"Cursos creados: {len(sistema.lista_cursos)}")
print(f"Paralelos creados: {len(datos.lista_paralelos)}")
print(f"Tutorias creadas: {len(sistema.lista_tutorias)}")
print("=" * 60)
print("PRUEBA COMPLETA FINALIZADA")



