from .lectura_data import DATA

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    resultado = {}

    for row in DATA:
        metrics = row[4]

        if not metrics:
            continue

        for elemento in metrics.split(","):
            clave, valor = elemento.split(":")
            resultado[clave] = resultado.get(clave, 0) + 1

    return dict(sorted(resultado.items()))

