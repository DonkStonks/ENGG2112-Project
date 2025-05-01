import pandas as pd
#import pathlib as pL
import os

# Adding Longitude and Latitude data to India. 
#df_geo = pd.read_csv(pL(__file__).parent / 'Ind_adm2_Points.csv')
df_geo = pd.read_csv(os.getcwd() + '\data-combing\poptable.csv')
print(df_geo.columns)
df_geo["State"] = df_geo["State"].replace("    ","", regex=True)
df_geo["State"] = df_geo["State"].str.title()
df_Agri = pd.read_csv(os.getcwd() + '\datasets\India Agriculture Crop Production Cleaned.csv')



from difflib import get_close_matches

Agri_stat = df_Agri["State"].unique()
geo_stat = df_geo["State"].unique()

corres_geo = []
for disr in Agri_stat:
    closest_match = get_close_matches(disr, geo_stat, n=1, cutoff=0.3)  # Adjust cutoff as needed
    if closest_match:
        corres_geo.append((disr, closest_match[0]))
    else:
        corres_geo.append((disr, None))

lookup_s = pd.DataFrame(corres_geo, columns=["State_Agri", "State_Geo"])

# imbed Longitude and Latitude Data
df_inter = pd.merge(lookup_s, df_geo[["State", "latitude", "longitude"]], left_on="State_Geo", right_on="State", how="right")
df_merge = pd.merge(df_Agri, df_inter[["State_Agri", "latitude", "longitude"]], left_on="State",right_on="State_Agri", how="left")

df_merge.to_csv(os.getcwd() + '\datasets\India Agriculture Crop Production Cleaned with Geo.csv', index=False)
#df_merge.to_csv(pL(__file__).parent / 'India Agriculture Crop Production Cleaned with Geo.csv', index=False)