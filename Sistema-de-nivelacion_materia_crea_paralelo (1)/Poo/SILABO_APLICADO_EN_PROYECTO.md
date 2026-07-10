# Mapa de temas del sílabo aplicados en el proyecto

Este archivo sirve como guía para ubicar en el código los temas revisados en Programación Orientada a Objetos.

## Unidad 1. Fundamentos de Programación Orientada a Objetos

- Introducción a POO: el sistema trabaja con objetos como usuarios, tutorías, horarios, carreras y paralelos.
- Abstracción: `estructura/clases_abstractas.py` define la clase base `Usuarios`.
- Clases y objetos: `estructura/usuarios.py`, `estructura/tutoria.py`, `estructura/horario.py`, `estructura/paralelo.py`.
- Encapsulamiento: atributos manejados desde clases y métodos.
- Constructores: métodos `__init__` en usuarios, tutorías, horarios, paralelos y ventanas.
- Métodos: guardar usuarios, crear carreras, crear paralelos, crear tutorías, generar horarios, matricular estudiantes.

## Unidad 2. Herencia, polimorfismo e interfaces

- Herencia: `Docente`, `Estudiante` y `Personal` heredan de `Usuarios`.
- Polimorfismo: cada rol tiene su propio `opciones_menu`.
- Interfaces: `estructura/interfaces.py` contiene la interfaz para actualizar datos.
- Inyección de dependencias: `interfaz.py` pasa el almacenamiento al servicio de autenticación.

## Unidad 3. Patrones de diseño

- SOLID:
  - SRP: archivos separados por responsabilidad: usuarios, horarios, tutorías, importación.
  - OCP: la fábrica permite crear usuarios según rol.
  - DIP: la autenticación depende del almacenamiento recibido.
- Patrones creacionales:
  - Factory: `estructura/fabrica_usuarios.py`.
  - Factory de importación: `estructura/estrategias_importacion.py`.
- Patrones de comportamiento:
  - Strategy: importación CSV y Excel con estrategias separadas.
- Patrones estructurales:
  - Facade: `estructura/facade_json.py` simplifica el manejo del JSON.

## Unidad 4. Arquitectura de software

- Arquitectura por capas:
  - `vista_*.py`: capa de presentación.
  - `estructura/*.py`: modelo y lógica.
  - `Datos/*.json`: almacenamiento.
- MVC:
  - Vista: archivos `vista_*.py`.
  - Modelo: clases dentro de `estructura/`.
  - Controlador/lógica de coordinación: autenticación, almacenamiento y métodos llamados desde las vistas.

## Cambios funcionales agregados

1. Importación de usuarios desde CSV/Excel con columna `tipo_usuario`.
2. Creación automática de usuarios como Estudiante, Docente o Personal.
3. Botón para mostrar todos los usuarios registrados.
4. Creación de paralelos a partir de materias ya creadas.
5. Tutorías ligadas a materias y paralelos.
6. Solo estudiantes matriculados en la materia pueden ver/inscribirse en tutorías.
7. Docente puede marcar estudiantes obligatorios para una tutoría.
8. Horarios generados por todas las materias de un paralelo.
9. Validación de choques de horario para el mismo docente.

Los comentarios en el código usan frases simples como:

```python
# Aqui se hizo Herencia
# Aqui se hizo Polimorfismo
# Aqui se hizo Patron Factory
# Aqui se hizo Patron Strategy
# Aqui se implementa la Vista (MVC)
```

## Cambios finales agregados

- **Tutorías obligatorias:** cuando el docente selecciona estudiantes obligatorios, esos estudiantes quedan inscritos automáticamente en la tutoría y en su panel aparece como "Tutoría obligatoria".
- **Configuración de evaluaciones:** el administrador puede modificar los segmentos de evaluación y sus porcentajes. Por defecto se usa: Actuación 25%, Producción 25%, Práctica 15% y Evaluación final 35%, sobre una nota final de 10.
- **Actividades por segmento:** el docente ya no registra una sola nota general, sino actividades dentro de cada segmento. El sistema promedia las actividades de cada segmento y calcula la nota final de la materia.
- **Consulta de notas del estudiante:** el estudiante puede ver actividades, promedio por segmento, aporte de cada segmento y nota final.
- **Uso real de JSON:** el repositorio JSON fue ajustado para leer y guardar los archivos dentro de la carpeta `Datos` del proyecto, aunque el programa se ejecute desde otra ubicación.
