import polars as pl
from datetime import date
import sqlite3


# This is testing data, for prod, we gonna use whole file
uri = "sqlite://data/database/cardata.db"
schema_overrides = {"rok_produkcji":pl.String, "data_pierwszej_rej": pl.Date}

df = pl.read_csv(
    "data/batch/*.csv",
    schema_overrides=schema_overrides,
)
result = df.filter(pl.col("data_pierwszej_rej") > date(2000, 1, 1))