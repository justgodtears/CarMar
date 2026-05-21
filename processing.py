import pandas as pd

PATH = "data/raw/vehicles.csv"

df = pd.read_csv("data/raw/vehicles.csv")
print(df.head())