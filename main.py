from sentinel_1_info_extraction import extract_info_from_sar
from sentinel_2_info_extraction import extract_info_from_optic
from extract_satellites_archive import extract_archives
import os


class SatelliteError(Exception):
    pass


def main():
    '''
    Following script is used to extract files and information about satellite images,
    sort them and insert them to PostgreSql(PostGIS) database.

    replace variables with your paths bellow, to extract information from files downloaded via SentinelHub:

        - path_to_zip_archives: in this directory should be .zip files that you downloaded from SentinelHub (should have .zip files in it).
        - images: specify directory in which the extracted images will be stored (can be empty).
        - output: specify directory where the csv files will be generated (shold be empty).

    for now, it works only on Sentinel-1 and Sentinel-2 download.
    '''

    path_to_zip_archives = 'D:\Praca_magisterska\scripts\satellite_imagery_archives'
    images = 'D:\Praca_magisterska\scripts\images'
    output = 'D:\Praca_magisterska\scripts\output'


    print('Starting the Proces of Satellite Image Archive Information Extraction...\n\n')

    extract_archives(path_to_zip_archives, images)
    print('Acquisition of Information Started...')
    extract_info_from_sar(images,output)
    extract_info_from_optic(images,output)
    print('Process finished')

'''
OPTIC:
extract all files from all zips in specified directory  - ✓ 
(do not extract them into subdirectories all images in one folder) - ✓
then get path to every image
from the path extract:

- date of acqusition
- band or product to insert into postgresql table
- type of satellite

Then join based on date of acquisition. 

After that take random image and with PIL extract 'im_height' and 'im_width'

EPSG is constant: 32633
spatial resolution is constant: 5m/px

'glacier' will be updated in QGIS based on TopoSvalbard.

'''

if __name__ == "__main__":
    main()
