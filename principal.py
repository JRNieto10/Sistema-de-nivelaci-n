
from facade import FacadeSistemaAcademico

sistema = FacadeSistemaAcademico()

print("""
rrrrreeeeee




""")

sistema.crear_archivos_directorios()

print("estas son las cedulas que pueden entrar")




cedulas_estudiantes = ["77777777", "888888888", "999999999", "101010101", "121212121"]
cedulas_docentes = ["111111111", "222222222", "333333333", "444444444", "666666666"]
cedulas_personal = ["123456789", "987654321", "555555555"]





sistema.agregar_cedulas_multiples(cedulas_estudiantes, "estudiante")
sistema.agregar_cedulas_multiples(cedulas_docentes, "docente")
sistema.agregar_cedulas_multiples(cedulas_personal, "personal")


print("vamos a registrar a los profesores y estudiantes y admins")


admin_personas = [("josue", "123456789", "apellido", "josue@uleam.edu", "admin123"),
    ("david", "987654321", "apellido", "david@uleam.edu", "admin321"),
    ("jessica", "555555555", "apellido", "jessica@uleam.edu", "admin132")
]

for nombre, cedula, apellido, correo, contrasena in admin_personas:
    estado, mensaje = sistema.crear_administrativo(nombre, cedula, apellido, correo, contrasena)
    print(mensaje)

profesores_lista = [
    ("pepito", "111111111", "garcia", "pepito@uleam.edu", "pepito123"),
    ("juanito", "222222222", "lopez1", "juanito@uleam.edu", "juanito123"),
    ("changuin", "333333333", "lopez2", "changuin@uleam.edu", "changuin123"),
    ("mari", "444444444", "fernandez", "mari@uleam.edu", "mari123"),
    ("carlitos", "666666666", "sanchez", "carlitos@uleam.edu", "carlitos123")
]

guardar_profes = []
for nombre, cedula, apellido, correo, contrasena in profesores_lista:
    estado, mensaje = sistema.crear_docente(nombre, cedula, apellido, correo, contrasena)
    print(mensaje)
    if estado:
        from estructura.docentes import Docente
        doc = Docente(nombre, cedula, apellido, correo, contrasena, "docente")
        guardar_profes.append(doc)

estudiantes_lista = [
    ("pedrin", "777777777", "ramirez", "pedrin@uleam.edu", "pedrin123"),
    ("laura", "888888888", "torres", "laura@uleam.edu", "laura123"),
    ("jorge", "999999999", "flores", "jorge@uleam.edu", "jorge123"),
    ("marta", "101010101", "diaz", "marta@uleam.edu", "marta123"),
    ("roberto", "121212121", "vega", "roberto@uleam.edu", "roberto123")
]

for nombre, cedula, apellido, correo, contrasena in estudiantes_lista:
    estado, mensaje = sistema.crear_estudiante(nombre, cedula, apellido, correo, contrasena)
    print(mensaje)







print("""






ahora vamos a crear las carreras:
      
      
      """)

carrera_uno = sistema.crear_carrera(1, "Ciencias de la vida", "software1", "la mañana", "presencial")
carrera_dos = sistema.crear_carrera(2, "Ciencias de la vida", "software2", "tarde", "presencial")
carrera_tres = sistema.crear_carrera(3, "tecnologia", "ti", "tarde", "virtual")

sistema.mostrar_todas_carreras()

print("""







""")

materia_poo = sistema.crear_asignatura("poo", "Poo123", 4, 5, "Presencial")
materia_bd = sistema.crear_asignatura("basede datos", "bd123", 4, 4, "Presencial")
materia_redes = sistema.crear_asignatura("redes", "red123", 3, 3, "Virtual")
materia_estructuras = sistema.crear_asignatura("estructuras", "ed145", 4, 5, "Presencial")
materia_sistemas = sistema.crear_asignatura("sistemas", "s333", 3, 3, "Virtual")

print("""


""")

