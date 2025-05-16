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

def has_data(img, point):
    try:
        val = img.sample(region=point, scale=30, projection='EPSG:4326').first().getInfo()
        return val is not None and 'properties' in val
    except Exception:
        return False
    
def fetch_elevation_data(vic_df,output_file,first):
    for idx, row in vic_df.iterrows():
        x = row['x']
        y = row['y']
        year = int(row['Year'])
        day_in_year = int(row['Day_in_Year'])
        date = datetime(year, 1, 1) + timedelta(days=day_in_year - 1)
        date_str = date.strftime('%Y-%m-%d')
        ee_date = ee.Date(date_str).advance(-10,"year")
        
        sand_content_percent = ee.Image('OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02') \
            .select('b30').rename('sand_content')
        organic_carbon_content_percent = ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02") \
            .select('b30').rename('organic_carbon')
        soil_type = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02") \
            .select('b30').rename('soil_type')
        # Define the elevation dataset
        soil_density_gcm3_5cm = ee.ImageCollection("CSIRO/SLGA") \
            .filterDate(ee_date.advance(-10,"year"), ee_date.advance(15, 'day').advance(-10,"year")) \
            .filter(ee.Filter.eq('attribute_code', 'BDW')) \
            .mean().select('BDW_000_005_EV')
        # Bulk Density of whole soil, estimated value at depth 0-5cm
        nitrogen_levels = ee.ImageCollection("CSIRO/SLGA") \
            .filterDate(ee_date.advance(-10,"year"), ee_date.advance(15, 'day').advance(-10,"year")) \
            .filter(ee.Filter.eq('attribute_code', 'NTO')) \
            .mean() \
            .select('NTO_005_015_EV')
        soil_pHL = ee.ImageCollection("CSIRO/SLGA") \
            .filterDate(ee_date.advance(-10,"year"), ee_date.advance(15, 'day').advance(-10,"year")) \
            .filter(ee.Filter.eq('attribute_code', 'pHc')) \
            .mean() \
            .select('pHc_005_015_EV')
        phosphorus_levels = ee.ImageCollection("CSIRO/SLGA") \
            .filterDate(ee_date.advance(-10,"year"), ee_date.advance(15, 'day').advance(-10,"year")) \
            .filter(ee.Filter.eq('attribute_code', 'PTO')) \
            .mean() \
            .select('PTO_005_015_EV')
        # Temperatuer of land surface in Kelvin
        soil_cation_exchange_meqper100g = ee.ImageCollection("CSIRO/SLGA") \
            .filterDate(ee_date.advance(-10,"year"), ee_date.advance(15, 'day').advance(-10,"year")) \
            .filter(ee.Filter.eq('attribute_code', 'ECE')) \
            .mean() \
            .select('ECE_000_005_EV')
        point = ee.Geometry.Point([x, y])
        for img, name in [
            (soil_density_gcm3_5cm, "Soil Density"),
            (nitrogen_levels, "Nitrogen"),
            (soil_pHL, "pH"),
            (phosphorus_levels, "Phosphorus"),
            (soil_cation_exchange_meqper100g, "Cation Exchange"),
            (sand_content_percent, "Sand Content"),
            (organic_carbon_content_percent, "Organic Carbon"),
            (soil_type, "Soil Type")
        ]:
            if not has_data(img, point):
                print(f"No data for {name} at ({x}, {y}) on {date_str}")
                print("Colected the data for: ",idx)
    #        # Combine datasets 
        combined_dataset = soil_density_gcm3_5cm \
            .addBands(nitrogen_levels) \
            .addBands(soil_pHL) \
            .addBands(phosphorus_levels) \
            .addBands(soil_cation_exchange_meqper100g) \
            .addBands(sand_content_percent) \
            .addBands(organic_carbon_content_percent) \
            .addBands(soil_type)
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
            result['Soil_Density'] = props.get('BDW_000_005_EV', None)
            result['Nitrogen_Mass'] = props.get('NTO_005_015_EV', None)
            result["pH_Levels"] = props.get('pHc_005_015_EV', None)
            result["Phosphorous_Mass"] = props.get('PTO_005_015_EV', None)
            result["soil_Cation_Exchange_Capacity"] = props.get('ECE_000_005_EV', None)
            result["Sand_Content"] = props.get('sand_content', None)
            result["Organic_Carbon_Content"] = props.get('organic_carbon', None)
            result["Soil_Type"] = props.get('soil_type', None)
        except Exception as e:
            print(f"Failed at ({x}, {y}) on {date_str}: {e}")
            result = row.to_dict()
            result['Soil_Density'] = None
            result['Nitrogen_Mass'] = None
            result['pH_Levels'] = None
            result["Phosphorous_Mass"] = None
            result["soil_Cation_Exchange_Capacity"] = None
            result["Sand_Content"] = None
            result["Organic_Carbon_Content"] = None
            result["Soil_Type"] = None
        #print("Created the feature collection")
        # Convert to DataFrame and append to CSV
        pd.DataFrame([result]).to_csv(
            output_file, mode='a', header=first, index=False
        )
        first = False
    print("")

# Path to the produced folder
produced_folder = Path(__file__).parent / "produced" / "Reduced"
output_folder = Path(__file__).parent / "allocated-weather"
output_folder.mkdir(exist_ok=True)  # Ensure the folder exists
first = True
# Iterate through all VIC data files in the produced folder
for file in os.listdir(produced_folder):
     
    print(f"The file {file} is being processed.")
    file_path = produced_folder / file
    print(f"Processing file: {file}")

    # Load the VIC data
    vic_df = pd.read_csv(file_path)

    output_folder = produced_folder / "Reduced"
    output_folder.mkdir(exist_ok=True)  # Create the folder if it doesn't exist
    output_file = output_folder / "GSI_VIC_dataset.csv"
    #out_df.to_csv(output_file, index=False)

    # Fetch elevation data from Earth Engine
    elevation_df = fetch_elevation_data(vic_df,output_file,first)

    
    print(f"Reduced resolution file saved: {output_folder / file}")
