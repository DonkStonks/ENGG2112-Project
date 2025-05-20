import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

#print(os.getcwd())

df = pd.read_csv(os.getcwd() + '\datasets\h5-i2_2016-2021_daily_harvest_cleaned.csv')

columns = ['Crop', 'Treatment',
       'Grain_yield_kg_ha', 
       'Sol_Rad_MJ_m2_d',  'T_max_C', 'RH_f',
       'Wind_spd_m_s']
df = df[columns]

df = df.rename(columns={
    'Grain_yield_kg_ha': 'Grain Yield (kg/ha)',
    'Stover_g_m2': 'Biomass Leftover (g/m2)',
    'Harvest_index': 'Harvest Index',
    'Sol_Rad_MJ_m2_d': 'Solar Radiation (MJ/m2/d)',
    'T_min_C': 'Min Temperature (C)',
    'T_max_C': 'Max Temperature (C)',
    'RH_f': 'Relative Humidity (%)',
    'Wind_spd_m_s': 'Wind Speed (m/s)'
})


print("hello_goodbye - World")

# Create a scatter plot matrix
sns.pairplot(df, diag_kind="kde",hue="Crop", palette="Set2", markers=["o", "s", "D", "P", "X"])
#sns.pairplot(df, diag_kind="kde", hue="Crop", palette="Set2", markers=["o", "s", "D", "P", "X"], plot_kws={'alpha': 0.5})
#sns.pairplot(df, diag_kind='kde', corner=True)

# Show the plot
plt.savefig(os.getcwd() +'\charactersing_datasets\H5_USDA_Seaborn_Matrix.png', dpi=300, bbox_inches='tight')
plt.close()
# Create a heatmap of the correlation matrix
df.drop(columns=['Crop', 'Treatment'], inplace=True)

sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('H5 USA Dataset Correlation Heatmap')
plt.savefig(os.getcwd() +'\charactersing_datasets\H5_USDA_Seaborn_Heatmap.png', dpi=300, bbox_inches='tight')