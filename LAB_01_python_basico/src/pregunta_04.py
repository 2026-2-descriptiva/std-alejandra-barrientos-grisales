from .lectura_data import DATA

def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    resultado = {}

    for row in DATA:
        mes = row[2].split("-")[1]
        resultado[mes] = resultado.get(mes, 0) + 1

    return sorted(resultado.items())
