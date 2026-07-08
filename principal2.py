from facade import FacadeSistemaAcademico
from facade_datos import FacadeDatos

sistema = FacadeSistemaAcademico()
datos = FacadeDatos()

print("\nCREANDO DOCENTES Y ESTUDIANTES BASE")
print("-" * 40)

cedulas_docentes = ["111111111", "222222222", "333333333", "444444444", "666666666"]
for cedula in cedulas_docentes:
    datos.agregar_cedula_permitida(cedula, "docente")

cedulas_estudiantes = ["888888888", "999999999", "101010101", "121212121", "131313131", "141414141", "151515151", "161616161", "171717171"]
for cedula in cedulas_estudiantes:
    datos.agregar_cedula_permitida(cedula, "estudiante")

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

estudiantes_extra = [
    sistema.crear_estudiante("ana", "131313131", "martinez", "ana@uleam.edu", "ana123"),
    sistema.crear_estudiante("luis", "141414141", "gonzalez", "luis@uleam.edu", "luis123"),
    sistema.crear_estudiante("carla", "151515151", "ramirez", "carla@uleam.edu", "carla123"),
    sistema.crear_estudiante("pedro2", "161616161", "morales", "pedro2@uleam.edu", "pedro123"),
    sistema.crear_estudiante("maria", "171717171", "ortiz", "maria@uleam.edu", "maria123")
]
print("Estudiantes extra creados")

print("\n21. CREACION DE NUEVA CARRERA")
print("-" * 40)

carrera_cuatro, msg4 = sistema.crear_carrera(4, "Ingenieria", "sistemas", "presencial")
carrera_cinco, msg5 = sistema.crear_carrera(5, "Administracion", "administracion", "virtual")
print(f"  Carrera 4: {msg4}")
print(f"  Carrera 5: {msg5}")

print("\n22. CREACION DE ASIGNATURAS PARA NUEVAS CARRERAS")
print("-" * 40)

materia_programacion = sistema.crear_asignatura("programacion", "prog123", 5, 6, "Presencial")
materia_algebra = sistema.crear_asignatura("algebra", "alg123", 4, 5, "Presencial")
materia_calculo = sistema.crear_asignatura("calculo", "cal123", 4, 5, "Presencial")
materia_fisica = sistema.crear_asignatura("fisica", "fis123", 3, 4, "Presencial")
materia_estadistica = sistema.crear_asignatura("estadistica", "est123", 3, 3, "Virtual")
materia_contabilidad = sistema.crear_asignatura("contabilidad", "con123", 4, 4, "Virtual")
materia_administracion = sistema.crear_asignatura("administracion", "adm123", 3, 3, "Virtual")
materia_marketing = sistema.crear_asignatura("marketing", "mar123", 3, 3, "Virtual")
print("Asignaturas para nuevas carreras creadas")

sistema.agregar_asignatura_a_carrera(4, materia_programacion)
sistema.agregar_asignatura_a_carrera(4, materia_algebra)
sistema.agregar_asignatura_a_carrera(4, materia_calculo)
sistema.agregar_asignatura_a_carrera(4, materia_fisica)
sistema.agregar_asignatura_a_carrera(5, materia_estadistica)
sistema.agregar_asignatura_a_carrera(5, materia_contabilidad)
sistema.agregar_asignatura_a_carrera(5, materia_administracion)
sistema.agregar_asignatura_a_carrera(5, materia_marketing)
print("Asignaturas agregadas a carreras")

print("\n23. CREACION DE CURSOS PARA CARRERA 4")
print("-" * 40)

curso_d = sistema.crear_curso("Primero")
curso_e = sistema.crear_curso("Segundo")
curso_f = sistema.crear_curso("Tercero")
print("Cursos creados para carrera 4")

print("\n24. CONFIGURACION DEL CURSO D (Primero)")
print("-" * 40)

sistema.agregar_materia_a_curso(curso_d, materia_programacion, 4)
sistema.asignar_docente_a_materia(curso_d, pepito, materia_programacion)
sistema.agregar_materia_a_curso(curso_d, materia_algebra, 3)
sistema.asignar_docente_a_materia(curso_d, juanito, materia_algebra)
sistema.agregar_materia_a_curso(curso_d, materia_calculo, 3)
sistema.asignar_docente_a_materia(curso_d, changuin, materia_calculo)
print("Curso D configurado")

print("\n25. CONFIGURACION DEL CURSO E (Segundo)")
print("-" * 40)

sistema.agregar_materia_a_curso(curso_e, materia_programacion, 4)
sistema.asignar_docente_a_materia(curso_e, pepito, materia_programacion)
sistema.agregar_materia_a_curso(curso_e, materia_fisica, 3)
sistema.asignar_docente_a_materia(curso_e, mari, materia_fisica)
sistema.agregar_materia_a_curso(curso_e, materia_estadistica, 3)
sistema.asignar_docente_a_materia(curso_e, carlitos, materia_estadistica)
print("Curso E configurado")

