from .lectura_data import DATA

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    resultado = {}

    for letter, value, *_ in DATA:
        value = int(value)

        if value not in resultado:
            resultado[value] = set()

        resultado[value].add(letter)

    return [
        (valor, sorted(letras))
        for valor, letras in sorted(resultado.items())
    ]