import json

class Facada_json:
    
    def cargar_datos(self,archivo):
        try:
            with open(archivo,"r", encoding="utf-8") as f:
                datos_cargados = json.load(f)
                return datos_cargados
        except FileNotFoundError:
            return []
        
    @staticmethod
    def comprobar_duplicados(validacion, datos, lista):
        for usuario in lista:
            if usuario.get(validacion) == datos.get(validacion):
                return True
        return False
    
    def guardar_datos(self, archivo, validacion, datos):
        if isinstance(datos, list):
            return self.guardar_lista_datos(archivo, validacion, datos)

        datos_cargados = self.cargar_datos(archivo)
        if not self.comprobar_duplicados(validacion, datos, datos_cargados):
            datos_cargados.append(datos)
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos_cargados, f, indent=4, ensure_ascii=False)
            return True
        return False
    
    def guardar_lista_datos(self, archivo, validacion, lista):
        datos_cargados = self.cargar_datos(archivo)
        existentes = {item.get(validacion) for item in datos_cargados}
        nuevos = False
        
        for dato in lista:
            if dato.get(validacion) not in existentes:
                datos_cargados.append(dato)
                existentes.add(dato.get(validacion))
                nuevos = True
        if nuevos:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos_cargados, f, indent=4, ensure_ascii=False)
            return True
        return False
