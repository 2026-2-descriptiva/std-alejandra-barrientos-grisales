import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    lab_dir = Path(__file__).resolve().parents[1]
    sales = pd.read_csv(lab_dir / "data" / "sales.csv.gz")
    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])
    sales = sales.dropna(subset=["CustomerID", "OrderDate"])

    sales["order_month"] = sales["OrderDate"].dt.to_period("M")
    first_purchase = sales.groupby("CustomerID")["order_month"].transform("min")
    sales["cohort_month"] = first_purchase
    sales["period_index"] = (
        sales["order_month"].dt.year * 12
        + sales["order_month"].dt.month
        - sales["cohort_month"].dt.year * 12
        - sales["cohort_month"].dt.month
    )

    retention = (
        sales.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .rename("active_customers")
        .reset_index()
    )
    cohort_sizes = (
        retention[retention["period_index"] == 0]
        .loc[:, ["cohort_month", "active_customers"]]
        .rename(columns={"active_customers": "cohort_size"})
    )
    retention = retention.merge(cohort_sizes, on="cohort_month", how="left")
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    )
    retention["cohort_month"] = retention["cohort_month"].astype(str)
    retention = retention[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ].sort_values(["cohort_month", "period_index"])

    submission_dir = lab_dir / "submission"
    submission_dir.mkdir(exist_ok=True)
    retention.to_csv(
        submission_dir / "cohort_retention.csv",
        index=False,
    )

    heatmap = retention.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate",
    ).sort_index()
    figure_width = max(8, heatmap.shape[1] * 0.6)
    figure_height = max(4, heatmap.shape[0] * 0.35)
    figure, axis = plt.subplots(figsize=(figure_width, figure_height))
    image = axis.imshow(
        heatmap,
        aspect="auto",
        cmap="YlGnBu",
        vmin=0,
        vmax=1,
    )
    axis.set_xticks(range(len(heatmap.columns)))
    axis.set_xticklabels(heatmap.columns)
    axis.set_yticks(range(len(heatmap.index)))
    axis.set_yticklabels(heatmap.index)
    axis.set_xlabel("Meses desde la primera compra")
    axis.set_ylabel("Mes de cohorte")
    figure.colorbar(image, ax=axis, format=lambda value, _: f"{value:.0%}")

    for row_index, row in enumerate(heatmap.index):
        for column_index, column in enumerate(heatmap.columns):
            value = heatmap.loc[row, column]
            if pd.notna(value):
                axis.text(
                    column_index,
                    row_index,
                    f"{value:.0%}",
                    ha="center",
                    va="center",
                )

    figure.tight_layout()
    figure.savefig(submission_dir / "cohort_retention_heatmap.png")
    plt.close(figure)

    return retention

build_cohort_analysis()