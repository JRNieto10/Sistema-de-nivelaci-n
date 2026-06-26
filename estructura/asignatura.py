class Asignatura:
    def __init__(self,nombre,codigo,creditos,horas, modalidad):
        self.nombre = nombre
        self.codigo = codigo 
        self.creditos = creditos 
        self.horas = horas
        self.modalidad = modalidad

    def obtener_nombre(self):
        return self.nombre

    def obtener_creditos(self):
        return self.creditos

    def calcular_carga_horaria(self):
        return self.horas * self.creditos