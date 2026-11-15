import pandas as pd
import numpy as np
from pathlib import Path


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    lab_dir = Path(__file__).resolve().parents[1]
    frames = []

    for channel in ("letter", "web"):
        path = lab_dir / "data" / f"historical_requests_{channel}.csv.gz"
        data = pd.read_csv(path).drop_duplicates()
        data["channel"] = channel
        data["in_date"] = pd.to_datetime(data["in_date"])
        data["out_date"] = pd.to_datetime(data["out_date"])
        data["year"] = data["in_date"].dt.year
        data["answered"] = data["out_date"].notna()
        data["business_days"] = pd.NA
        data["calendar_days"] = pd.NA

        answered = data["answered"]
        entry_dates = data.loc[answered, "in_date"].dt.date.astype(str)
        response_dates = data.loc[answered, "out_date"].dt.date.astype(str)
        data.loc[answered, "business_days"] = np.busday_count(
            entry_dates.to_numpy(dtype="datetime64[D]") + np.timedelta64(1, "D"),
            response_dates.to_numpy(dtype="datetime64[D]") + np.timedelta64(1, "D"),
        )
        data.loc[answered, "calendar_days"] = (
            data.loc[answered, "out_date"] - data.loc[answered, "in_date"]
        ).dt.days
        data["on_time"] = data["answered"] & (data["business_days"] <= 15)
        frames.append(data)

    requests = pd.concat(frames, ignore_index=True)
    submission_dir = lab_dir / "submission"
    submission_dir.mkdir(exist_ok=True)

    channel_summary = (
        requests.groupby("channel", sort=True)
        .agg(
            requests=("channel", "size"),
            answered=("answered", "sum"),
            pending=("answered", lambda values: (~values).sum()),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )
    channel_summary.to_csv(submission_dir / "channel_summary.csv", index=False)

    yearly_summary = (
        requests.groupby(["year", "channel"], sort=True)
        .agg(
            requests=("channel", "size"),
            pending=("answered", lambda values: (~values).sum()),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )
    yearly_summary.to_csv(submission_dir / "yearly_summary.csv", index=False)

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    entry_day_summary = (
        requests.groupby("day_name", sort=False)
        .agg(
            requests=("day_name", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .reindex(day_order)
        .reset_index()
    )
    entry_day_summary.to_csv(
        submission_dir / "entry_day_summary.csv",
        index=False,
    )

    return channel_summary, yearly_summary, entry_day_summary

pregunta_01()