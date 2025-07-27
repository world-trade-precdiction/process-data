import requests
import pandas as pd
from io import StringIO

url = "https://ourworldindata.org/grapher/annual-freshwater-withdrawals.csv" #csv 파일 위치
resp = requests.get(url) #데이터에 접근 요청
resp.raise_for_status() #상태 확인

df = pd.read_csv(StringIO(resp.text)) #csv 파일을 읽기

filtered_df = df[(df["Year"] >= 2000) & (df["Year"] <= 2023)] #2000년부터 2023년까지로 한정
filtered_df_pivot = filtered_df.pivot(index = 'Entity', columns = 'Year', values = 'Annual freshwater withdrawals, total (billion cubic meters)')
filtered_df_pivot.index.name = 'Country'
filtered_df_pivot.columns.name = 'Year' #국가별, 연도별로 정리
filtered_df_pivot.to_csv("annual_freshwater_withdrawals_2000_2021.csv", index=True, index_label="Country", encoding="utf-8-sig") #csv 파일로 만들기
