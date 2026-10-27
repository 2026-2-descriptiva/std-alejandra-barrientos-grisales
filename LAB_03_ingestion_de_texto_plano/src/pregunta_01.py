import pandas as pd
import re
from pathlib import Path

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    data_path = Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"

    registros = []
    cluster_actual = None
    palabras_clave = []

    with open(data_path, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            coincidencia = re.match(
                r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$",
                linea
            )

            if coincidencia:
                if cluster_actual is not None:
                    texto = re.sub(
                        r"\s+", " ", " ".join(palabras_clave)
                    ).strip()
                    palabras = [
                        palabra.strip()
                        for palabra in texto.split(",")
                        if palabra.strip()
                    ]
                    if palabras:
                        palabras[-1] = palabras[-1].rstrip(".")

                    cluster_actual["principales_palabras_clave"] = ", ".join(palabras)
                    registros.append(cluster_actual)

                cluster_actual = {
                    "cluster": int(coincidencia.group(1)),
                    "cantidad_de_palabras_clave": int(coincidencia.group(2)),
                    "porcentaje_de_palabras_clave": float(
                        coincidencia.group(3).replace(",", ".")
                    ),
                }

                palabras_clave = [coincidencia.group(4).strip()]

            elif cluster_actual is not None and linea.strip():
                if not set(linea.strip()) == {"-"}:
                    palabras_clave.append(linea.strip())

    if cluster_actual is not None:
        texto = re.sub(
            r"\s+", " ", " ".join(palabras_clave)
        ).strip()
        palabras = [
            palabra.strip()
            for palabra in texto.split(",")
            if palabra.strip()
        ]
        if palabras:
            palabras[-1] = palabras[-1].rstrip(".")

        cluster_actual["principales_palabras_clave"] = ", ".join(palabras)
        registros.append(cluster_actual)

    return pd.DataFrame(registros, columns=[
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ])