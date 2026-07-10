# Aqui se implementa el Modelo (MVC)
# estructura/calificaciones.py
class Calificaciones:
    """Representa una nota puntual de un estudiante en una materia."""

    def __init__(self, nota, fecha):
        self.nota = float(nota)
        self.fecha = fecha

    def asignar_nota(self):
        return self.nota

    def aprobar(self):
        """Regla de negocio: se aprueba con nota >= 7 (sobre 10)."""
        return self.nota >= 7

    def __str__(self):
        estado = "Aprobado" if self.aprobar() else "Reprobado"
        return f"{self.nota} ({estado}) - {self.fecha}"
