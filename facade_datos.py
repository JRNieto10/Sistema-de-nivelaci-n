from estructura.Almacenamiento_horario import GuardarHorarios
from estructura.Almacenamiento_horario_docente import horariodocentealmacenar
from estructura.gest_permitidos import GestionPermitidos
import json
import os

class FacadeDatos:
    def __init__(self):
        self._inicializar_subsistemas()
        self.lista_paralelos = []

    def _inicializar_subsistemas(self):
        self.gestor_horarios = GuardarHorarios()
        self.gestor_horarios_docentes = horariodocentealmacenar()
        self.gestion_permitidos = GestionPermitidos()

    def agregar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.agregar_cedula(cedula, tipo)

    def guardar_horario_docente(self, docente, cursos):
        if hasattr(docente, 'horario'):
            self.gestor_horarios_docentes.guardar_horario_docente(docente, cursos)

    def crear_horario_paralelo(self, curso, nombre_paralelo=None):
        from estructura.gestor_curso import Gestor_curso
        gestor_cursos = Gestor_curso()
        
        if nombre_paralelo is None:
            cantidad_paralelos = len([p for p in self.lista_paralelos if p.curso == curso])
            letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            letra = letras[cantidad_paralelos % len(letras)]
            nombre_paralelo = f"{curso.nombre}_{letra}"
        
        paralelo = gestor_cursos.crear_paralelo(nombre_paralelo, 1, curso)
        self.lista_paralelos.append(paralelo)
        self.gestor_horarios.guardar_paralelo(paralelo)
        
        return paralelo

    def mostrar_horario_paralelo(self, nombre_paralelo):
        self.gestor_horarios.mostrar_horario_paralelo(nombre_paralelo)

    def mostrar_horario_docente(self, docente):
        if hasattr(docente, 'horario'):
            print(f"\n=== HORARIO DEL DOCENTE: {docente.nombre} ===")
            for dia, clases in docente.horario.items():
                print(f"\n{dia.upper()}:")
                if clases:
                    for clase in clases:
                        print(f"  {clase['hora_inicio']} - {clase['hora_fin']} | "
                              f"Materia: {clase['materia']} | "
                              f"Paralelo: {clase['paralelo']} | "
                              f"Aula: {clase['aula']}")
                else:
                    print("  Sin clases")
        else:
            print(f"El docente {docente.nombre} no tiene horario asignado")

    def mostrar_todos_los_paralelos(self):
        print("\n=== PARALELOS REGISTRADOS ===")
        for paralelo in self.lista_paralelos:
            if hasattr(paralelo, 'nombre'):
                print(f"- {paralelo.nombre}")
            else:
                print(f"- {paralelo}")

    def eliminar_cedula_permitida(self, cedula, tipo):
        return self.gestion_permitidos.eliminar_cedula(cedula, tipo)

    def verificar_cedula(self, cedula):
        return self.gestion_permitidos.verificar_cedula(cedula)