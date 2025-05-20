import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
fileplace = os.getcwd() + r'\data-combing\GIS\allocated-weather\combined.csv'
print(fileplace)

df = pd.read_csv(fileplace)
print(df.columns)


print(len(df))
columns = ['value', 'elevation', 'evapotranspiration', 'SPL4_Soilmoisture',
       'Land_Surface_Temp_K', 'Precipictation_m', "Surface_Pres_Pa"]
print(df.columns)
df = df[columns]

#df = df.rename(columns={
#    'Area': 'Area (Hectare)',
#    'Production': 'Production (Tonnes)',
#    'Yield': 'Yield (Tonnes/Hectare)',
#    'latitude': 'Latitude',
#    'longitude': 'Longitude'
#})
#df.drop(columns=['District', 'Season'], inplace=True)


# Create a scatter plot matrix
sns.pairplot(df, diag_kind="kde")
#sns.pairplot(df, diag_kind='kde', corner=True)
#print("Printing Time")
# Show the plot
plt.savefig(os.getcwd() +'\charactersing_datasets\GIS_prelimdata_histogramsnscatter.png', dpi=300, bbox_inches='tight')

#sns.pairplot(df[['Area','Production', 'Yield', "Season"]], diag_kind="kde",hue="Season")
#plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-Season.png', dpi=300, bbox_inches='tight')

#sns.pairplot(df[['Area', 'Production', 'Yield', "District",'Crop']], diag_kind="kde",hue="District")
#plt.savefig(os.getcwd() +'\charactersing_datasets\India_Agriculture_Crop_Seaborn_Matrix-District.png', dpi=300, bbox_inches='tight')

#sns.pairplot(df, diag_kind="kde")
#plt.show()%
plt.close()

sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig(os.getcwd() +'\charactersing_datasets\GIS_prelimdata_Seaborn_Heatmap.png', dpi=300, bbox_inches='tight')