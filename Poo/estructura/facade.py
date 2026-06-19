import json

class Facada_json:
    
    def cargar_datos(self,archivo):
        try:
            with open(archivo,"r", encoding="utf-8") as f:
                datos_cargados = json.load(f)
                return datos_cargados
        except Exception:
            print("No existe ningun usuario registrado por el momento")
            return False

    def guardar_datos(self,archivo,datos_cargados):
        with open(archivo,"w",encoding="utf-8") as archivo:
            json.dump(datos_cargados, archivo, indent=4, ensure_ascii=False)
