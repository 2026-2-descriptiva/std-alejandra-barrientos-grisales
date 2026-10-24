from .lectura_data import DATA

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    resultado = []

    for row in DATA:
        letter = row[0]
        codes = row[3]
        metrics = row[4]

        cantidad_codes = len(codes.split(","))
        cantidad_metrics = len(metrics.split(",")) if metrics else 0

        resultado.append((letter, cantidad_codes, cantidad_metrics))

    return resultado
