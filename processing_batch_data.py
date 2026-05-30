import polars as pl
import sqlite3


# This is testing data, for prod, we gonna use whole file
uri = "sqlite://data/database/cardata.db"
PATH = "data/batch/pojazdy_10_2022-04-17.csv"
schema_overrides = {"rok_produkcji":pl.String, "data_pierwszej_rej": pl.Date}



df = pl.read_csv(PATH, schema_overrides=schema_overrides)

result = df.filter(pl.col("data_pierwszej_rej") > pl.date(2000,1,1))
result.write_database(
    table_name="pojazdy_10_2022-04-17_testing",
    connection=uri,
    engine="adbc",
    if_table_exists="replace",
)
