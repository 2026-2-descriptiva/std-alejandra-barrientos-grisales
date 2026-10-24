from .lectura_data import DATA

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    resultado = {}

    for letter, value, *_ in DATA:
        value = int(value)

        if letter not in resultado:
            resultado[letter] = [value, value]
        else:
            resultado[letter][0] = max(resultado[letter][0], value)
            resultado[letter][1] = min(resultado[letter][1], value)

    return [
        (letter, maximo, minimo)
        for letter, (maximo, minimo) in sorted(resultado.items())
    ]
