import polars as pl





overrides = {"rok_produkcji": pl.String}
df = pl.read_csv('data/batch/pojazdy_10_2022-04-17.csv', schema_overrides=overrides)

result = df.sort('data_pierwszej_rej', nulls_last=True)
print(result.select(["pojazd_id","marka","data_pierwszej_rej"]).head(5))


