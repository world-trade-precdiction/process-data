import pandas as pd
from pandas_datareader import wb
import pycountry

start_year = 2000
end_year = 2021

indicators = {
    'urban_population': 'SP.URB.TOTL',
    'rural_population': 'SP.RUR.TOTL'
}

urban = wb.download(indicator=indicators['urban_population'], country='all', start=start_year, end=end_year)
urban = urban.reset_index()
urban.rename(columns={indicators['urban_population']: 'urban_population'}, inplace=True)

rural = wb.download(indicator=indicators['rural_population'], country='all', start=start_year, end=end_year)
rural = rural.reset_index()
rural.rename(columns={indicators['rural_population']: 'rural_population'}, inplace=True)

merged = pd.merge(urban, rural, on=['country', 'year'], how='outer')

def get_iso_code(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None

merged['iso_code'] = merged['country'].apply(get_iso_code)

merged = merged[merged['iso_code'].notna()]

merged = merged[['country', 'iso_code', 'year', 'urban_population', 'rural_population']]

merged.sort_values(by=['country', 'year'], inplace=True)

filtered_df_pivot = merged.pivot(index = 'country', columns = 'year', values = ['urban_population', 'rural_population'])
filtered_df_pivot.index.name = 'Country'
filtered_df_pivot.columns.name = 'Year'
filtered_df_pivot.to_csv("urban_rural_population_2000_2021.csv", index=True, index_label="Country", encoding="utf-8-sig")