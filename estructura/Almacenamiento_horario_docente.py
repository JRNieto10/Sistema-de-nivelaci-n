import json

class horariodocentealmacenar:
    def __init__(self):
        self.ruta_horarios_docentes = "Datos/horarios_docentes.json"
    
    def guardar_horario_docente(self, docente, horario):
        try:
            with open(self.ruta_horarios_docentes, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except FileNotFoundError:
            datos = []
        
        encontrado = False
        for item in datos:
            if item["docente"]["cedula"] == docente.cedula:
                item["horario"] = horario
                encontrado = True
                break
        
        if not encontrado:
            datos.append({
                "docente": {
                    "cedula": docente.cedula,
                    "nombre": docente.nombre,
                    "apellido": docente.apellido,
                    "correo": docente.correo
                },
                "horario": horario
            })
        
        with open(self.ruta_horarios_docentes, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    
    def cargar_horarios_docentes(self):
        try:
            with open(self.ruta_horarios_docentes, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def obtener_horario_docente(self, cedula):
        horarios = self.cargar_horarios_docentes()
        for item in horarios:
            if item["docente"]["cedula"] == cedula:
                return item["horario"]
        return None
    
    def mostrar_horario_docente(self, cedula):
        horario = self.obtener_horario_docente(cedula)
        if not horario:
            print(f"No se encontro horario para el docente con cedula {cedula}")
            return
        
        print(f"\nHorario del docente")
        print("=" * 40)
        for paralelo, info in horario.items():
            print(f"\nParalelo: {paralelo} ({info['jornada']} - Aula: {info['aula']})")
            for materia_info in info["materias"]:
                print(f"    {materia_info['hora']} - {materia_info['materia']}")