import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

df = pd.read_csv(os.getcwd() + '\datasets\India Agriculture Crop Production Cleaned.csv')
#print(df.columns)


df = df[df['Production Units'] == 'Tonnes']
df = df[df['Area Units'] == 'Hectare']
print(len(df))
columns = ['District', 'Crop', 'Season', 'Area',
       'Production', 'Yield']
df = df[columns]

# Create a scatter plot matrix
sns.pairplot(df[['Area','Production', 'Yield', "Crop"]], diag_kind="kde",hue="Crop")
# sns.pairplot(df, diag_kind='kde', corner=True)

# Show the plot
plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-Crop.png', dpi=300, bbox_inches='tight')

sns.pairplot(df[['Area','Production', 'Yield', "Season"]], diag_kind="kde",hue="Season")
plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-Season.png', dpi=300, bbox_inches='tight')

sns.pairplot(df[['Area', 'Production', 'Yield', "District"]], diag_kind="kde",hue="District")
plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-District.png', dpi=300, bbox_inches='tight')

sns.pairplot(df, diag_kind="kde")
#plt.show()