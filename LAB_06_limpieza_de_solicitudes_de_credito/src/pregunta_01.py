
from pathlib import Path
import pandas as pd


def lectura_solicitudes():
    activity_dir = Path(__file__).resolve().parents[1]
    solicitudes_path = activity_dir / "data" / "solicitudes_de_credito.csv.gz"

    solicitudes_creditos = pd.read_csv(
        solicitudes_path,
        sep=";",
        index_col=0,
        compression="gzip",
        encoding="utf-8"
    )

    solicitudes_creditos.columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito"
    ]

    return solicitudes_creditos


def seleccionar_columnas(df):
    columnas = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito"
    ]

    return df[columnas].copy()


def limpiar_textos(df):
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "comuna_ciudadano",
        "línea_credito"
    ]

    for columna in columnas_texto:
        df[columna] = (
            df[columna]
            .astype("string")
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.replace("_", " ", regex=False)
            .apply(lambda s: " ".join(s.split()) if pd.notna(s) else s)
        )

        df[columna] = df[columna].replace("", pd.NA)

    return df


def limpiar_numeros(df):
    df["estrato"] = pd.to_numeric(df["estrato"], errors="coerce")

    def limpiar_monto(valor):
        if pd.isna(valor):
            return pd.NA

        valor = str(valor).replace("$", "").replace(",", "").strip()
        return pd.to_numeric(valor, errors="coerce")

    df["monto_del_credito"] = df["monto_del_credito"].apply(limpiar_monto)

    return df


def limpiar_fechas(df):
    def limpiar_fecha(valor):
        if pd.isna(valor):
            return pd.NA

        partes = str(valor).strip().replace("-", "/").split("/")

        if len(partes) == 3:
            if len(partes[0]) == 4:
                anio, mes, dia = partes
            else:
                dia, mes, anio = partes

            return f"{int(anio):04d}-{int(mes):02d}-{int(dia):02d}"

        return pd.NA

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(limpiar_fecha)

    return df


def eliminar_incompletos(df):
    columnas_obligatorias = [
        columna for columna in df.columns
        if columna != "comuna_ciudadano"
    ]

    return df.dropna(subset=columnas_obligatorias)


def convertir_enteros(df):
    columnas_numericas = ["estrato", "monto_del_credito"]

    for columna in columnas_numericas:
        df[columna] = df[columna].astype(int)

    return df


def eliminar_duplicados(df):
    return df.drop_duplicates()


def guardar_solicitudes(df):
    activity_dir = Path(__file__).resolve().parents[1]
    submission_dir = activity_dir / "submission"

    submission_dir.mkdir(parents=True, exist_ok=True)

    output_path = submission_dir / "solicitudes_de_credito.csv"

    df.to_csv(output_path, sep=";", index=False)


def pregunta_01():
    df = lectura_solicitudes()

    df = seleccionar_columnas(df)
    df = limpiar_textos(df)
    df = limpiar_numeros(df)
    df = limpiar_fechas(df)
    df = eliminar_incompletos(df)
    df = convertir_enteros(df)
    df = eliminar_duplicados(df)

    guardar_solicitudes(df)

    return df




    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

 

pregunta_01()