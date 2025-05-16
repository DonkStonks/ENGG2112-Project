import ee
print("Signing into Earth Engine API.")
ee.Authenticate()
# Log into Earth Engine
ee.Initialize()
print(ee.String('Hello from the Earth Engine servers!').getInfo())

import os
import pandas as pd
from pathlib import Path

produced_folder = Path(__file__).parent / "produced" / "Reduced"

# List all CSV files in the folder
csv_files = [produced_folder / f for f in os.listdir(produced_folder) if f.endswith('.csv')]

# Read and concatenate all CSVs
df_list = [pd.read_csv(f) for f in csv_files]
combined_df = pd.concat(df_list, ignore_index=True)

# Save the combined CSV
combined_df.to_csv(Path(__file__).parent / "allocated-weather" / "combined.csv", index=False)
home = Path(__file__).parent / "allocated-weather" / "combined.csv"
print(f"Combined {len(csv_files)} files into {home}")