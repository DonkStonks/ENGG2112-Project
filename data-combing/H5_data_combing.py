import pandas as pd
from pathlib import Path
import os
#print(os.getcwd())
#print(__file__)
#print(Path(__file__).parent)

# Load the data
df_harvest = pd.read_csv(Path(__file__).parent / 'h5_i2_2019-2022_hand_harvest.csv')
df_weather = pd.read_csv(Path(__file__).parent / 'h5-i2_2016-2021_daily-weather.csv')
#print("Columns in df_harvest:", df_harvest.columns)

# Print the initial lengths of the DataFrames
print(f"Before consolidating to years with weather data: {len(df_harvest)}")

# Filter df_harvest for specific years
df_harvest = df_harvest[df_harvest['Year'].isin([2019, 2020, 2021])]
df_harvest.dropna()
# Keep only the necessary columns in df_harvest
Col_Harvest = ['DoY', 'Year', "Crop", "Treatment","Site", 'Grain_yield_kg_ha', 'Stover_g_m2', 'Harvest_index']
df_harvest = df_harvest[Col_Harvest]

print(f"After consolidating to years with weather data: {len(df_harvest)}")

#print("Columns in df_weather:", df_weather.columns)
# Keep only the necessary columns in df_weather
col_weather = ['Year', 'FIeld', 'Crop', 'DoY', 'Sol_Rad_MJ_m2_d',
       'T_min_C', 'T_max_C', 'PCPN_mm_d', 'RH_f', 'Wind_spd_m_s']
df_weather = df_weather[col_weather]

# Add a new column to extract the first two letters of Site and FIeld
df_harvest['Site_Prefix'] = df_harvest['Site'].str[:2]

# Merge the two DataFrames on Year, DoY, Crop, and the first two letters of Site and FIeld
df_combi = pd.merge(
    df_harvest,
    df_weather,
    left_on=['Year', 'DoY', 'Crop', 'Site_Prefix'],
    right_on=['Year', 'DoY', 'Crop', 'FIeld'],
    how='inner'
)

# Drop the temporary prefix columns
df_combi.drop(columns=['Site_Prefix'], inplace=True)

# Print the resulting DataFrame
print(f"After merging: {len(df_combi)} rows")

#print("Columns in df_combi:", df_combi.columns)
combi_columns = ["Year",'Crop', 'Treatment',
       'Grain_yield_kg_ha', 'Stover_g_m2', 'Harvest_index',
       'Sol_Rad_MJ_m2_d', 'T_min_C', 'T_max_C', 'PCPN_mm_d', 'RH_f',
       'Wind_spd_m_s']

df_combi.to_csv('./datasets/h5-i2_2016-2021_daily_harvest_cleaned.csv', index=False)