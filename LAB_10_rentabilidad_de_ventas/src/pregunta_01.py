import pandas as pd
from pathlib import Path

#def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
"""
Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    data/superstore_orders.csv.gz tiene una fila por línea de pedido, con
    el número de pedido (Order ID), las ventas (Sales), la utilidad
    (Profit), el descuento aplicado (Discount, como proporción), el
    segmento del cliente (Customer Segment) y la categoría del producto
    (Product Category). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (profit_margin): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - loss_line_rate: la proporción de líneas con pérdida.
    - lost_profit: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (discount_band): 0% si no hubo descuento,
      1%-5% si fue mayor que 0 y hasta 5 %, 6%-10% si fue mayor que 5 % y
      hasta 10 %, y más de 10% en otro caso.

    Genere tres archivos en submission/, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. profitability_summary.csv, con una sola fila: lines (cantidad de
       líneas), orders (pedidos distintos), sales, profit,
       profit_margin, loss_lines (cantidad de líneas con pérdida),
       loss_line_rate y lost_profit.

    2. discount_summary.csv, con una fila por rango de descuento, en el
       orden en que se definieron arriba: discount_band, lines, sales,
       profit, profit_margin, loss_line_rate y lost_profit.

    3. priority_segments.csv, con los cinco segmentos segmento–categoría
       que más utilidad pierden: Customer Segment, Product Category,
       lines, sales, profit, profit_margin y lost_profit. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       lost_profit de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de discount_summary.csv:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
"""
def cargar_datos():

    DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "superstore_orders.csv.gz"

    df = pd.read_csv(
        DATA_PATH,
        compression="gzip",
        sep=";",
        decimal=","
    )

    return df


def preparar_datos(df):

    df["is_loss"] = df["Profit"] < 0

    df["lost_profit"] = (-df["Profit"]).where(df["is_loss"], 0)

    df["discount_band"] = "más de 10%"

    df.loc[df["Discount"] == 0, "discount_band"] = "0%"

    df.loc[
        (df["Discount"] > 0) & (df["Discount"] <= 0.05),
        "discount_band"
    ] = "1%-5%"

    df.loc[
        (df["Discount"] > 0.05) & (df["Discount"] <= 0.10),
        "discount_band"
    ] = "6%-10%"

    orden_descuentos = ["0%", "1%-5%", "6%-10%", "más de 10%"]

    df["discount_band"] = pd.Categorical(
        df["discount_band"],
        categories=orden_descuentos,
        ordered=True
    )

    return df

def calcular_indicadores(grupo):

    sales = grupo["Sales"].sum()
    profit = grupo["Profit"].sum()

    return pd.Series({
        "lines": len(grupo),
        "sales": sales,
        "profit": profit,
        "profit_margin": profit / sales if sales != 0 else 0,
        "loss_line_rate": grupo["is_loss"].mean(),
        "lost_profit": grupo["lost_profit"].sum()
    })


def crear_profitability_summary(df):

    sales = df["Sales"].sum()
    profit = df["Profit"].sum()

    profitability_summary = pd.DataFrame([{
        "lines": len(df),
        "orders": df["Order ID"].nunique(),
        "sales": sales,
        "profit": profit,
        "profit_margin": profit / sales if sales != 0 else 0,
        "loss_lines": df["is_loss"].sum(),
        "loss_line_rate": df["is_loss"].mean(),
        "lost_profit": df["lost_profit"].sum()
    }])

    return profitability_summary


def crear_discount_summary(df):

    discount_summary = (
        df.groupby("discount_band", observed=False)
        .apply(calcular_indicadores, include_groups=False)
        .reset_index()
    )

    discount_summary = discount_summary[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit"
        ]
    ]

    return discount_summary


def crear_priority_segments(df):

    priority_segments = (
        df.groupby(
            ["Customer Segment", "Product Category"],
            dropna=False
        )
        .apply(calcular_indicadores, include_groups=False)
        .reset_index()
    )


    priority_segments = priority_segments[
        priority_segments["lines"] >= 100
    ]


    priority_segments = (
        priority_segments
        .sort_values("lost_profit", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    priority_segments = priority_segments[
        [
            "Customer Segment",
            "Product Category",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "lost_profit"
        ]
    ]

    return priority_segments


def guardar_archivos(
    profitability_summary,
    discount_summary,
    priority_segments
):


    BASE_PATH = Path(__file__).resolve().parents[1]

   
    output_path = BASE_PATH / "submission"
    output_path.mkdir(parents=True, exist_ok=True)

  
    profitability_summary.to_csv(
        output_path / "profitability_summary.csv",
        index=False
    )

    discount_summary.to_csv(
        output_path / "discount_summary.csv",
        index=False
    )

    priority_segments.to_csv(
        output_path / "priority_segments.csv",
        index=False
    )

    print("Archivos guardados correctamente en:", output_path)

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    # Cargar y preparar datos
    df = cargar_datos()
    df = preparar_datos(df)

    # Crear las tres tablas
    profitability_summary = crear_profitability_summary(df)
    discount_summary = crear_discount_summary(df)
    priority_segments = crear_priority_segments(df)

    # Guardar archivos
    guardar_archivos(
        profitability_summary,
        discount_summary,
        priority_segments
    )

    # Retornar las tres tablas
    return (
        profitability_summary,
        discount_summary,
        priority_segments
    )


resultado = pregunta_01()
