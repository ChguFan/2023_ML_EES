import os
import geopandas as gpd
import pandas as pd


# Geojson to be merged
folder_path = "E:\geeproject\output_end"

# Read geojsons
geojson_files = [file for file in os.listdir(folder_path) if file.endswith(".geojson")]
l = 0
# Merge geojsons
merged_gdf = gpd.GeoDataFrame()
for file in geojson_files:
    file_path = os.path.join(folder_path, file)
    gdf = gpd.read_file(file_path)
    merged_gdf = gpd.GeoDataFrame(pd.concat([merged_gdf, gdf], ignore_index=True))
    l += 1
    print(l)

# Save as new geojson and csv files.
merged_gdf.to_file("merged_points.geojson", driver="GeoJSON")
merged_gdf.to_csv("merged_points.csv", index=False)

df = pd.read_csv('merged_points.csv')

selected_columns = df[[ 'agbd', 'lat_lowestmode','lon_lowestmode', 'band_1_values', 'band_2_values',
       'band_3_values', 'band_4_values', 'band_5_values', 'band_6_values',
       'band_7_values', 'band_8_values', 'band_8a_values', 'band_9_values',
       'band_11_values', 'band_12_values']]

# New csv file containing only variables needed.
selected_columns.to_csv('dataset.csv', index=False)

#Filter the dataset by percentile.
p1 = selected_columns['agbd'].quantile(0.01)
p99 = selected_columns['agbd'].quantile(0.99)

filtered_df = df[(df['agbd'] >= p1) & (df['agbd'] <= p99)]

#Final csv file ready to be loaded to machine learning process.
filtered_df.to_csv('data0199.csv', index=False)