print("\n26. CONFIGURACION DEL CURSO F (Tercero)")
print("-" * 40)

sistema.agregar_materia_a_curso(curso_f, materia_calculo, 4)
sistema.asignar_docente_a_materia(curso_f, changuin, materia_calculo)
sistema.agregar_materia_a_curso(curso_f, materia_estadistica, 3)
sistema.asignar_docente_a_materia(curso_f, carlitos, materia_estadistica)
sistema.agregar_materia_a_curso(curso_f, materia_administracion, 3)
sistema.asignar_docente_a_materia(curso_f, mari, materia_administracion)
print("Curso F configurado")

print("\n27. CREACION DE PARALELOS PARA CURSOS DE CARRERA 4")
print("-" * 40)

paralelo_d1 = datos.crear_horario_paralelo(curso_d, "Primero_A")
paralelo_d2 = datos.crear_horario_paralelo(curso_d, "Primero_B")
paralelo_d3 = datos.crear_horario_paralelo(curso_d, "Primero_C")
paralelo_e1 = datos.crear_horario_paralelo(curso_e, "Segundo_A")
paralelo_e2 = datos.crear_horario_paralelo(curso_e, "Segundo_B")
paralelo_f1 = datos.crear_horario_paralelo(curso_f, "Tercero_A")
paralelo_f2 = datos.crear_horario_paralelo(curso_f, "Tercero_B")
print("Paralelos para carrera 4 creados")

print("\n28. CREACION DE CURSOS PARA CARRERA 5 (Administracion)")
print("-" * 40)

curso_g = sistema.crear_curso("Primero")
curso_h = sistema.crear_curso("Segundo")
curso_i = sistema.crear_curso("Tercero")
print("Cursos creados para carrera 5")

print("\n29. CONFIGURACION DEL CURSO G (Primero Administracion)")
print("-" * 40)

sistema.agregar_materia_a_curso(curso_g, materia_administracion, 3)
sistema.asignar_docente_a_materia(curso_g, mari, materia_administracion)
sistema.agregar_materia_a_curso(curso_g, materia_contabilidad, 3)
sistema.asignar_docente_a_materia(curso_g, juanito, materia_contabilidad)
sistema.agregar_materia_a_curso(curso_g, materia_estadistica, 3)
sistema.asignar_docente_a_materia(curso_g, carlitos, materia_estadistica)
print("Curso G configurado")

print("\n30. CONFIGURACION DEL CURSO H (Segundo Administracion)")
print("-" * 40)

sistema.agregar_materia_a_curso(curso_h, materia_administracion, 3)
sistema.asignar_docente_a_materia(curso_h, mari, materia_administracion)
sistema.agregar_materia_a_curso(curso_h, materia_marketing, 3)
sistema.asignar_docente_a_materia(curso_h, pepito, materia_marketing)
sistema.agregar_materia_a_curso(curso_h, materia_contabilidad, 3)
sistema.asignar_docente_a_materia(curso_h, juanito, materia_contabilidad)
print("Curso H configurado")

print("\n31. CONFIGURACION DEL CURSO I (Tercero Administracion)")
print("-" * 40)

sistema.agregar_materia_a_curso(curso_i, materia_marketing, 3)
sistema.asignar_docente_a_materia(curso_i, pepito, materia_marketing)
sistema.agregar_materia_a_curso(curso_i, materia_estadistica, 3)
sistema.asignar_docente_a_materia(curso_i, carlitos, materia_estadistica)
sistema.agregar_materia_a_curso(curso_i, materia_administracion, 3)
sistema.asignar_docente_a_materia(curso_i, mari, materia_administracion)
print("Curso I configurado")

print("\n32. CREACION DE PARALELOS PARA CURSOS DE CARRERA 5")
print("-" * 40)

paralelo_g1 = datos.crear_horario_paralelo(curso_g, "Primero_A")
paralelo_g2 = datos.crear_horario_paralelo(curso_g, "Primero_B")
paralelo_h1 = datos.crear_horario_paralelo(curso_h, "Segundo_A")
paralelo_h2 = datos.crear_horario_paralelo(curso_h, "Segundo_B")
paralelo_i1 = datos.crear_horario_paralelo(curso_i, "Tercero_A")
paralelo_i2 = datos.crear_horario_paralelo(curso_i, "Tercero_B")
print("Paralelos para carrera 5 creados")

print("\n33. INSCRIPCION DE ESTUDIANTES EN NUEVOS PARALELOS")
print("-" * 40)

