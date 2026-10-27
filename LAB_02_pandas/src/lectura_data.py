

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def cargar_tablas() -> dict[str, pd.DataFrame]:
    """Lee y retorna las tres tablas del laboratorio."""

    return {
        "tbl0": pd.read_csv(DATA_DIR / "tbl0.tsv", sep="\t"),
        "tbl1": pd.read_csv(DATA_DIR / "tbl1.tsv", sep="\t"),
        "tbl2": pd.read_csv(DATA_DIR / "tbl2.tsv", sep="\t"),
    }


TABLAS = cargar_tablas()
tbl0 = TABLAS["tbl0"]
tbl1 = TABLAS["tbl1"]
tbl2 = TABLAS["tbl2"]