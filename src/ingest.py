import pandas as pd

BASE_URL = "https://data.open-power-system-data.org/time_series"
VERSION = "2020-10-06"

DATA_URL = f"{BASE_URL}/{VERSION}/time_series_60min_singleindex.csv"

print(df.shape)
print(df.columns)
print(df.head())