for materia in [materia_poo,materia_bd,materia_redes,materia_estructuras,materia_sistemas ]:
    carga = sistema.calcular_carga_horaria_asignatura(materia)
    print(f"{materia.nombre}: {carga} horas totales")

print("creando los cursos ")

curso_a = sistema.crear_curso("Tercero A")
sistema.agregar_materia_a_curso(curso_a, "POO", 3)
sistema.asignar_docente_a_materia(curso_a, "pepito", "POO")
sistema.agregar_materia_a_curso(curso_a, "MOO", 2)
sistema.asignar_docente_a_materia(curso_a, "juanito", "POO")
sistema.agregar_materia_a_curso(curso_a, "Base de Datos", 3)
sistema.asignar_docente_a_materia(curso_a, "changuin", "Base de Datos")
sistema.agregar_materia_a_curso(curso_a, "Redes", 2)
sistema.asignar_docente_a_materia(curso_a, "mari", "Redes")
sistema.agregar_materia_a_curso(curso_a, "Estructura", 2)
sistema.asignar_docente_a_materia(curso_a, "carlitos", "Estructura")

curso_b = sistema.crear_curso("Tercero B")
sistema.agregar_materia_a_curso(curso_b, "POO", 3)
sistema.asignar_docente_a_materia(curso_b, "juanito", "POO")
sistema.agregar_materia_a_curso(curso_b, "MOO", 2)
sistema.asignar_docente_a_materia(curso_b, "changuin", "MOO")
sistema.agregar_materia_a_curso(curso_b, "Base de Datos", 3)
sistema.asignar_docente_a_materia(curso_b, "mari", "Base de Datos")
sistema.agregar_materia_a_curso(curso_b, "Redes", 2)
sistema.asignar_docente_a_materia(curso_b, "carlitos", "Redes")
sistema.agregar_materia_a_curso(curso_b, "Estructura", 2)
sistema.asignar_docente_a_materia(curso_b, "pepito", "Estructura")

curso_c = sistema.crear_curso("Tercero C")
sistema.agregar_materia_a_curso(curso_c, "POO", 3)
sistema.asignar_docente_a_materia(curso_c, "changuin", "POO")
sistema.agregar_materia_a_curso(curso_c, "MOO", 2)
sistema.asignar_docente_a_materia(curso_c, "mari", "MOO")
sistema.agregar_materia_a_curso(curso_c, "Base de Datos", 3)
sistema.asignar_docente_a_materia(curso_c, "carlitos", "Base de Datos")
sistema.agregar_materia_a_curso(curso_c, "Redes", 2)
sistema.asignar_docente_a_materia(curso_c, "pepito", "Redes")
sistema.agregar_materia_a_curso(curso_c, "Estructura", 2)
sistema.asignar_docente_a_materia(curso_c, "juanito", "Estructura")

paralelos_a = sistema.crear_paralelos("Tercero A", 2, curso_a)
paralelos_b = sistema.crear_paralelos("Tercero B", 2, curso_b)
paralelos_c = sistema.crear_paralelos("Tercero C", 2, curso_c)

todos_los_paralelos = paralelos_a + paralelos_b + paralelos_c
print(f"\nen total hay {len(todos_los_paralelos)} paralelos")



nombres_estudiantes = ["pedro", "laura", "jorge", "marta", "roberto"]
for i, nombre in enumerate(nombres_estudiantes):
    if i < len(todos_los_paralelos):
        sistema.inscribir_estudiante_en_paralelo(todos_los_paralelos[i], nombre)


nota1 = sistema.crear_calificacion(8.5, "2026-06-15")
nota2 = sistema.crear_calificacion(6.0, "2026-06-15")
nota3 = sistema.crear_calificacion(9.0, "2026-06-16")
nota4 = sistema.crear_calificacion(7.5, "2026-06-16")
nota5 = sistema.crear_calificacion(5.5, "2026-06-17")

for nota in [nota1, nota2, nota3, nota4, nota5]:
    paso = sistema.verificar_aprobacion(nota)
    estado_final = "aprobo" if paso else "reprobo"
    print(f"nota: {nota.nota} - {estado_final}")



