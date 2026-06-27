import json
from datetime import datetime

class GestorAlmacenamiento:
    def __init__(self):
        self.ruta_estudiantes = "Datos/estudiantes.json"
        self.ruta_docentes = "Datos/docentes.json"
        self.ruta_personal = "Datos/personal_administrativo.json"
        self._crear_archivos_json()
    
    def _crear_archivos_json(self):
        archivos = [
            self.ruta_estudiantes,
            self.ruta_docentes,
            self.ruta_personal
        ]
        for archivo in archivos:
            try:
                with open(archivo, 'x', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
            except FileExistsError:
                pass
    
    def _cargar_datos(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _guardar_datos(self, ruta_archivo, datos):
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    
    def comprobar_duplicados(self, cedula, tipo_usuario):
        if tipo_usuario.lower() == "estudiante":
            ruta = self.ruta_estudiantes
        elif tipo_usuario.lower() == "docente":
            ruta = self.ruta_docentes
        elif tipo_usuario.lower() == "personal" or tipo_usuario.lower() == "administrador":
            ruta = self.ruta_personal
        else:
            raise ValueError("Tipo de usuario no valido")
        
        usuarios = self._cargar_datos(ruta)
        
        for usuario_existente in usuarios:
            if usuario_existente.get('cedula') == cedula:
                return True
        return False
    
    def agregar_usuario(self, usuario, tipo_usuario):
        if self.comprobar_duplicados(usuario['cedula'], tipo_usuario):
            return False
        
        if tipo_usuario.lower() == "estudiante":
            ruta = self.ruta_estudiantes
        elif tipo_usuario.lower() == "docente":
            ruta = self.ruta_docentes
        elif tipo_usuario.lower() == "personal" or tipo_usuario.lower() == "administrador":
            ruta = self.ruta_personal
        else:
            raise ValueError("Tipo de usuario no valido")
        
        usuarios = self._cargar_datos(ruta)
        usuario['fecha_registro'] = datetime.now().isoformat()
        usuarios.append(usuario)
        self._guardar_datos(ruta, usuarios)
        return True