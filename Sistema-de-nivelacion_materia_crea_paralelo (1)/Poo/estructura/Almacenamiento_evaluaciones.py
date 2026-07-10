# Aqui se implementa el Modelo (MVC)
# Aqui se hizo Configuracion de Evaluaciones del silabo
from estructura.facade_json import Facada_json


class Almacenamiento_Evaluaciones:
    """Guarda los segmentos de evaluacion que define el administrador."""

    def __init__(self):
        self.ruta = "Datos/evaluaciones_config.json"
        self.json = Facada_json(self.ruta)
        self.segmentos_defecto = [
            {"nombre": "Actuacion", "porcentaje": 25, "valor": 2.5},
            {"nombre": "Produccion", "porcentaje": 25, "valor": 2.5},
            {"nombre": "Practica", "porcentaje": 15, "valor": 1.5},
            {"nombre": "Evaluacion final", "porcentaje": 35, "valor": 3.5},
        ]

    def obtener_configuracion(self):
        datos = self.json.repo.leer_todo()
        if not datos:
            self.guardar_configuracion(self.segmentos_defecto, 10)
            return {"nota_final": 10, "segmentos": self.segmentos_defecto}
        return datos[0]

    def guardar_configuracion(self, segmentos, nota_final=10):
        # Aqui se hizo Validacion de porcentajes de evaluacion
        total = sum(float(s.get("porcentaje", 0)) for s in segmentos)
        if round(total, 2) != 100:
            return False, "Los porcentajes deben sumar 100%."
        nota_final = float(nota_final)
        segmentos_limpios = []
        for s in segmentos:
            nombre = str(s.get("nombre", "")).strip()
            porcentaje = float(s.get("porcentaje", 0))
            if not nombre or porcentaje <= 0:
                return False, "Cada segmento debe tener nombre y porcentaje mayor a 0."
            segmentos_limpios.append({
                "nombre": nombre,
                "porcentaje": porcentaje,
                "valor": round(nota_final * porcentaje / 100, 2),
            })
        return self.json.repo.guardar_todo([{"nota_final": nota_final, "segmentos": segmentos_limpios}]), "Configuracion guardada."

    def nombres_segmentos(self):
        return [s["nombre"] for s in self.obtener_configuracion().get("segmentos", [])]

    def valor_segmento(self, nombre_segmento):
        for s in self.obtener_configuracion().get("segmentos", []):
            if s.get("nombre") == nombre_segmento:
                return float(s.get("valor", 0))
        return 0
