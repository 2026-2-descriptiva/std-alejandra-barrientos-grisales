from pathlib import Path
import json
import pandas as pd


def lectura_ventas():
  activity_dir = Path(__file__).resolve().parents[1]
  ventas_path = activity_dir / "data" / "ventas.csv.gz"

  ventas = pd.read_csv(ventas_path)

  return ventas


def normalizacion_col_ventas(ventas):
  ventas.columns = (
      ventas.columns.str.strip()  # Eliminar espacios al inicio y al final
      .str.lower()  # Pasar a minúsculas
      .str.replace(" ", "_")  # Reemplazar espacios internos por guiones bajos
  )

  return ventas


def contar_filas(ventas):
  return int(ventas.shape[0])


def contar_columnas(ventas):
  return int(ventas.shape[1])



def contar_columnas_faltantes(ventas, columnas_requeridas):
  return sorted(set(columnas_requeridas) - set(ventas.columns))


def columnas_no_requeridas(ventas, columnas_requeridas):
  return sorted(set(ventas.columns) - set(columnas_requeridas))


def cantidad_filas_duplicadas(ventas):
  return int(ventas.duplicated().sum())


def cantidad_filas_supplier_id_duplicadas(ventas):
  return int(ventas.duplicated(subset=["supplier_id"], keep=False).sum())

def datos_faltantes_por_columna(ventas):
    
  valores = ventas.astype("string")
  faltantes = ventas.isna() | valores.apply(
    lambda columna: columna.str.strip().isin(["", "N/A"])
  )
  return {columna: int(cantidad) for columna, cantidad in faltantes.sum().items()}


def cantidad_correo_electronico_invalido(ventas):
  correos_validos = ventas["contact_email"].astype("string").str.match(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$", na=False
  )
  return int((~correos_validos).sum())

def cantidad_unidades_invalidas(ventas):
  units = ventas["units"].dropna()

  return int(((units <= 0) | (units % 1 != 0)).sum())


def valores_country(ventas):
  return sorted(ventas["country"].dropna().unique().tolist())

def guardar_reporte(reporte):
  submission_dir = Path(__file__).resolve().parents[1] / "submission"
  submission_dir.mkdir(parents=True, exist_ok=True)
  reporte_path = submission_dir / "data_quality_report.json"

  with reporte_path.open("w", encoding="utf-8") as archivo:
    json.dump(reporte, archivo, ensure_ascii=False, indent=2)



def main():
    columnas_requeridas = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]

    ventas = normalizacion_col_ventas(lectura_ventas())
    row_count = contar_filas(ventas)
    column_count = contar_columnas(ventas)
    missing_required_columns = contar_columnas_faltantes(ventas, columnas_requeridas)
    unexpected_columns = columnas_no_requeridas(ventas, columnas_requeridas)
    duplicate_row_count = cantidad_filas_duplicadas(ventas)
    duplicate_supplier_id_row_count = cantidad_filas_supplier_id_duplicadas(ventas)
    missing_value_count_by_column = datos_faltantes_por_columna(ventas)
    invalid_email_count = cantidad_correo_electronico_invalido(ventas)
    invalid_unit_count = cantidad_unidades_invalidas(ventas)
    country_values = valores_country(ventas)
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    resultados = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values,
    }

    guardar_reporte(resultados)
    return resultados

main()
