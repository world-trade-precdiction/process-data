import pandas as pd
from pandas_datareader import wb
import pycountry

# 연도 범위 설정
start_year = 2000
end_year = 2023

# 인디케이터: 도시 인구, 농촌 인구
indicators = {
    'urban_population': 'SP.URB.TOTL',
    'rural_population': 'SP.RUR.TOTL'
}

# 도시 인구 수
urban = wb.download(indicator=indicators['urban_population'], country='all', start=start_year, end=end_year)
urban = urban.reset_index()
urban.rename(columns={indicators['urban_population']: 'urban_population'}, inplace=True)

# 농촌 인구 수
rural = wb.download(indicator=indicators['rural_population'], country='all', start=start_year, end=end_year)
rural = rural.reset_index()
rural.rename(columns={indicators['rural_population']: 'rural_population'}, inplace=True)

# 도시/농촌 데이터 병합 (iso_code 제외)
merged = pd.merge(urban, rural, on=['country', 'year'], how='outer')
# ISO 코드 붙이기 (alpha-3)
def get_iso_code(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None

merged['iso_code'] = merged['country'].apply(get_iso_code)

merged = merged[merged['iso_code'].notna()]
# 열 순서 정리
merged = merged[['country', 'iso_code', 'year', 'urban_population', 'rural_population']]

# 정렬
merged.sort_values(by=['country', 'year'], inplace=True)

# CSV 저장
merged.to_csv("urban_rural_population_2000_2023.csv", index=False, encoding='utf-8-sig')

print("✅ 'urban_rural_population_2000_2023.csv' 파일이 생성되었습니다.")
