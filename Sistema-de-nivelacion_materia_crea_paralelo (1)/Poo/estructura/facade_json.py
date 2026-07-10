from estructura.Repositorio_json import JsonRepository

# Aqui se hizo Patron Facade
# Esta clase simplifica el uso del repositorio JSON.
class Facada_json:
    def __init__(self, ruta):
        # Aqui se hizo Inyeccion de Dependencias
        self.repo = JsonRepository(ruta)

    @staticmethod
    def comprobar_duplicados(validacion, datos, lista):
        for item in lista:
            if item.get(validacion) == datos.get(validacion):
                return True
        return False
    
    def guardar_datos(self, validacion, datos):
        if isinstance(datos, list):
            return self.guardar_lista_datos(validacion, datos)

        datos_cargados = self.repo.leer_todo()
        
        if not self.comprobar_duplicados(validacion, datos, datos_cargados):
            datos_cargados.append(datos)
            return self.repo.guardar_todo(datos_cargados)
        return False
    
    def guardar_lista_datos(self, validacion, lista):
        datos_cargados = self.repo.leer_todo()
        existentes = {item.get(validacion) for item in datos_cargados}
        nuevos = False
        
        for dato in lista:
            if dato.get(validacion) not in existentes:
                datos_cargados.append(dato)
                existentes.add(dato.get(validacion))
                nuevos = True
                
        if nuevos:
            return self.repo.guardar_todo(datos_cargados)
        return False