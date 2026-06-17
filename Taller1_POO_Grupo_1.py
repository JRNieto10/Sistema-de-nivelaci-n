# Grupo_1.
#Integrantes:
#Anchundia Anchundia Wagner Modesto
#Nieto Hernández Jessika Rosmary
#Sánchez Villavicencio Josué Alexander
#Sánchez Pincay David Raúl
#Zambrano Roldan Joice Magdalena

# Sistema de nivelación.

class PlanificadorCurso:
    def __init__(self, docente, materia, horas, cupos):
        self.docente = docente
        self.materia = materia

        # privados
        self.__horas = horas
        self.__cupos = cupos

        # protegido
        self._inscritos = 0

        # lista simple para simular estudiantes (mejora lógica)
        self._lista_estudiantes = []

    @property
    def cupos(self):
        return self.__cupos

    @cupos.setter
    def cupos(self, valor):
        if valor > 0 and valor >= self._inscritos:
            self.__cupos = valor
        else:
            print("Error: los cupos deben ser mayores a 0 y no menores a los inscritos")

    @property
    def horas(self):
        return self.__horas

    @horas.setter
    def horas(self, valor):
        if valor > 0:
            self.__horas = valor
        else:
            print("Error: las horas deben ser positivas")

    # método con "sobrecarga" usando *args
    def registrar_estudiante(self, *args, becado=False):
        for nombre in args:
            if self._inscritos < self.__cupos:
                self._inscritos += 1
                self._lista_estudiantes.append(nombre)

                tipo = "Becado" if becado else "Regular"
                print(f"Estudiante {nombre} registrado como {tipo}.")
            else:
                print(f"No hay cupos disponibles para {nombre}.")

    def mostrar_info(self):
        print("\n=== Información del Curso ===")
        print(f"Docente: {self.docente}")
        print(f"Materia: {self.materia}")
        print(f"Horas: {self.__horas}")
        print(f"Cupos totales: {self.__cupos}")
        print(f"Inscritos: {self._inscritos}")
        print(f"Cupos disponibles: {self.__cupos - self._inscritos}")
        print(f"Estudiantes: {self._lista_estudiantes}")


# instancias (envío de datos)

curso1 = PlanificadorCurso("Juan Pérez", "Matemática", 40, 2)
curso2 = PlanificadorCurso("Ana López", "Física", 35, 3)

# mostrar info inicial
curso1.mostrar_info()
curso2.mostrar_info()

# registro de estudiantes (sobrecarga real con *args)
curso1.registrar_estudiante("Carlos")
curso1.registrar_estudiante("María", "Luis")  # prueba de múltiples entradas

curso2.registrar_estudiante("Sofía", becado=True)
curso2.registrar_estudiante("Pedro", "Lucía")

# modificar propiedades
curso2.cupos = 5
curso2.horas = 50

# mostrar resultados finales
curso1.mostrar_info()
curso2.mostrar_info()