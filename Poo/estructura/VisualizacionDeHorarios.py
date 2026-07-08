from estructura.facade_json import Facada_json

class Visualizador_Horarios:
    def __init__(self, rol, identificador):
        self.__rol = rol.lower()  # CAMBIO: Ahora es estrictamente privado
        self._identificador = identificador
        self.ruta_horarios = f"Poo/Datos/horarios_{rol}.json"
        self.json = Facada_json(self.ruta_horarios)

    def cargar_horarios(self):
        return self.json.repo.leer_todo()
    
    def obtener_horario(self):
        horarios = self.cargar_horarios()
        for item in horarios:
            if self.__rol == "paralelo":
                if item["nombre"] == self._identificador:
                    return item["horario"]
            # Si es docente/estudiante, mantiene tu lógica original
            elif item[self.__rol]["cedula"] == self._identificador:
                return item["horario"]
        return None
    
    def _imprimir_horario_usuario(self, horario):
        print(f"\nHorario del {self.__rol}")
        print("=" * 40)
        for paralelo, info in horario.items():
            print(f"\nParalelo: {paralelo} ({info['jornada']} - Aula: {info['aula']})")
            for materia_info in info["materias"]:
                print(f"    [{materia_info['dia']}] {materia_info['hora']} - {materia_info['materia']}")
    
    def _imprimir_horario_paralelo(self, horario):
        print(f"\nHorario del paralelo: {self._identificador}")
        print("=" * 40)
        for materia, info in horario.items():
            print(f"    {info['hora']} - {materia} ({info['docente']})")

    @property
    def horario(self):
        """Propiedad principal que decide qué y cómo mostrar según el rol"""
        datos_horario = self.obtener_horario()
        
        if not datos_horario:
            print(f"No se encontró horario para {self.__rol}: {self._identificador}")
            return None
        
        # Redirecciona al formato de impresión correcto según el rol
        if self.__rol == "paralelo":
            self._imprimir_horario_paralelo(datos_horario)
        else:
            self._imprimir_horario_usuario(datos_horario)
            
        # Opcional: devolvemos los datos por si además de imprimirlos quieres usarlos
        return datos_horario