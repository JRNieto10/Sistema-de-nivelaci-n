#Grupo_1.
#Sistema_de_nivelación.
class PlanificadorCurso:
    def __init__(self, docente, materia, horas, cupos):
        self.docente = docente
        self.materia = materia
        #prvados
        self.__horas = horas
        self.__cupos = cupos
        
        #protrgido
        self._inscritos = 0
    
    @property
    def cupos(self):
        return self.__cupos

    @cupos.setter
    def cupos(self, valor):
        if valor > 0:
            self.__cupos = valor
        else:
            print("los cupos deben ser mayores a 0")

    @property
    def horas(self):
        return self.__horas

    @horas.setter
    def horas(self, valor):
        if valor > 0:
            self.__horas = valor
        else:
            print("Error: Las horas deben ser positivas")

    #metodos y sobrecarga
    def registrar_estudiante(self, nombre, becado=False):
        if self._inscritos < self.__cupos:
            self._inscritos += 1
            tipo = "Becado" if becado else "Regular"
            print(f"Estudiante {nombre} registrado como {tipo}.")
        else:
            print("No hay cupos disponibles.")

    def mostrar_info(self):
        print("\n===Información del Curso===")
        print(f"Docente: {self.docente}")
        print(f"Materia: {self.materia}")
        print(f"Horas: {self.__horas}")
        print(f"Cupos totales: {self.__cupos}")
        print(f"Inscritos: {self._inscritos}")
        print(f"Cupos disponibles: {self.__cupos - self._inscritos}")

#intancias(envios de datos)

curso1 = PlanificadorCurso("Juan Pérez", "Matemática", 40, 2)
curso2 = PlanificadorCurso("Ana López", "Física", 35, 3)

# Uso de métodos
curso1.mostrar_info()
curso2.mostrar_info()

# Registro de estudiantes (sobrecarga)
curso1.registrar_estudiante("Carlos")
curso1.registrar_estudiante("María", True)
curso1.registrar_estudiante("Luis")  # ya no hay cupos

# Uso de propiedades (setter)
curso2.cupos = 5
curso2.horas = 50

curso2.mostrar_info()