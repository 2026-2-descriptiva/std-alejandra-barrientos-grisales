from .lectura_data import DATA

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    resultado = {}

    for row in DATA:
        letra = row[0]
        metrics = row[4]
        suma = 0

        if metrics:
            for elemento in metrics.split(","):
                clave, valor = elemento.split(":")
                suma += int(valor)

        resultado[letra] = resultado.get(letra, 0) + suma

    return dict(sorted(resultado.items()))
