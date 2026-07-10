"""
Prueba de integración SIN interfaz gráfica.
Ejercita: autenticación, factory de usuarios, carreras/materias, importación
masiva de cédulas (Strategy), matrícula de docentes, creación de paralelos,
matrícula de estudiantes (con choque de horario), calificaciones y tutorías.

Ejecutar desde la carpeta Poo/:  python3 Pruebas/prueba_sistema_completo.py
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estructura.fabrica_usuarios import FabricaUsuarios
from estructura.AlmacenamietoUsuarios import Almacenamiento_Usuarios
from estructura.Almacenamiento_permitidos import Almacenamiento_Permitidos
from estructura.Autenticacion import Autenticacion


def linea(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


fabrica = FabricaUsuarios()
alm_usuarios = Almacenamiento_Usuarios()
login = Autenticacion(alm_usuarios)

# 1. Crear administrador (Personal) directamente, sin necesitar cédula permitida
linea("1. Crear Personal (Admin)")
admin = fabrica.crear_usuario({
    "nombre": "Ana", "apellido": "Reyes", "correo": "ana@uleam.edu.ec",
    "contraseña": "admin123", "rol": "Personal", "cedula": "1000000001"
})
assert alm_usuarios.guardar_usuario_objeto(admin), "No se pudo guardar el admin"
print("Admin creado y guardado.")

# 2. Importación masiva de cédulas (Patrón Strategy) para autorizar Docente/Estudiante
linea("2. Importar cédulas autorizadas desde CSV (Strategy)")
resultado = admin.importar_cedulas("importaciones/cedulas_ejemplo.csv")
print("Resultado importación:", resultado)
assert resultado["exitosos"] >= 1

permitidos = Almacenamiento_Permitidos()
assert permitidos.esta_permitida("555555555", "docente")
assert permitidos.esta_permitida("6060606060", "estudiante")
print("Cédulas correctamente autorizadas.")

# 3. Registrar Docente y Estudiante (ya autorizados)
linea("3. Registrar Docente y Estudiante autorizados")
docente = fabrica.crear_usuario({
    "nombre": "Carlos", "apellido": "Perez", "correo": "carlos@uleam.edu.ec",
    "contraseña": "doc123", "rol": "Docente", "cedula": "555555555"
})
assert alm_usuarios.guardar_usuario_objeto(docente)

estudiante = fabrica.crear_usuario({
    "nombre": "Maria", "apellido": "Lopez", "correo": "maria@uleam.edu.ec",
    "contraseña": "est123", "rol": "Estudiante", "cedula": "6060606060"
})
assert alm_usuarios.guardar_usuario_objeto(estudiante)
print("Docente y Estudiante registrados.")

# 4. Crear carrera y materia
linea("4. Crear carrera y materia")
carrera = admin.crear_carrera("C1", "Ingeniería en Software", 8)

from estructura.Almacenamiento_materias import CreadorAcademico
academico = CreadorAcademico()
academico.agregar_materia_a_carrera("Ingeniería en Software", {"id": "M1", "nombre": "POO", "creditos": 4})
print("Carrera y materia creadas.")

# 5. Matricular al docente en la materia (a nivel de currícula)
linea("5. Matricular Docente a Materia")
assert academico.matricular_docente("555555555", "Ingeniería en Software", "POO")
print("Docente matriculado en la materia POO.")

# 6. Crear un paralelo concreto (materia + docente + horario)
linea("6. Crear Paralelo")
paralelo = admin.crear_paralelo("P1", "Tercero A", "Matutina", "POO", "555555555",
                                 "Lunes", "07:00", "09:00", "Aula 101")
print("Paralelo creado:", paralelo)

# 7. El docente ve sus materias asignadas
linea("7. Docente consulta sus materias")
materias_docente = docente.ver_materias_asignadas()
print(materias_docente)
assert len(materias_docente) == 1

# 8. El estudiante se matricula en el paralelo
linea("8. Estudiante se matricula")
exito, msg = estudiante.matricularse("P1")
print(exito, msg)
assert exito

# 8b. Intentar matricular de nuevo debe fallar (ya inscrito)
exito2, msg2 = estudiante.matricularse("P1")
print(exito2, msg2)
assert not exito2

# 9. Choque de horario: crear otro paralelo que se cruza y debe fallar la matrícula
linea("9. Probar choque de horario")
admin.crear_paralelo("P2", "Tercero B", "Matutina", "POO", "555555555",
                      "Lunes", "08:00", "10:00", "Aula 102")
exito3, msg3 = estudiante.matricularse("P2")
print(exito3, msg3)
assert not exito3, "Debió detectar el choque de horario"

# 10. Docente califica al estudiante
linea("10. Docente califica al estudiante")
docente.calificar_estudiante("6060606060", "POO", 8.5, "2026-07-09")
notas = estudiante.ver_notas()
print(notas)
assert len(notas) == 1 and notas[0]["aprobado"] is True

# 11. Docente crea tutoría y el estudiante se inscribe
linea("11. Tutorías")
docente.crear_tutoria("T1", "2026-07-15", "Refuerzo de Herencia y Polimorfismo")
disponibles = estudiante.ver_tutorias_disponibles()
print(disponibles)
assert len(disponibles) == 1
estudiante.inscribirse_en_tutoria("T1")
tutorias_docente = docente.ver_tutorias()
assert "6060606060" in tutorias_docente[0]["estudiantes"]

# 12. Horario del estudiante
linea("12. Horario del estudiante")
horario = estudiante.ver_horario()
print(horario)
assert len(horario) == 1

# 13. Login real a través de Autenticacion
linea("13. Probar login real")
assert login.iniciar_sesion("maria@uleam.edu.ec", "est123")
login.cerrar_sesion()
assert not login.iniciar_sesion("maria@uleam.edu.ec", "clave_incorrecta")

linea("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
