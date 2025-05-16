import ee
ee.Authenticate()
# Log into Earth Engine
ee.Initialize()
print(ee.String('Hello from the Earth Engine servers!').getInfo())

evapotranspiration_dataset = ee.ImageCollection('TERN/AET/CMRSET_LANDSAT_V2_2').filterDate('2023-01-01', '2023-01-02').mean().select('ETa')

print(evapotranspiration_dataset.bandNames().getInfo())

