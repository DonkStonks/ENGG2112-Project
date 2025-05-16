import ee
print("Signing into Earth Engine API.")
ee.Authenticate()
# Log into Earth Engine
ee.Initialize()
print(ee.String('Hello from the Earth Engine servers!').getInfo())

import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def fetch_elevation_data(vic_df,output_file):
    first = True
    for idx, row in vic_df.iterrows():
        x = row['x']
        y = row['y']
        year = int(row['Year'])
        day_in_year = int(row['Day_in_Year'])
        date = datetime(year, 1, 1) + timedelta(days=day_in_year - 1)
        date_str = date.strftime('%Y-%m-%d')
        ee_date = ee.Date(date_str)

        # Define the elevation dataset
        elevation_dataset = ee.Image('AU/GA/DEM_1SEC/v10/DEM-H').select('elevation')

        evapotranspiration_dataset = ee.ImageCollection('TERN/AET/CMRSET_LANDSAT_V2_2') \
            .filterDate(ee_date, ee_date.advance(35, 'day')) \
            .mean().select('ETa')
        
        surface_and_root_zone_moisture_dataset = ee.ImageCollection("NASA/SMAP/SPL4SMGP/007") \
            .filterDate(ee_date, ee_date.advance(15, 'day')) \
            .mean() \
            .select('sm_surface')
        surface_temperature_K = ee.ImageCollection("JAXA/GCOM-C/L3/LAND/LST/V1") \
            .filterDate(ee_date, ee_date.advance(15, 'day')) \
            .mean() \
            .select('LST_AVE')
        # Temperatuer of land surface in Kelvin
        daily_precipt = ee.ImageCollection('ECMWF/ERA5/DAILY') \
            .filterDate(ee_date, ee_date.advance(15, 'day')) \
            .mean() \
            .select('total_precipitation')
        pressure_day = ee.ImageCollection('ECMWF/ERA5/DAILY') \
            .filterDate(ee_date, ee_date.advance(15, 'day')) \
            .mean() \
            .select('surface_pressure')
        print("Colected the data for: ",idx)
#        # Combine datasets 
        combined_dataset = elevation_dataset \
            .addBands(surface_and_root_zone_moisture_dataset) \
            .addBands(surface_temperature_K) \
            .addBands(daily_precipt) \
            .addBands(pressure_day) \
            .addBands(evapotranspiration_dataset)
    # Convert VIC coordinates to Earth Engine geometry points
        points = ee.Geometry.Point([x, y])
        feature_collection = combined_dataset.sample(region=points, scale=30, projection='EPSG:4326').first()
        #feat1 = evapotranspiration_dataset.sample(region=points, scale=30, projection='EPSG:4326').first()
        # Get info from Earth Engine
        try:
            info = feature_collection.getInfo()
            #print("info:", info)
            props = info['properties']
            print("props:", props)
            #info = feat1.getInfo()
            #props1 = info['properties']
            result = row.to_dict()
            # Add new columns
            result['elevation'] = props.get('elevation', None)
            result['evapotranspiration'] = props.get('ETa', None)
            result["SPL4_Soilmoisture"] = props.get('sm_surface', None)
            result["Land_Surface_Temp_K"] = props.get('LST_AVE', None)
            result["Precipictation_m"] = props.get('total_precipitation', None)
            result["Surface_Pres_Pa"] = props.get('surface_pressure', None)
        except Exception as e:
            print(f"Failed at ({x}, {y}) on {date_str}: {e}")
            result = row.to_dict()
            result['elevation'] = None
            result['evapotranspiration'] = None
            result['SPL4_Soilmoisture'] = None
            result["Land_Surface_Temp_K"] = None
            result["Precipictation_m"] = None
            result["Surface_Pres_Pa"] = None
        #print("Created the feature collection")
        # Convert to DataFrame and append to CSV
        pd.DataFrame([result]).to_csv(
            output_file, mode='a', header=first, index=False
        )
        first = False
    print("")

# Path to the produced folder
produced_folder = Path(__file__).parent / "produced"
output_folder = produced_folder / "Reduced"
output_folder.mkdir(exist_ok=True)  # Ensure the folder exists

# Iterate through all VIC data files in the produced folder
for file in os.listdir(produced_folder):
    
    if file.endswith(".csv") and "VIC" in file:
        output_file = output_folder / file
        if output_file.exists():
            print(f"Skipping {file} because it already exists.")
            continue    
        print(f"The file {file} is being processed.")
        file_path = produced_folder / file
        print(f"Processing file: {file}")

        # Load the VIC data
        vic_df = pd.read_csv(file_path)
        # Ensure evenly spaced values by keeping every 32760th row
        print("rawsize: ", len(vic_df))
        evenly_spaced_df = vic_df[vic_df.index % 32768 == 0]
        print("cutdown: ", len(evenly_spaced_df))

        output_folder = produced_folder / "Reduced"
        output_folder.mkdir(exist_ok=True)  # Create the folder if it doesn't exist
        output_file = output_folder / file
        #out_df.to_csv(output_file, index=False)

        # Fetch elevation data from Earth Engine
        elevation_df = fetch_elevation_data(evenly_spaced_df,output_file)

        
        print(f"Reduced resolution file saved: {output_folder / file}")
    else:
        print(f"{file} is rejected.")