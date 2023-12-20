
from rasterstats import zonal_stats
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


input_folder = r'E:\test\input_json_test2'
output_folder = r'E:\test\output_test2'

# LULC tif, here I use the vertual tif combing all the tifs within the range of ROI.
tif_path = r'E:\OUTTIF\newxuni.vrt'


l = 0

# Read footprints geojson
json_files = glob(os.path.join(input_folder, '*.geojson'))

for json_file in json_files:

    l += 1
    t0 = time.time()
    base_name = os.path.splitext(os.path.basename(json_file))[0]
    geojson_output_path = os.path.join(output_folder, f'{base_name}_forest.geojson')

    print(f"{base_name} processing")

    #Change the crs to build buffer.
    gdf = gpd.read_file(json_file)
    gdf.crs = 'EPSG:4326'
    gdf_tr = gdf.to_crs(epsg=3857)

    for index, row in gdf_tr.iterrows():

        point_geometry = row.geometry

        # Build buffer
        buffered_point = point_geometry.buffer(25)

        # Extract the mean value of the buffer
        stats = zonal_stats(buffered_point, tif_path, all_touched=True)

        # 2 refers to the forests
        if stats[0]['mean'] != 2:
            gdf_tr = gdf_tr.drop(index)

    gdf_tr.to_file(geojson_output_path, driver='GeoJSON')
    t1 = time.time()
    t = t1-t0
    print(f"Time {t}")
    print(f"{l} finished")
    print("\n")

print("Conversion complete.")