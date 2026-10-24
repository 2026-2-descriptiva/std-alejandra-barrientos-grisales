from .lectura_data import DATA

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    resultado = {}

    for row in DATA:
        metrics = row[4]

        if not metrics:
            continue

        for elemento in metrics.split(","):
            clave, valor = elemento.split(":")
            valor = int(valor)

            if clave not in resultado:
                resultado[clave] = [valor, valor]
            else:
                resultado[clave][0] = min(resultado[clave][0], valor)
                resultado[clave][1] = max(resultado[clave][1], valor)

    return [
        (clave, minimo, maximo)
        for clave, (minimo, maximo) in sorted(resultado.items())
    ]

