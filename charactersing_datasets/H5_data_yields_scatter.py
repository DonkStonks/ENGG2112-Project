import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

#print(os.getcwd())

df = pd.read_csv(os.getcwd() + '\datasets\h5-i2_2016-2021_daily_harvest_cleaned.csv')

columns = ['Crop', 'Treatment',
       'Grain_yield_kg_ha', 'Stover_g_m2', 'Harvest_index',
       'Sol_Rad_MJ_m2_d', 'T_min_C', 'T_max_C', 'RH_f',
       'Wind_spd_m_s']
df = df[columns]

# Create a scatter plot matrix
sns.pairplot(df, diag_kind="kde",hue="Crop", markers=["o", "s", "D"],)
# sns.pairplot(df, diag_kind='kde', corner=True)

# Show the plot
plt.savefig(os.getcwd() +'\charactersing_datasets\H5_USDA_Seaborn_Matrix.png', dpi=300, bbox_inches='tight')