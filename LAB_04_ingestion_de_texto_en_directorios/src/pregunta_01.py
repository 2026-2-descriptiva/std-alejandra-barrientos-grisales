import pandas as pd
from pathlib import Path

def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

   


    base_path = Path(__file__).resolve().parents[1]
    data_path = base_path / "data"
    submission_path = base_path / "submission"

    submission_path.mkdir(parents=True, exist_ok=True)

    for division in ["train", "test"]:
        registros = []
        division_path = data_path / division

        # Recorrer las carpetas de sentimientos en orden alfabético
        carpetas = sorted(
            carpeta for carpeta in division_path.iterdir()
            if carpeta.is_dir()
        )

        for carpeta in carpetas:
            # Recorrer los archivos .txt en orden alfabético
            archivos = sorted(carpeta.rglob("*.txt"))

            for archivo in archivos:
                frase = archivo.read_text(encoding="utf-8").strip()

                registros.append({
                    "phrase": frase,
                    "target": carpeta.name
                })

        # Construir el DataFrame con Pandas
        dataset = pd.DataFrame(
            registros,
            columns=["phrase", "target"]
        )

        # Guardar el CSV sin índice
        ruta_salida = submission_path / f"{division}_dataset.csv"
        dataset.to_csv(ruta_salida, index=False)


pregunta_01()