# from estructura.usuarios import Estudiante,Docente,Personal
# from estructura.asignatura import Asignatura
# from estructura.calificaciones import Calificaciones
# from estructura.carrera import Carrera
# from estructura.horario import Horario
# from estructura.tutoria import Tutoria
# from estructura.carrera import Carrera
# from estructura.paralelo import Paralelo


# from estudiantes import agregar

# usuarios=agregar()
# print(usuarios)

# # juanito = Estudiante("juanito","de la montaña","juanito@gmail.com","4545464","estudiante")
# # juanito.iniciar_sesion()
# # juanito.actualizar_datos()
# # juanito.cambiar_contraseña()
# # juanito.cerrar_sesion()


# # pepito = Docente("pepito","de la facu","pepitocolegio@gmail.com","pepito123","docente")
# # pepito.iniciar_sesion()
# # pepito.actualizar_datos()
# # pepito.cambiar_contraseña()
# # pepito.cerrar_sesion()

# # asistentes= {}
# # asistentes["josue"] = "poo"
# # Tutoria1= Tutoria(1 , 2010, "POO", **asistentes)
# # Tutoria1.estud_asistentes()

# # Docente1= Docente("David Raul","Sanchez Pincay","elteacher@uleam.edu.ec","DRSP1234","Docente")
# # datos=Docente1.crear_usuario()
# # print(datos)

# usuario = factory.crear_usuario("Marcos","Solorzano","ADADASDA","123456","Estudiante")
# usuario_2 = factory.crear_usuario("Wagner","Anchundia","@gmail.com","123456","Docente")
# usuario_3 = factory.crear_usuario("Marcos","Solorzano","ADADASDA","123456","Personal")
# usuario.iniciar_sesion()
# usuario_2.iniciar_sesion()
# usuario_3.iniciar_sesion()
# p= usuario.crear_usuario()
# p2= usuario_2.crear_usuario()
# p3= usuario_3.crear_usuario()
# alm = Almacenar_Usuarios()
# alm.obtener(p)
# alm.obtener(p2)
# alm.obtener(p3)

from estructura.fabrica_usuarios import FabricaUsuarios
from estructura.Almacenamieto import Almacenamiento_Usuarios
from Ingresar_datos import *
from estructura.Autenticacion import *

factory = FabricaUsuarios()
ingreso = Ingreso_datos()
alm = Almacenamiento_Usuarios()
login = Autenticacion(alm)

datos = ingreso.agregar(0)
usuario = factory.crear_usuario(datos)
alm.obtener(datos)
datos = ingreso.agregar(2)
usuario = factory.crear_usuario(datos)
alm.obtener(datos)
login.iniciar_sesion("a", "e")
login.cerrar_sesion()
login.iniciar_sesion("a","a")
login.cerrar_sesion()


# PRUEBA DE HORARIO Y PARALELO

from estructura.horario import Horario
from estructura.paralelo import Paralelo

# usuario contiene el último usuario creado.
# En este flujo corresponde al estudiante ingresado
# mediante ingreso.agregar(2).

horario_a = Horario("Lunes", "07:00", "09:00", "101")
horario_b = Horario("Lunes", "08:00", "10:00", "102")  # choca

paralelo_a = Paralelo("1", "Tercero A", "Matutina", horario_a)
paralelo_b = Paralelo("2", "Tercero B", "Matutina", horario_b)

print("\n=== PARALELOS ===")
print(paralelo_a)
print(paralelo_b)

print("\n=== INSCRIPCIÓN ===")
paralelo_a.inscribir_estudiante(usuario)

print("\n=== INTENTO DE INSCRIPCIÓN CON CHOQUE DE HORARIO ===")
paralelo_b.inscribir_estudiante(
    usuario,
    paralelos_del_estudiante=[paralelo_a]
)

print("\n=== RETIRO ===")
paralelo_a.retirar_estudiante(usuario)


