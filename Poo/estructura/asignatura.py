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
        # cada credito equivale a una hora de clase a la semana
        return self.creditos * self.horas

    def __str__(self):
        return f"{self.nombre} ({self.creditos} creditos)"