sistema.inscribir_estudiante_en_paralelo(paralelo_d1, laura)
sistema.inscribir_estudiante_en_paralelo(paralelo_d1, jorge)
sistema.inscribir_estudiante_en_paralelo(paralelo_d2, marta)
sistema.inscribir_estudiante_en_paralelo(paralelo_d3, roberto)

for est in estudiantes_extra[:3]:
    sistema.inscribir_estudiante_en_paralelo(paralelo_e1, est)

sistema.inscribir_estudiante_en_paralelo(paralelo_g1, estudiantes_extra[3])
sistema.inscribir_estudiante_en_paralelo(paralelo_g1, estudiantes_extra[4])
print("Estudiantes inscritos en nuevos paralelos")

print("\n34. VERIFICACION DE INSCRIPCIONES")
print("-" * 40)

print(f"Estudiantes en Primero_A: {len(paralelo_d1.estudiantes) if hasattr(paralelo_d1, 'estudiantes') else 0}")
print(f"Estudiantes en Primero_B: {len(paralelo_d2.estudiantes) if hasattr(paralelo_d2, 'estudiantes') else 0}")
print(f"Estudiantes en Primero_C: {len(paralelo_d3.estudiantes) if hasattr(paralelo_d3, 'estudiantes') else 0}")
print(f"Estudiantes en Segundo_A: {len(paralelo_e1.estudiantes) if hasattr(paralelo_e1, 'estudiantes') else 0}")
print(f"Estudiantes en Primero_A (Adm): {len(paralelo_g1.estudiantes) if hasattr(paralelo_g1, 'estudiantes') else 0}")

print("\n35. GUARDADO DE CURSOS ADICIONALES")
print("-" * 40)

materias_dict_d = {}
for materia in curso_d.materias:
    nombre = materia.nombre if hasattr(materia, 'nombre') else str(materia)
    materias_dict_d[nombre] = ["pepito"]
datos.guardar_curso("sistemas", "Primero", materias_dict_d)

materias_dict_e = {}
for materia in curso_e.materias:
    nombre = materia.nombre if hasattr(materia, 'nombre') else str(materia)
    materias_dict_e[nombre] = ["pepito"]
datos.guardar_curso("sistemas", "Segundo", materias_dict_e)

materias_dict_g = {}
for materia in curso_g.materias:
    nombre = materia.nombre if hasattr(materia, 'nombre') else str(materia)
    materias_dict_g[nombre] = ["mari"]
datos.guardar_curso("administracion", "Primero", materias_dict_g)
print("Cursos adicionales guardados")

print("\n36. GUARDADO DE PARALELOS ADICIONALES")
print("-" * 40)

paralelos_sistemas = [
    {"letra": "A", "aula": "201", "horario": "Lunes 8-10", "materias": []},
    {"letra": "B", "aula": "202", "horario": "Martes 8-10", "materias": []},
    {"letra": "C", "aula": "203", "horario": "Miercoles 8-10", "materias": []}
]
datos.guardar_paralelos("sistemas", "Primero", paralelos_sistemas)

paralelos_adm = [
    {"letra": "A", "aula": "301", "horario": "Jueves 8-10", "materias": []},
    {"letra": "B", "aula": "302", "horario": "Viernes 8-10", "materias": []}
]
datos.guardar_paralelos("administracion", "Primero", paralelos_adm)
print("Paralelos adicionales guardados")

print("\n37. GUARDADO DE HORARIOS DE NUEVOS DOCENTES")
print("-" * 40)

cursos_nuevos = [curso_d, curso_e, curso_f, curso_g, curso_h, curso_i]
datos.guardar_horario_docente(pepito, cursos_nuevos)
datos.guardar_horario_docente(juanito, cursos_nuevos)
datos.guardar_horario_docente(changuin, cursos_nuevos)
datos.guardar_horario_docente(mari, cursos_nuevos)
datos.guardar_horario_docente(carlitos, cursos_nuevos)
print("Horarios de nuevos cursos guardados")

print("\n38. CREACION DE TUTORIAS ADICIONALES")
print("-" * 40)

tutoria_prog = sistema.crear_tutoria(4, "2026-06-23", materia_programacion, ["laura", "jorge", "marta"])
tutoria_algebra = sistema.crear_tutoria(5, "2026-06-24", materia_algebra, ["roberto", "ana", "luis"])
tutoria_calculo = sistema.crear_tutoria(6, "2026-06-25", materia_calculo, ["carla", "pedro2"])
tutoria_adm = sistema.crear_tutoria(7, "2026-06-26", materia_administracion, ["maria", "jorge"])
tutoria_marketing = sistema.crear_tutoria(8, "2026-06-27", materia_marketing, ["laura", "roberto"])
print("Tutorias adicionales creadas")

