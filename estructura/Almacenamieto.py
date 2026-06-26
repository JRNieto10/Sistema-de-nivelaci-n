import json

class Almacenamiento_Usuarios:
    def __init__(self):
        self.ruta_estudiantes = "Datos/estudiantes.json"
        self.ruta_docentes = "Datos/docentes.json"
        self.ruta_personal = "Datos/personal_administrativo.json"
    
    def _cargar_datos(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def verificar_credenciales(self, cedula, contrasena_ingresada):
        archivos = [
            (self.ruta_estudiantes, "estudiante"),
            (self.ruta_docentes, "docente"),
            (self.ruta_personal, "personal")
        ]
        
        for ruta, tipo in archivos:
            usuarios = self._cargar_datos(ruta)
            for usuario in usuarios:
                if usuario.get('cedula') == cedula and usuario.get('contrasena') == contrasena_ingresada:
                    usuario['tipo'] = tipo
                    return usuario
        
        return False