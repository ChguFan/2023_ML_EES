You can find the codes, data, slides and reports here for the final project for the *Machine Learning for Earth and Environmental Sciences* course at the University of Lausanne, Autumn Semester 2023.

Here is a table introducing each file of the final project.

| Folder    | File | Description    |
| :------- | :------ | :------- |
| 1     | GEDI_Request.py   | Make a job request through Harmony API.     |
| 1 | GEDI_Download.py | Download GEDI h5 files. |
| 1 | Sentinel2_12bands.txt | Javascript of GEE code editor for downloading Sentinel-2 12 bands. |
|1 | Sentinel2_14bands.txt | Javascript of GEE code editor for downloading Sentinel-2 12 bands plus lat, lon in forested pixels .|
|2| GEDI_Quality_Filtration.py | Filter the footprints of low quality.|
|2| GEDI_Forest_Filtration.py | Filter the footprints in non-forested areas.|
|2| Footprint_Band_Match.py | Match the footprints with Sentinel-2 band values.|
|2| CSV_Merge.py | Merge all the samples and filter the outlines.|
|2| dataset_download_link.md | Download the dataset after filtration.|
|3| rdmfr.py| Train the Random Forest model.|
|3| lgbmsearch.py| Search parameters of Light GBM model.|
|3| lightgbm.py| Train the Light GBM model using best parameters.|
|3| MLP.ipynb| Train the MLP model.|
|3| 1DCNN.ipynb| Train the 1DCNN model.|
|4| Confusion_plot.ipynb| Draw the confusion plot using MLP as an example.|
|4| Feature_importance.ipynb| Calculate and plot the feature importance of Random Foest model.|
|4| map_predict.py| Generate AGB map by Random Forest model.|
