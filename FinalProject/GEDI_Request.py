# This code references the GEDI L4A tutorial, available at https://github.com/ornldaac/gedi_tutorials.

import h5py
import requests as re
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from datetime import datetime
from glob import glob
from harmony import BBox, Client, Collection, Environment, Request

harmony_client = Client(auth=("aaaaaaaa", "111111111"))   #Replace them by your username and password of NASA Earthdata.
# GEDI L4A DOI
doi = '10.3334/ORNLDAAC/2056'

# CMR API base url
doisearch=f'https://cmr.earthdata.nasa.gov/search/collections.json?doi={doi}'
concept_id = re.get(doisearch).json()['feed']['entry'][0]['id']

collection = Collection(id=concept_id)

#Select the variables
variables = ['/BEAM0000/agbd',
             '/BEAM0000/algorithm_run_flag',
             '/BEAM0000/delta_time',
             '/BEAM0000/l2_quality_flag',
             '/BEAM0000/l4_quality_flag',
             '/BEAM0000/lat_lowestmode',
             '/BEAM0000/lon_lowestmode',
             '/BEAM0000/sensitivity',
             '/BEAM0000/shot_number',
             '/BEAM0000/land_cover_data/leaf_off_flag',
             '/BEAM0000/land_cover_data/pft_class',
             '/BEAM0001/agbd',
             '/BEAM0001/algorithm_run_flag',
             '/BEAM0001/delta_time',
             '/BEAM0001/l2_quality_flag',
             '/BEAM0001/l4_quality_flag',
             '/BEAM0001/lat_lowestmode',
             '/BEAM0001/lon_lowestmode',
             '/BEAM0001/sensitivity',
             '/BEAM0001/shot_number',
             '/BEAM0001/land_cover_data/leaf_off_flag',
             '/BEAM0001/land_cover_data/pft_class',
             '/BEAM0010/agbd',
             '/BEAM0010/algorithm_run_flag',
             '/BEAM0010/delta_time',
             '/BEAM0010/l2_quality_flag',
             '/BEAM0010/l4_quality_flag',
             '/BEAM0010/lat_lowestmode',
             '/BEAM0010/lon_lowestmode',
             '/BEAM0010/sensitivity',
             '/BEAM0010/shot_number',
             '/BEAM0010/land_cover_data/leaf_off_flag',
             '/BEAM0010/land_cover_data/pft_class',
             '/BEAM0011/agbd',
             '/BEAM0011/algorithm_run_flag',
             '/BEAM0011/delta_time',
             '/BEAM0011/l2_quality_flag',
             '/BEAM0011/l4_quality_flag',
             '/BEAM0011/lat_lowestmode',
             '/BEAM0011/lon_lowestmode',
             '/BEAM0011/sensitivity',
             '/BEAM0011/shot_number',
             '/BEAM0011/land_cover_data/leaf_off_flag',
             '/BEAM0011/land_cover_data/pft_class',
             '/BEAM0101/agbd',
             '/BEAM0101/algorithm_run_flag',
             '/BEAM0101/delta_time',
             '/BEAM0101/l2_quality_flag',
             '/BEAM0101/l4_quality_flag',
             '/BEAM0101/lat_lowestmode',
             '/BEAM0101/lon_lowestmode',
             '/BEAM0101/sensitivity',
             '/BEAM0101/shot_number',
             '/BEAM0101/land_cover_data/leaf_off_flag',
             '/BEAM0101/land_cover_data/pft_class',
             '/BEAM0110/agbd',
             '/BEAM0110/algorithm_run_flag',
             '/BEAM0110/delta_time',
             '/BEAM0110/l2_quality_flag',
             '/BEAM0110/l4_quality_flag',
             '/BEAM0110/lat_lowestmode',
             '/BEAM0110/lon_lowestmode',
             '/BEAM0110/sensitivity',
             '/BEAM0110/shot_number',
             '/BEAM0110/land_cover_data/leaf_off_flag',
             '/BEAM0110/land_cover_data/pft_class',
             '/BEAM1000/agbd',
             '/BEAM1000/algorithm_run_flag',
             '/BEAM1000/delta_time',
             '/BEAM1000/l2_quality_flag',
             '/BEAM1000/l4_quality_flag',
             '/BEAM1000/lat_lowestmode',
             '/BEAM1000/lon_lowestmode',
             '/BEAM1000/sensitivity',
             '/BEAM1000/shot_number',
             '/BEAM1000/land_cover_data/leaf_off_flag',
             '/BEAM1000/land_cover_data/pft_class',
             '/BEAM1011/agbd',
             '/BEAM1011/algorithm_run_flag',
             '/BEAM1011/delta_time',
             '/BEAM1011/l2_quality_flag',
             '/BEAM1011/l4_quality_flag',
             '/BEAM1011/lat_lowestmode',
             '/BEAM1011/lon_lowestmode',
             '/BEAM1011/sensitivity',
             '/BEAM1011/shot_number',
             '/BEAM1011/land_cover_data/leaf_off_flag',
             '/BEAM1011/land_cover_data/pft_class']

#Select the temporal range.
temporal_range = {'start': datetime(2022, 4, 1), 'stop': datetime(2022, 9, 30)}

#Select your ROI.
dongbei = gpd.read_file('dongbeilunkuo.json')
b = dongbei.total_bounds
# bounding box for Harmony
bounding_box = BBox(w=b[0], s=b[1], e=b[2], n=b[3])

#Make a request.
request = Request(collection=collection,
                  variables=variables,
                  temporal=temporal_range,
                  spatial=bounding_box,
                  ignore_errors=True)

# submit harmony request, will return job id
subset_job_id = harmony_client.submit(request)

print(f'Processing job: {subset_job_id}')

print(f'Waiting for the job to finish')
results = harmony_client.result_json(subset_job_id, show_progress=True)

print(f'Downloading subset files...')
futures = harmony_client.download_all(subset_job_id, overwrite=False)
for f in futures:
    # all subsetted files have this suffix
    if f.result().endswith('subsetted.h5'):
        print(f'Downloaded: {f.result()}')

print(f'Done downloading files.')

#If a pause is encountered, you can manually restart the job request process through the Harmony API's GUI.
#https://harmony.earthdata.nasa.gov/workflow-ui
# Once the request process is completed, download all data through 'GEDI_Download' script.