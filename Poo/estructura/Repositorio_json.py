import json

class JsonRepository:
    def __init__(self, ruta: str):
        self.ruta = ruta

    def leer_todo(self) -> list:
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def guardar_todo(self, datos: list) -> bool:
        try:
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error de persistencia: {e}")
            return False