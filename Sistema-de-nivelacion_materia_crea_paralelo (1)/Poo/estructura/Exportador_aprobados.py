# Aqui se hizo exportacion de reportes a Excel
from openpyxl import Workbook
from estructura.Almacenamiento_horario import GuardarHorarios
from estructura.Almacenamiento_calificaciones import Almacenamiento_Calificaciones
from estructura.AlmacenamietoUsuarios import Almacenamiento_Usuarios


class ExportadorAprobados:
    NOTA_MINIMA = 7

    def generar(self, ruta):
        gestor_horarios = GuardarHorarios()
        paralelos = gestor_horarios.listar_paralelos()
        usuarios = Almacenamiento_Usuarios().json.repo.leer_todo()
        nombres = {u.get("cedula"): f"{u.get('nombre','')} {u.get('apellido','')}".strip() for u in usuarios}
        calificaciones = Almacenamiento_Calificaciones().json.repo.leer_todo()
        mapa_notas = {
            (c.get("cedula_estudiante"), c.get("paralelo_id"), c.get("materia")):
            Almacenamiento_Calificaciones()._calcular_promedios(c).get("nota_final", 0)
            for c in calificaciones
        }

        # Reune todas las materias realmente matriculadas por cada estudiante.
        matriculas = {}
        for paralelo in paralelos:
            for materia in gestor_horarios._materias_paralelo(paralelo):
                for cedula in gestor_horarios._estudiantes_materia(paralelo, materia):
                    matriculas.setdefault(cedula, []).append((paralelo, materia))

        wb = Workbook()
        ws = wb.active
        ws.title = "Aprobados"
        ws.append(["Cedula", "Estudiante", "Materias matriculadas", "Notas", "Resultado"])
        cantidad = 0
        for cedula, inscripciones in sorted(matriculas.items()):
            detalles = []
            notas = []
            for paralelo, materia in inscripciones:
                nota = float(mapa_notas.get((cedula, paralelo.get("id"), materia), 0))
                notas.append(nota)
                detalles.append(f"{materia} - {paralelo.get('nombre')} ({paralelo.get('id')})")
            if notas and all(nota >= self.NOTA_MINIMA for nota in notas):
                ws.append([
                    cedula,
                    nombres.get(cedula, ""),
                    ", ".join(detalles),
                    ", ".join(f"{detalle}: {nota:.2f}" for detalle, nota in zip(detalles, notas)),
                    "Aprobado en todas las materias",
                ])
                cantidad += 1

        ws.freeze_panes = "A2"
        for columna in ws.columns:
            ancho = max(len(str(c.value or "")) for c in columna) + 2
            ws.column_dimensions[columna[0].column_letter].width = min(ancho, 60)
        wb.save(ruta)
        return True, f"Archivo generado con {cantidad} estudiante(s) aprobado(s)."
