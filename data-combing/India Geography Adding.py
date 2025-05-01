import pandas as pd
#import pathlib as pL
import os

# Adding Longitude and Latitude data to India. 
#df_geo = pd.read_csv(pL(__file__).parent / 'Ind_adm2_Points.csv')
df_geo = pd.read_csv(os.getcwd() + '\data-combing\Ind_adm2_Points.csv')

# Keep only the necessary columns
df_geo = df_geo[["State","District","Ind_adm2_ID","Latitude","Longitude"]]

# Group by 'District' and 'Ind_adm2_ID' and calculate the mean for 'Latitude' and 'Longitude'
df_india = df_geo[["State","Latitude","Longitude"]].groupby("State", as_index=False).mean()
#df_india = df_geo.groupby(["Ind_adm2_ID","District","State"], as_index=False).mean()

#print(df_india.head())

df_Agri = pd.read_csv(os.getcwd() + '\datasets\India Agriculture Crop Production Cleaned.csv')
#df_Agri["District"] = df_Agri["District"].str.title()
#df_india["District"] = df_india["District"].replace("Islands","", regex=True)
#df_Agri["District"] = df_Agri["District"].replace("North And Middle","", regex=True)
#df_Agri["District"] = df_Agri["District"].replace("South","", regex=True)


#Agri_dis = df_Agri["District"].unique()
#geo_dis = df_india["District"].unique()
#print("Number of unique districts: ",len(Agri_dis))

#Agri_dis = Agri_dis.replace("Islands","")

# Find the common districts between df_Agri and df_india
from difflib import get_close_matches

#corres_geo = []
#for disr in Agri_dis:
#    closest_match = get_close_matches(disr, geo_dis, n=1, cutoff=0.3)  # Adjust cutoff as needed
#    if closest_match:
#        corres_geo.append((disr, closest_match[0]))
#    else:
#        corres_geo.append((disr, None))

#lookup_d = pd.DataFrame(corres_geo, columns=["District_Agri", "District_Geo"])

df_Agri["State"] = df_Agri["State"].str.title()

Agri_stat = df_Agri["State"].unique()
geo_stat = df_india["State"].unique()

corres_geo = []
for disr in Agri_stat:
    closest_match = get_close_matches(disr, geo_stat, n=1, cutoff=0.3)  # Adjust cutoff as needed
    if closest_match:
        corres_geo.append((disr, closest_match[0]))
    else:
        corres_geo.append((disr, None))

lookup_s = pd.DataFrame(corres_geo, columns=["State_Agri", "State_Geo"])

# imbed Longitude and Latitude Data

# Merge df_Agri with df_geo based on the "State" column
df_inter = pd.merge(lookup_s, df_india[["State", "Latitude", "Longitude"]], left_on="State_Geo", right_on="State", how="right")
#print(df_inter)

df_merge = pd.merge(df_Agri, df_inter[["State_Agri", "Latitude", "Longitude"]], left_on="State",right_on="State_Agri", how="left")
print(df_merge)

df_merge.to_csv(os.getcwd() + '\datasets\India Agriculture Crop Production Cleaned with Geo.csv', index=False)
#df_merge.to_csv(pL(__file__).parent / 'India Agriculture Crop Production Cleaned with Geo.csv', index=False)