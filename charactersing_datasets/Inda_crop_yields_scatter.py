import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

df = pd.read_csv(os.getcwd() + '\datasets\India Agriculture Crop Production Cleaned with Geo.csv')
#print(df.columns)


df = df[df['Production Units'] == 'Tonnes']
df = df[df['Area Units'] == 'Hectare']
print(len(df))
columns = ['District', 'Crop', 'Season', 'Area',
       'Production', 'Yield', "latitude", "longitude"]
print(df.columns)
df = df[columns]

df = df.rename(columns={
    'Area': 'Area (Hectare)',
    'Production': 'Production (Tonnes)',
    'Yield': 'Yield (Tonnes/Hectare)',
    'latitude': 'Latitude',
    'longitude': 'Longitude'
})
df.drop(columns=['District', 'Season'], inplace=True)


# Create a scatter plot matrix
sns.pairplot(df, diag_kind="kde",hue="Crop")
#sns.pairplot(df, diag_kind='kde', corner=True)
#print("Printing Time")
# Show the plot
plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-Crop.png', dpi=300, bbox_inches='tight')

#sns.pairplot(df[['Area','Production', 'Yield', "Season"]], diag_kind="kde",hue="Season")
#plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-Season.png', dpi=300, bbox_inches='tight')

#sns.pairplot(df[['Area', 'Production', 'Yield', "District",'Crop']], diag_kind="kde",hue="District")
#plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-District.png', dpi=300, bbox_inches='tight')

#sns.pairplot(df, diag_kind="kde")
#plt.show()%
plt.close()
df.drop(columns=['Crop'], inplace=True)

sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Heatmap.png', dpi=300, bbox_inches='tight')