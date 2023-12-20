#This code references the GEDI L4A tutorial, available at https://github.com/ornldaac/gedi_tutorials.

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

# Enter the input folder path and output folder path.
input_folder = 'D:/pyproject/l4a2022'
output_folder = 'D:/pyproject/output_data'

# Read the GeoJSON file of ROI.
dongbei = gpd.read_file('dongbeilunkuo.json')

# Retrieve all .h5 files in the input folder.
h5_files = glob(os.path.join(input_folder, '*.h5'))
proc = 0

# Iterate through each .h5 file and process them.
for h5_file in h5_files:
    # Generate the filenames for the output files
    # (retain the original filename, replacing the extension with .geojson and .csv).
    proc += 1
    base_name = os.path.splitext(os.path.basename(h5_file))[0]
    geojson_output_path = os.path.join(output_folder, f'{base_name}.geojson')
    csv_output_path = os.path.join(output_folder, f'{base_name}.csv')

    hf_in = h5py.File(h5_file, 'r')
    subset_df = pd.DataFrame()

    for v in list(hf_in.keys()):
        if v.startswith('BEAM'):
            col_names = []
            col_val = []
            beam = hf_in[v]
            # copy BEAMS
            for key, value in beam.items():
                # looping through subgroups
                if isinstance(value, h5py.Group):
                    for key2, value2 in value.items():
                        if (key2 != "shot_number"):
                            # xvar variables have 2D
                            if (key2.startswith('xvar')):
                                for r in range(4):
                                    col_names.append(key2 + '_' + str(r + 1))
                                    col_val.append(value2[:, r].tolist())
                            else:
                                col_names.append(key2)
                                col_val.append(value2[:].tolist())

                # looping through base group
                else:
                    # xvar variables have 2D
                    if (key.startswith('xvar')):
                        for r in range(4):
                            col_names.append(key + '_' + str(r + 1))
                            col_val.append(value[:, r].tolist())
                    else:
                        col_names.append(key)
                        col_val.append(value[:].tolist())

            # create a pandas dataframe
            beam_df = pd.DataFrame(map(list, zip(*col_val)), columns=col_names)
            # Inserting BEAM names
            beam_df.insert(0, 'BEAM', np.repeat(str(v), len(beam_df.index)).tolist())
            # Appending to the subset_df dataframe
            subset_df = pd.concat([subset_df, beam_df])
    hf_in.close()

    # Setting 'shot_number' as dataframe index. shot_number column is unique
    subset_df = subset_df.set_index('shot_number')

    # Drop the samples with low quality.
    subset_df = subset_df[subset_df['agbd'] != -9999]
    subset_df = subset_df[subset_df['algorithm_run_flag'] != 0]
    subset_df = subset_df[subset_df['l2_quality_flag'] != 0]
    subset_df = subset_df[subset_df['l4_quality_flag'] != 0]

    subset_gdf = gpd.GeoDataFrame(subset_df,
                                  geometry=gpd.points_from_xy(subset_df.lon_lowestmode, subset_df.lat_lowestmode))
    subset_gdf.crs = "EPSG:4326"

    # convert object types columns to strings. object types are not supported
    for c in subset_gdf.columns:
        if subset_gdf[c].dtype == 'object':
            subset_gdf[c] = subset_gdf[c].astype(str)

    #Clip the footprints into ROI.
    clipgdf = subset_gdf[subset_gdf['geometry'].within(dongbei.geometry[0])]

    clipgdf.to_file(geojson_output_path, driver='GeoJSON')
    clipgdf.to_csv(csv_output_path)
    print(proc)

print("Conversion complete.")