import requests
import pandas as pd
from io import StringIO

url = "https://ourworldindata.org/grapher/annual-freshwater-withdrawals.csv"
resp = requests.get(url)
resp.raise_for_status()

df = pd.read_csv(StringIO(resp.text))

filtered_df = df[(df["Year"] >= 2000) & (df["Year"] <= 2023)]
filtered_df_pivot = filtered_df.pivot(index = 'Entity', columns = 'Year', values = 'Annual freshwater withdrawals, total (billion cubic meters)')
filtered_df_pivot.index.name = 'Country'
filtered_df_pivot.columns.name = 'Year'
filtered_df_pivot.to_csv("annual_freshwater_withdrawals_2000_2021.csv", index=True, index_label="Country", encoding="utf-8-sig")