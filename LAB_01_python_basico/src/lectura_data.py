import csv
import gzip
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

with gzip.open(DATA_PATH, mode="rt", newline="") as data_file:
    DATA = tuple(csv.reader(data_file, delimiter="\t"))