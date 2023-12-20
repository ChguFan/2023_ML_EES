import os
import rasterio
import numpy as np
import pandas as pd
from joblib import load
import time
import glob

# We put the input tifs (12 band values + lat band + lon band, forest masked) in the input_folder, the output agbd tif is in the output_folder.
input_folder_path = 'E:\predicttest\input1'
output_folder_path = 'E:\predicttest\output1'

# read tif
tiff_files = glob.glob(os.path.join(input_folder_path, '*.tif'))

# load Random Forest model
model = load('rfmodel.joblib')
sum = 0

for tiff_path in tiff_files:

    sum += 1
    print(f'{sum} processing')
    t0 = time.time()

    with rasterio.open(tiff_path) as dataset:
        bands = dataset.read(masked=True)


        data = {}
        for i in range(bands.shape[0]):
            data[f"Band_{i + 1}"] = bands[i].flatten()

        # Extract 14 bands in tif to build a df

        df_input = pd.DataFrame(data)


        mask = ~df_input.isna().any(axis=1)
        df_input.columns = ['lat_lowestmode', 'lon_lowestmode', 'band_1_values', 'band_2_values', 'band_3_values',
                            'band_4_values', 'band_5_values', 'band_6_values', 'band_7_values', 'band_8_values',
                            'band_8a_values', 'band_9_values', 'band_11_values', 'band_12_values']

        df_input.dropna(inplace=True)
        if df_input.empty:
            print(f" No valid pixel in {tiff_path}.")
            continue


        #make predictions using Random Forest model
        df_predictions = model.predict(df_input)
        df_predictions[df_predictions < 0] = np.nan


        output_array = np.full((dataset.height, dataset.width), np.nan, dtype=df_predictions.dtype)


        mask_array = mask.to_numpy()


        height, width = output_array.shape


        mask_2d = mask_array.reshape(height, width)


        new_band_array = df_predictions.flatten()


        output_array[mask_2d] = new_band_array


        output_filename = os.path.basename(tiff_path).replace('.tif', '_output.tif')
        output_file_path = os.path.join(output_folder_path, output_filename)

        # write new agbd tif
        meta = dataset.meta.copy()
        meta.update(dtype=new_band_array.dtype, count=1)

        # output tif
        with rasterio.open(output_file_path, 'w', **meta) as out_dataset:
            out_dataset.write(output_array, 1)

    t1 = time.time()
    print(t1 - t0)