print(f"Total tutorias: {len(sistema.lista_tutorias)}")

print("\n39. ELIMINACION DE CEDULAS PERMITIDAS ADICIONALES")
print("-" * 40)

print("Eliminando cedulas 131313131 y 141414141...")
datos.eliminar_cedula_permitida("131313131", "estudiante")
datos.eliminar_cedula_permitida("141414141", "estudiante")
print(f"  ?131313131 valida? {datos.verificar_cedula('131313131')}")
print(f"  ?141414141 valida? {datos.verificar_cedula('141414141')}")

print("\n40. BUSQUEDA DE PARALELOS EN NUEVAS CARRERAS")
print("-" * 40)

paralelos_sistemas = datos.buscar_paralelos("sistemas")
print(f"Paralelos en sistemas: {len(paralelos_sistemas)}")
for p in paralelos_sistemas[:5]:
    print(f"  - {p['nombre']}")

paralelos_adm = datos.buscar_paralelos("administracion")
print(f"Paralelos en administracion: {len(paralelos_adm)}")
for p in paralelos_adm:
    print(f"  - {p['nombre']}")

print("\n41. VERIFICACION DE EXISTENCIA DE USUARIOS EN NUEVAS CARRERAS")
print("-" * 40)

print(f"  ?Estudiante 131313131 existe? {datos.verificar_estudiante_existe('131313131')}")
print(f"  ?Estudiante 151515151 existe? {datos.verificar_estudiante_existe('151515151')}")
print(f"  ?Docente 111111111 existe? {datos.verificar_docente_existe('111111111')}")

print("\n42. VERIFICACION DE CARRERAS ADICIONALES")
print("-" * 40)

print(f"  ?Carrera 'sistemas' existe? {datos.carrera_existe('sistemas')}")
print(f"  ?Carrera 'administracion' existe? {datos.carrera_existe('administracion')}")

carrera_sistemas = sistema.obtener_carrera_por_id(4)
if carrera_sistemas:
    print(f"  Carrera sistemas: ID={carrera_sistemas.id}, Nombre={carrera_sistemas.nombre}")

carrera_adm = sistema.obtener_carrera_por_id(5)
if carrera_adm:
    print(f"  Carrera administracion: ID={carrera_adm.id}, Nombre={carrera_adm.nombre}")

print("\n43. MOSTRAR TODOS LOS PARALELOS CREADOS")
print("-" * 40)

print("Lista completa de paralelos:")
for i, p in enumerate(datos.lista_paralelos):
    nombre = p.nombre if hasattr(p, 'nombre') else str(p)
    print(f"  {i+1}. {nombre}")

print("\n44. RESUMEN DE NUEVAS CREACIONES")
print("-" * 40)

print(f"Carreras totales: {len(sistema.lista_carreras)}")
print(f"Asignaturas totales: {len(sistema.lista_materias)}")
print(f"Cursos totales: {len(sistema.lista_cursos)}")
print(f"Paralelos totales: {len(datos.lista_paralelos)}")
print(f"Tutorias totales: {len(sistema.lista_tutorias)}")

print("\n45. DETALLE DE CURSOS POR CARRERA")
print("-" * 40)

cursos_software1 = [c for c in sistema.lista_cursos if c.nombre in ["Tercero", "Cuarto", "Quinto"]]
print(f"  Cursos software1: {[c.nombre for c in cursos_software1]}")

cursos_sistemas = [c for c in sistema.lista_cursos if c.nombre in ["Primero", "Segundo", "Tercero"] and c not in cursos_software1]
print(f"  Cursos sistemas: {[c.nombre for c in cursos_sistemas]}")

cursos_adm = [c for c in sistema.lista_cursos if c.nombre in ["Primero", "Segundo", "Tercero"] and c not in cursos_software1 and c not in cursos_sistemas]
print(f"  Cursos administracion: {[c.nombre for c in cursos_adm]}")

print("\n" + "=" * 60)
print("RESUMEN FINAL COMPLETO")
print("=" * 60)
print(f"Usuarios creados: {len(sistema.lista_usuarios)}")
print(f"Carreras creadas: {len(sistema.lista_carreras)}")
print(f"Asignaturas creadas: {len(sistema.lista_materias)}")
print(f"Cursos creados: {len(sistema.lista_cursos)}")
print(f"Paralelos creados: {len(datos.lista_paralelos)}")
print(f"Tutorias creadas: {len(sistema.lista_tutorias)}")
print(f"Estudiantes inscritos totales: {sum(len(p.estudiantes) if hasattr(p, 'estudiantes') else 0 for p in datos.lista_paralelos)}")
print("=" * 60)
print("PRUEBA COMPLETA FINALIZADA CON EXITO")