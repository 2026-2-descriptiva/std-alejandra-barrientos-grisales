from .lectura_data import DATA

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    resultado = {}

    for letter, value, *_ in DATA:
        resultado[letter] = resultado.get(letter, 0) + 1

    return sorted(resultado.items())
