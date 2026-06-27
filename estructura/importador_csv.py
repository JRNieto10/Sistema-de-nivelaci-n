"""
importador_csv.py
=================
Ubicación: estructura/importador_csv.py

Responsabilidad única (SRP): leer un CSV con cédulas y cargarlas
en permitidos.json a través de GestionPermitidos.

El CSV solo necesita dos columnas:
    cedula, tipo
    1234567890, estudiante
    0987654321, docente
    1122334455, personal

Principios aplicados:
- SRP  : esta clase solo lee CSV y delega el guardado (no toca JSON directamente).
- OCP  : si en el futuro se necesita importar desde Excel u otro formato,
         se crea una subclase de LectorMasivo sin tocar ImportadorCSV.
- DIP  : depende de GestionPermitidos (abstracción), no de archivos JSON directo.
- Herencia: LectorMasivo (ABC) → ImportadorCSV (implementación concreta).
"""

import csv
import os
from abc import ABC, abstractmethod
from estructura.gest_permitidos import GestionPermitidos

TIPOS_VALIDOS = {"estudiante", "docente", "personal"}


# ---------------------------------------------------------------------------
# Clase base abstracta — contrato para cualquier importador masivo
# ---------------------------------------------------------------------------

class LectorMasivo(ABC):
    """
    Define el contrato para importadores masivos de cédulas.
    Subclases posibles: ImportadorCSV, ImportadorExcel, ImportadorAPI, etc.
    """

    def __init__(self, gestor_permitidos: GestionPermitidos):
        self.gestor = gestor_permitidos

    @abstractmethod
    def importar(self, origen: str) -> dict:
        """
        Importa cédulas desde 'origen'.
        Retorna: { "exitosos": int, "duplicados": int, "errores": list }
        """

    def _construir_resumen(self) -> dict:
        return {"exitosos": 0, "duplicados": 0, "errores": []}


# ---------------------------------------------------------------------------
# Implementación concreta para CSV
# ---------------------------------------------------------------------------

class ImportadorCSV(LectorMasivo):
    """
    Lee un CSV con columnas 'cedula' y 'tipo', y habilita cada cédula
    en permitidos.json usando GestionPermitidos.agregar_multiple().

    Wagner: para conectar esto a CustomTkinter, llama a:
        resultado = sistema.importar_cedulas_csv(ruta_del_archivo)
    y muestra resultado["exitosos"], resultado["duplicados"], resultado["errores"]
    en los labels o cuadros de texto de la interfaz.
    """

    COLUMNAS_REQUERIDAS = {"cedula", "tipo"}

    def importar(self, origen: str) -> dict:
        resumen = self._construir_resumen()

        if not os.path.exists(origen):
            resumen["errores"].append(f"Archivo no encontrado: {origen}")
            return resumen

        with open(origen, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            encabezados = set(lector.fieldnames or [])

            if not self.COLUMNAS_REQUERIDAS.issubset(encabezados):
                faltantes = self.COLUMNAS_REQUERIDAS - encabezados
                resumen["errores"].append(f"Columnas faltantes en el CSV: {faltantes}")
                return resumen

            # Agrupar por tipo para una sola escritura al JSON por tipo
            por_tipo: dict[str, list[str]] = {
                "estudiante": [],
                "docente": [],
                "personal": [],
            }

            for num_fila, fila in enumerate(lector, start=2):
                cedula = fila.get("cedula", "").strip()
                tipo   = fila.get("tipo",   "").strip().lower()

                if not cedula or not tipo:
                    resumen["errores"].append(
                        f"Fila {num_fila}: campos vacíos, se omite"
                    )
                    continue

                if not cedula.isdigit():
                    resumen["errores"].append(
                        f"Fila {num_fila}: cédula '{cedula}' no es numérica"
                    )
                    continue

                if tipo not in TIPOS_VALIDOS:
                    resumen["errores"].append(
                        f"Fila {num_fila}: tipo '{tipo}' no válido "
                        f"(debe ser estudiante / docente / personal)"
                    )
                    continue

                por_tipo[tipo].append(cedula)

        # Delegar el guardado — GestionPermitidos maneja duplicados internamente
        for tipo, cedulas in por_tipo.items():
            if not cedulas:
                continue
            agregadas  = self.gestor.agregar_multiple(cedulas, tipo)
            duplicadas = len(cedulas) - len(agregadas)
            resumen["exitosos"]   += len(agregadas)
            resumen["duplicados"] += duplicadas

        return resumen

    def listar_csvs(self, carpeta: str) -> list[str]:
        """
        Devuelve las rutas de todos los .csv en 'carpeta'.
        Wagner: usa esto para poblar un Combobox o Listbox con archivos disponibles.
        """
        if not os.path.isdir(carpeta):
            return []
        return [
            os.path.join(carpeta, f)
            for f in sorted(os.listdir(carpeta))
            if f.lower().endswith(".csv")
        ]
