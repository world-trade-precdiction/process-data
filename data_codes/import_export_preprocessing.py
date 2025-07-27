import pandas as pd
df = pd.read_csv("comtrade_merged_export_2000_2023.csv")
processed_food = list(range(16, 25))
raw_materials = list(range(1, 16)) + list(range(25, 28)) + list(range(44, 50))
tech_intensive_products = list(range(84, 93))
unprocessed_materials = list(range(28, 41)) + list(range(72, 84)) #항목별 hs_code 저장

filtered_df = df[(df["refPeriodId"] >= 2000) & (df["refPeriodId"] <= 2021)] #연도 범위

df_pivot = filtered_df.pivot(index='reporterISO', columns=['refPeriodId', 'isOriginalClassification', 'flowCode'], values='fobvalue')
df_pivot.columns.names = ["year", "hs_code", "import_or_export"]
df_pivot = df_pivot.sort_index(axis=1, level=["year", "import_or_export"]) #국가별 정리

filtered_processed_food = df_pivot.loc[:, df_pivot.columns.get_level_values("hs_code").isin(processed_food)]
summed_processed_food = filtered_processed_food.groupby(level=["year", "import_or_export"], axis=1).sum()
summed_processed_food = summed_processed_food.sort_index(axis=1, level=["year", "import_or_export"])
summed_processed_food.to_csv("comtrade_merged_export_2000_2021_processed_food.csv", index=True, index_label='Country', encoding="utf-8-sig")

filtered_raw_materials = df_pivot.loc[:, df_pivot.columns.get_level_values("hs_code").isin(raw_materials)]
summed_raw_materials = filtered_raw_materials.groupby(level=["year", "import_or_export"], axis=1).sum()
summed_raw_materials = summed_raw_materials.sort_index(axis=1, level=["year", "import_or_export"])
summed_raw_materials.to_csv("comtrade_merged_export_2000_2021_raw_materials.csv", index=True, index_label='Country', encoding="utf-8-sig")

filtered_tech_intensive_products = df_pivot.loc[:, df_pivot.columns.get_level_values("hs_code").isin(tech_intensive_products)]
summed = filtered_tech_intensive_products.groupby(level=["year", "import_or_export"], axis=1).sum()
summed = summed.sort_index(axis=1, level=["year", "import_or_export"])
summed.to_csv("comtrade_merged_export_2000_2021_tech_intensive_products.csv", index=True, index_label='Country', encoding="utf-8-sig")

filtered_unprocessed_materials = df_pivot.loc[:, df_pivot.columns.get_level_values("hs_code").isin(unprocessed_materials)]
summed = filtered_unprocessed_materials.groupby(level=["year", "import_or_export"], axis=1).sum()
summed = summed.sort_index(axis=1, level=["year", "import_or_export"])
summed.to_csv("comtrade_merged_export_2000_2021_unprocessed_materials.csv", index=True, index_label='Country', encoding="utf-8-sig")
#항목별로 csv 각각 만들기
