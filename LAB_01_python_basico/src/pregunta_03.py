from .lectura_data import DATA


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    resultado = {}
    for letter, value, *_ in DATA:
        resultado[letter] = resultado.get(letter, 0) + int(value)

    return sorted(resultado.items())