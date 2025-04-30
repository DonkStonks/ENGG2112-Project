import pandas as pd

df_harvest = pd.read_csv('h5_i2_2019-2022_hand_harvest.csv')
df_weather = pd.read_csv('h5-i2_2016-2021_daily-weather.csv')
print("Columns in df_harvest:", df_harvest.columns)

print(f"Before consolidating to years with weather data: {len(df_harvest)}")
print(f"After consolidating to years with weather data: {len(df_harvest)}")

#df_harvest.to_csv('./datasets/h5-i2_2016-2021_daily_harvest_cleaned.csv', index=False)