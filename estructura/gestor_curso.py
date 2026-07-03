from estructura.cursos import Curso
from .paralelo import Paralelo

class Gestor_curso:
    def __init__(self):
        self.lista_cursos = []
        self.lista_paralelos = []

    def crear_curso(self, nombre_curso):
        curso = Curso(nombre_curso)
        self.lista_cursos.append(curso)
        return curso

    def crear_paralelo(self, nombre, id=1, curso=None):
        paralelo = Paralelo(nombre, id, curso)  # id siempre será 1
        self.lista_paralelos.append(paralelo)
        return paralelo