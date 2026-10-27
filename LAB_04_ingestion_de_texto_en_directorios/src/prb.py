import pandas as pd
import os
from pathlib import Path

def pregunta_01():
    base_path = Path(__file__).resolve().parents[1]
    data_path = base_path / "data"
    submission_path = base_path / "submission"
    submission_path.mkdir(parents=True, exist_ok=True)

    for division in ["train", "test"]:
        registros = []

        division_path = data_path / division

        # Recorrer las carpetas de sentimientos en orden alfabético
        with os.scandir(division_path) as carpetas:
            carpetas = sorted(
                [c for c in carpetas if c.is_dir()],
                key=lambda c: c.name
            )

        for carpeta in carpetas:
            # Recorrer directamente los archivos de cada carpeta
            with os.scandir(carpeta.path) as archivos:
                archivos = sorted(
                    [a for a in archivos if a.is_file() and a.name.endswith(".txt")],
                    key=lambda a: a.name
                )

            for archivo in archivos:
                with open(archivo.path, "r", encoding="utf-8") as f:
                    frase = f.read().strip()

                registros.append((frase, carpeta.name))

        dataset = pd.DataFrame(registros, columns=["phrase", "target"])
        dataset.to_csv(
            submission_path / f"{division}_dataset.csv",
            index=False
        )

pregunta_01()