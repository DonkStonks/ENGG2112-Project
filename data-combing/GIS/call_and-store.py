#import os
from pathlib import Path
from io import BytesIO
from requests_oauth2client import *
import requests
CLIENT_ID = "87cbe909-b3d6-4b98-8bd6-e96ac52eff0c"
CLIENT_SECRET = "9nq8Q~fBIYeZXaeyC2_UoG4AH3W~x5hI~UDDUbJy"
oauth2client = OAuth2Client('https://login.microsoftonline.com/a815c246-a01f-4d10-bc3e-eeb6a48ef48a/oauth2/v2.0/token', (CLIENT_ID, CLIENT_SECRET))
session = requests.Session()
session.auth = OAuth2ClientCredentialsAuth(oauth2client, scope=f'{CLIENT_ID}/.default')

import rasterio
from rasterio.transform import xy
import pandas as pd

def tabulate_geotiff(filename):
    # Open the GeoTIFF file
    with rasterio.open(filename) as src:
        # Read the first band (assuming single-band GeoTIFF)
        band = src.read(1)  # 1-based index for the first band

        # Get the transform for converting pixel indices to coordinates
        transform = src.transform

        # Prepare lists to store coordinates and values
        data = []

        # Loop through each pixel
        for row in range(band.shape[0]):
            for col in range(band.shape[1]):
                value = band[row, col]
                # Skip NoData values
                if value == src.nodata:
                    continue
                # Get the coordinates of the pixel
                x, y = xy(transform, row, col)
                data.append({"x": x, "y": y, "value": value})

    # Convert to a DataFrame for easier handling
    df = pd.DataFrame(data)
    return df

def download_file(filename, session):
    """
    Downloads a file from the given URL and returns it as an in-memory buffer.
    """
    base_url = 'https://senaps.eratos.com/thredds/fileServer'
    http_path = f'csiro-agdatashop/npp/npp-sample/{filename}'
    with session.get(f'{base_url}/{http_path}', stream=True) as r:
        r.raise_for_status()
        buffer = BytesIO()
        for chunk in r.iter_content(chunk_size=4096):
            buffer.write(chunk)
        buffer.seek(0)  # Reset the buffer pointer to the beginning
    return buffer

print("Call: ", Path(__file__).with_name("api-catalogue.tsv"))
catalogue = pd.read_csv(Path(__file__).with_name("api-catalogue.tsv"),sep="\t", header=0)
print("Catalogue: ")
print(catalogue.head())
filenames = catalogue["Filename"]
#print(filenames)
print()
print("Number of files: ", len(filenames))
print()
filenames = ['CSPv21_NPP_2018.193.VIC.tif', 'CSPv21_NPP_2018.193.VIC.tif']

for name_of_item_tup in filenames:
    if len(name_of_item_tup) < 24:
        continue
    name_of_item_tup = name_of_item_tup.replace(" ", "")
    print("Processing:", name_of_item_tup)
    buffer = download_file(name_of_item_tup, session)
    df = tabulate_geotiff(buffer)
    df["Year"] = int(name_of_item_tup[11:14])
    df["Day_in_Year"] = int(name_of_item_tup[16:17])
    # Save to CSV or print
    df.to_csv(Path(__file__).with_name("\producedf\"+name_of_item_tup[0:-4]+".csv"), index=False)
    print(df.head())
