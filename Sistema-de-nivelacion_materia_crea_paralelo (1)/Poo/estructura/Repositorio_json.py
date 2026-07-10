import json
import os


# Aqui se hizo Patron Singleton
# Se reutiliza una sola instancia del repositorio por cada ruta JSON.
class JsonRepository:
    _instancias = {}

    def __new__(cls, ruta: str):
        ruta_resuelta = cls._resolver_ruta(ruta)
        if ruta_resuelta not in cls._instancias:
            cls._instancias[ruta_resuelta] = super().__new__(cls)
        return cls._instancias[ruta_resuelta]

    # Aqui se hizo Constructor
    def __init__(self, ruta: str):
        # Aqui se hizo lectura correcta de los archivos JSON guardados en el proyecto
        self.ruta = self._resolver_ruta(ruta)

    @staticmethod
    def _resolver_ruta(ruta: str) -> str:
        if os.path.isabs(ruta):
            return ruta
        # estructura/Repositorio_json.py -> Poo -> carpeta raiz del proyecto
        carpeta_estructura = os.path.dirname(os.path.abspath(__file__))
        carpeta_poo = os.path.dirname(carpeta_estructura)
        carpeta_proyecto = os.path.dirname(carpeta_poo)
        return os.path.join(carpeta_proyecto, ruta)

    # Aqui se aplico SRP
    # Esta clase solo se encarga de leer y guardar datos JSON.
    def leer_todo(self) -> list:
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos if isinstance(datos, list) else []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def guardar_todo(self, datos: list) -> bool:
        try:
            directorio = os.path.dirname(self.ruta)
            if directorio:
                os.makedirs(directorio, exist_ok=True)
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error de persistencia: {e}")
            return False
