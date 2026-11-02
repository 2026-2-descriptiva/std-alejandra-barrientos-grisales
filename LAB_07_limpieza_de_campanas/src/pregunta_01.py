import pandas as pd


from pathlib import Path


def lectura_datos():
    activity_dir = Path(__file__).resolve().parents[1]
    data_dir = activity_dir / "data"

    archivos = sorted(data_dir.glob("bank-marketing-campaing-*.csv.gz"))

    df = pd.concat(
        [pd.read_csv(archivo, compression="gzip") for archivo in archivos],
        ignore_index=True
    )

    return df

def guardar_csv(df, nombre_archivo):
    activity_dir = Path(__file__).resolve().parents[1]
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        submission_dir / nombre_archivo,
        index=False
    )

def crear_tabla_client(df):
 

    columnas = [
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage"
    ]

    df = df[columnas].copy()

    
    df["job"] = (
        df["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    df["education"] = (
        df["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )

    for columna in ["credit_default", "mortgage"]:
        df[columna] = (df[columna] == "yes").astype(int)

    guardar_csv(df, "client.csv")

    return df

def crear_tabla_campaign(df):

    columnas = [
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "month",
        "day"
    ]

    df = df[columnas].copy()

    df["previous_outcome"] = (
        df["previous_outcome"] == "success"
    ).astype(int)


    df["campaign_outcome"] = (
        df["campaign_outcome"] == "yes"
    ).astype(int)

    meses = {
        "jan": "01", "feb": "02", "mar": "03",
        "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09",
        "oct": "10", "nov": "11", "dec": "12"
    }

    df["month"] = df["month"].str.lower().map(meses)

    df["last_contact_date"] = pd.to_datetime(
        "2022-" + df["month"] + "-" + df["day"].astype(str).str.zfill(2),
        format="%Y-%m-%d",
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")


    df = df.drop(columns=["month", "day"])

    df = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "last_contact_date"
        ]
    ]

    guardar_csv(df, "campaign.csv")

    return df

def crear_tabla_economics(df):

    columnas = [
        "client_id",
        "cons_price_idx",
        "euribor_three_months"
    ]

    df = df[columnas].copy()

    guardar_csv(df, "economics.csv")

    return df



def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """
    df = lectura_datos()
    client = crear_tabla_client(df)
    campaign = crear_tabla_campaign(df)
    economics = crear_tabla_economics(df)

    return client, campaign, economics

clean_campaign_data()

