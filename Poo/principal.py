from estructura.usuarios import Estudiante,Docente,Personal
from estructura.asignatura import Asignatura
from estructura.calificaciones import Calificaciones
from estructura.carrera import Carrera
from estructura.horario import Horario
from estructura.tutoria import Tutoria
from estructura.carrera import Carrera
from estructura.paralelo import Paralelo


from estudiantes import agregar

usuarios=agregar()
print(usuarios)

# juanito = Estudiante("juanito","de la montaña","juanito@gmail.com","4545464","estudiante")
# juanito.iniciar_sesion()
# juanito.actualizar_datos()
# juanito.cambiar_contraseña()
# juanito.cerrar_sesion()


# pepito = Docente("pepito","de la facu","pepitocolegio@gmail.com","pepito123","docente")
# pepito.iniciar_sesion()
# pepito.actualizar_datos()
# pepito.cambiar_contraseña()
# pepito.cerrar_sesion()

# asistentes= {}
# asistentes["josue"] = "poo"
# Tutoria1= Tutoria(1 , 2010, "POO", **asistentes)
# Tutoria1.estud_asistentes()

# Docente1= Docente("David Raul","Sanchez Pincay","elteacher@uleam.edu.ec","DRSP1234","Docente")
# datos=Docente1.crear_usuario()
# print(datos)
