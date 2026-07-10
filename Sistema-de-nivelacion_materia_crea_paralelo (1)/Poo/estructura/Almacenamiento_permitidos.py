# estructura/Almacenamiento_permitidos.py
from estructura.facade_json import Facada_json


class Almacenamiento_Permitidos:
    """
    Controla qué cédulas están autorizadas a registrarse en el sistema
    (Estudiante/Docente) y con qué rol. Se llena mediante importación
    masiva (CSV/Excel) desde el panel de Personal.
    """

    def __init__(self):
        self.ruta = "Datos/permitidos.json"
        self.json = Facada_json(self.ruta)

    def agregar_cedula(self, cedula, tipo):
        cedula = str(cedula).strip().replace(" ", "").replace(" ", "")
        if not (cedula.isdigit() and len(cedula) == 10):
            return False
        registro = {"cedula": cedula, "tipo": tipo.strip().lower()}
        return self.json.guardar_datos("cedula", registro)

    def esta_permitida(self, cedula, rol_esperado=None):
        datos = self.json.repo.leer_todo()
        cedula = str(cedula).strip().replace(" ", "")
        for item in datos:
            if item["cedula"] == cedula:
                if rol_esperado is None or item["tipo"] == rol_esperado.strip().lower():
                    return True
        return False

    def listar(self):
        return self.json.repo.leer_todo()
