import ee
ee.Authenticate()
# Log into Earth Engine
ee.Initialize()
print(ee.String('Hello from the Earth Engine servers!').getInfo())

import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# Path to the produced folder
produced_folder = Path(__file__).parent / "produced" / "Reduced"
output_folder = Path(__file__).parent / "allocated-weather"
output_folder.mkdir(exist_ok=True)  # Ensure the folder exists
first = True