import json
from estructura.facade_json import Facada_json

class horariodocentealmacenar:
    def __init__(self,rol):
        self.rol = rol.lower()
        self.ruta_horarios = f"Poo/Datos/horarios_{self.rol}.json"
        self.json = Facada_json(self.ruta_horarios)
    
    def guardar_horario_docente(self, datos, horario):
        datos_cargados = self.json.repo.leer_todo()
        
        encontrado = False
        for item in datos_cargados:
            if item[self.rol]["cedula"] == datos.cedula:
                item["horario"] = horario
                encontrado = True
                break
        
        if not encontrado:
            datos_cargados.append({
                self.rol: {
                    "cedula": datos.cedula,
                    "nombre": datos.nombre,
                    "apellido": datos.apellido,
                    "correo": datos.correo
                },
                "horario": horario
            })

        self.json.repo.guardar_todo(datos_cargados)
    
