from .lectura_data import DATA

def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    resultado = {}

    for row in DATA:
        value = int(row[1])
        codes = row[3]

        if not codes:
            continue

        for letra in codes.split(","):
            resultado[letra] = resultado.get(letra, 0) + value

    return dict(sorted(resultado.items()))
