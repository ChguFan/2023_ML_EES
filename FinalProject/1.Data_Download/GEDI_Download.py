#This code references the GEDI L4A tutorial, available at https://github.com/ornldaac/gedi_tutorials.

from harmony import Client
harmony_client = Client(auth=("aaaaaaaa", "111111111"))   #Replace them by your username and password of NASA Earthdata.
futures = harmony_client.download_all('36bb80a0-a8ba-489d-8a18-61ffa45abfdb', overwrite=False)  #Replace it with your jobid.

#Download all data in this job.
for f in futures:
    # all subsetted files have this suffix
    if f.result().endswith('subsetted.h5'):
        print(f'Downloaded: {f.result()}')

print(f'Done downloading files.')