tutoria_poo = sistema.crear_tutoria(1, "2026-06-20", "Programacion Orientada a Objetos", ["pedro", "laura"])
tutoria_bd = sistema.crear_tutoria(2, "2026-06-21", "Base de Datos", ["jorge", "marta", "roberto"])
tutoria_estructuras = sistema.crear_tutoria(3, "2026-06-22", "Estructura de Datos", ["pedro", "marta"])

sistema.programar_tutoria(tutoria_poo)
sistema.programar_tutoria(tutoria_bd)
sistema.programar_tutoria(tutoria_estructuras)
sistema.ver_asistentes_tutoria(tutoria_poo)



sistema.gestor_horarios.guardar_paralelos(todos_los_paralelos)




sistema.mostrar_horario_paralelo("Tercero A A")
print()
sistema.mostrar_horario_paralelo("Tercero A B")
print()
sistema.mostrar_horario_paralelo("Tercero B A")
print()
sistema.mostrar_horario_paralelo("Tercero B B")
print()
sistema.mostrar_horario_paralelo("Tercero C A")
print()
sistema.mostrar_horario_paralelo("Tercero C B")



sistema.guardar_horarios_docentes(guardar_profes)



for profe in profesores_lista:
    cedula = profe[1]
    print(f"\nhorario de {profe[0]}:")
    sistema.mostrar_horario_docente(cedula)



if todos_los_paralelos:
    horario_paralelo = sistema.crear_horario_paralelo(todos_los_paralelos[0])
    horario_paralelo.mostrar()

    from estructura.horarios import HorarioParalelo
    if hasattr(horario_paralelo, 'obtener_materia_por_hora'):
        materia, profe = horario_paralelo.obtener_materia_por_hora("07:00")
        if materia:
            print(f"\na las 07:00 hay: {materia} con {profe}")

if guardar_profes:
    horario_profe = sistema.crear_horario_docente("pepito")
    horario_profe.mostrar()



print("probando login como admin:")
sistema.login("123456789", "admin123")

print("\nprobando login como profe:")
sistema.login("111111111", "pepito123")

print("\nprobando login como estudiante:")
sistema.login("777777777", "pedro123")

print("\ncerrando sesion:")
sistema.logout()



usuario_prueba = {
    "nombre": "test",
    "cedula": "999999999",
    "apellido": "test",
    "correo": "test@uleam.edu",
    "contrasena": "test123",
    "rol": "docente"
}

try:
    nuevo_user = sistema.crear_usuario_con_fabrica(usuario_prueba)
    print(f"usuario creado con fabrica: {nuevo_user.nombre} - {nuevo_user.rol}")
except ValueError as e:
    print(f"error: {e}")


sistema.matricular_carrera(carrera_uno)
sistema.retirar_carrera(carrera_uno)


credencial_valida = sistema.verificar_credenciales("111111111", "pepito123")
if credencial_valida:
    print(f"credenciales correctas para: {credencial_valida['nombre']} - {credencial_valida['rol']}")

credencial_mala = sistema.verificar_credenciales("111111111", "wrongpass")
if not credencial_mala:
    print("credenciales malas rechazadas")

print("")
print("mostrando horarios guardados en json")
print("")

paralelo_guardado = sistema.obtener_horario_paralelo("Tercero A A")
if paralelo_guardado:
    print(f"horario de Tercero A A encontrado con {len(paralelo_guardado)} materias")

horario_profe_guardado = sistema.obtener_horario_docente("111111111")
if horario_profe_guardado:
    print(f"horario de pepito encontrado con {len(horario_profe_guardado)} paralelos")

print("")
print("metodos del curso")
print("")

docentes_poo = sistema.obtener_docentes_por_materia(curso_a, "POO")
print(f"docentes de POO en Tercero A: {docentes_poo}")

materias_pepito = sistema.obtener_materias_por_docente(curso_a, "pepito")
print(f"materias de pepito en Tercero A: {materias_pepito}")

