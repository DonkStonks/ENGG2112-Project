import ee
ee.Authenticate()
# Log into Earth Engine
ee.Initialize()
print(ee.String('Hello from the Earth Engine servers!').getInfo())

import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def fetch_elevation_data(vic_df):
    # Define the elevation dataset
    elevation_dataset = ee.Image('AU/GA/DEM_1SEC/v10/DEM-H').select('elevation')
    
    # Extract the year and day from the VIC data (assuming all rows have the same date)
    year = int(vic_df.iloc[0]['Year'])
    day_in_year = int(vic_df.iloc[0]['Day_in_Year'])
    # Calculate the exact date
    date = datetime(year, 1, 1) + timedelta(days=day_in_year - 1)
    date_str = date.strftime('%Y-%m-%d')
    ee_date = ee.Date(date_str)
    # Filter the evapotranspiration dataset for the specific date
    evapotranspiration_dataset = ee.ImageCollection('TERN/AET/CMRSET_LANDSAT_V2_2') \
        .filterDate(ee_date, ee_date.advance(1, 'day')) \
        .mean() \
        .select('aet')
    evapotranspiration_dataset = ee.ImageCollection('TERN/AET/CMRSET_LANDSAT_V2_2').mean().select('aet')
    print("Colected the data")

    combined_dataset = elevation_dataset.addBands(evapotranspiration_dataset)
    # Convert VIC coordinates to Earth Engine geometry points
    points = [
        ee.Geometry.Point([row['x'], row['y']])
        for _, row in vic_df.iterrows()
    ]

    # Create a FeatureCollection from the points
    feature_collection = ee.FeatureCollection([
        ee.Feature(point) for point in points
    ])
    print("Created the feature collection")
    # Sample elevation data at the points
    sampled = combined_dataset.sampleRegions(
        collection=feature_collection,
        scale=30,  # Resolution in meters
        projection='EPSG:4326'
    )
    print("Sampled the data")
    # Convert sampled data to a list of dictionaries
    sampled_data = sampled.getInfo()['features']
    elevation_data = [
        {
            'x': feature['geometry']['coordinates'][0],
            'y': feature['geometry']['coordinates'][1],
            'elevation': feature['properties']['elevation']
        }
        for feature in sampled_data
    ]
    print("collection done")
    # Convert to a DataFrame
    return pd.DataFrame(elevation_data)

# Path to the produced folder
produced_folder = Path(__file__).parent / "produced"

# Iterate through all VIC data files in the produced folder
for file in os.listdir(produced_folder):
    print(f"The file {file} is being processed.")
    if file.endswith(".csv") and "VIC" in file:
        file_path = produced_folder / file
        print(f"Processing file: {file}")

        # Load the VIC data
        vic_df = pd.read_csv(file_path)
        # Ensure evenly spaced values by keeping every 8th row
        print("rawsize: ", len(vic_df))
        evenly_spaced_df = vic_df[vic_df.index % 32 == 0]
        print("cutdown: ", len(evenly_spaced_df))

        # Fetch elevation data from Earth Engine
        elevation_df = fetch_elevation_data(evenly_spaced_df)
        
        # Merge VIC data with elevation data based on coordinates
        merged_df = pd.merge(
            evenly_spaced_df,
            elevation_df,
            how="left",
            on=["x", "y"]
        )

        # Save the updated VIC data back to the produced folder
        output_folder = produced_folder / "Reduced"
        output_folder.mkdir(exist_ok=True)  # Create the folder if it doesn't exist
        out_df.to_csv(output_folder / file, index=False)
        print(f"Reduced resolution file saved: {output_folder / file}")
    else:
        print(f"{file} is rejected.")