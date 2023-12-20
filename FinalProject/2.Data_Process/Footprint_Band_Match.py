from rasterstats import zonal_stats
from rasterstats import point_query
import geopandas as gpd
import requests
import h5py
import pandas as pd
import geopandas as gpd
import contextily as ctx
import h5py
import matplotlib as plt
import numpy as np
from glob import glob
from os import path
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import orient
import os
import time
import rasterio

# Input geojson and output geojson
input_folder = r"E:\geeproject\input1"
output_folder = r"E:\geeproject\output1"

# Sentinel-2 tif. Here I extract the band values band by band.
# So I run the script for 12 times to get all the band values corresponding to each GEDI footprint.
tif_path = r"E:\geeproject\dongbei12.vrt"

l = 0

# read footprint geojson
json_files = glob(os.path.join(input_folder, '*.geojson'))

for json_file in json_files:

    l += 1
    t0 = time.time()
    base_name = os.path.splitext(os.path.basename(json_file))[0]
    geojson_output_path = os.path.join(output_folder, f'{base_name}12.geojson')
    print(f"{base_name} processing")

    #Make buffer
    gdf = gpd.read_file(json_file)
    buffered_point = gdf.geometry.buffer(25)

    #Extract the mean value of the buffer.
    stats = zonal_stats(buffered_point, tif_path, nodata=0, stats="mean")
    mean_values = [d['mean'] for d in stats]
    gdf[f'band_12_values'] = mean_values

    #Output geojson with new band values.
    gdf.to_file(geojson_output_path, driver='GeoJSON')
    t1 = time.time()
    t = t1-t0
    print(f"Time {t}")
    print(f"{l} finished")
    print("\n")

print("Conversion complete.")