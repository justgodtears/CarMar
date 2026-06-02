"""Process batch data from parquet"""
import polars as pl
from datetime import date
import sqlite3


# This is testing data, for prod, we gonna use whole file
uri = "sqlite:///data/database/cardata.db"
#schema_overrides = {"rok_produkcji":pl.String, "data_pierwszej_rej": pl.Date}


df = pl.read_parquet("data/preprocessed/batch_data.parquet")

# Filtering data to cars only
only_cars = df.filter(pl.col("rodzaj") == "SAMOCHÓD OSOBOWY")

# Saving as table (date is converted to a string to optimize table creation)
if "data_pierwszej_rej" in only_cars.columns:
    only_cars = only_cars.with_columns(pl.col("data_pierwszej_rej").cast(pl.String))

only_cars.write_database(
    table_name="only_cars",
    connection=uri,
    if_table_exists="replace",
    engine="adbc"
)

