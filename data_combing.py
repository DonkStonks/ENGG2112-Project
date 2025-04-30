import zipfile
import pandas as pd
import numpy as np

df = pd.read_csv("Louisiana_All_Genotypes_2010_onwards.csv")
# file = pd.read_csv("Louisiana_All_Genotypes_2010_onwards.csv", encoding='latin1')


df = df.drop(columns=['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 12'])
print(df.head())
# df.info()
print(len(df))