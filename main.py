from sentinel_1_info_extraction import extract_info_from_sar
from sentinel_2_info_extraction import extract_info_from_optic
from extract_satellites_archive import extract_archives
from aggregation_of_scene import s1_merge_images_per_scene, s2_merge_images_per_scene
import os


class SatelliteError(Exception):
    pass


def main():
    """
    Following script is used to extract files and information about satellite images,
    sort them and insert them to PostgresSql(PostGIS) database.

    replace variables with your paths bellow, to extract information from files downloaded via SentinelHub:

        - path_to_zip_archives: in this directory should be .zip files that you downloaded from SentinelHub (should have .zip files in it).
        - images: specify directory in which the extracted images will be stored (can be empty).
        - output: specify directory where the csv files will be generated (should be empty).

    for now, it works only on Sentinel-1 and Sentinel-2 download.

    The extraction part works well and the output of the process is .csv files for optic and sar imagery.
    Data came from filenames but some of them should be extract from metadata.

    csv 'optic' structure:
    scene_id | satellite | acquisition_date | level | band | im_height | im_width | path

    csv 'sar' structure:
    scene_id | satellite | acquisition_date | acq_mode | polarization | unit | correction_type | code | im_height | im_width | path

    """

    path_to_zip_archives = r'D:\Praca_magisterska\scripts\satellite_imagery_archives'
    images = r'D:\Praca_magisterska\scripts\images'
    output = r'D:\Praca_magisterska\scripts\output'

    question = input('Do you want to unpack satellite images? (Y/n):')
    answer = question.lower()
    if answer == 'y':
        print('Starting the Proces of Satellite Image Archive Information Extraction...\n\n')
        extract_archives(path_to_zip_archives, images)
        print(f"Files extracted successfully into: {images}\n\nAcquisition of Files Information Started...\n{'v' * 100}\n")
    elif answer == 'n':
        print('Skipping process of extracting archives\n')

    question = input('Do you want to collect file information? (Y/n):')
    answer = question.lower()
    if answer == 'y':
        question = input('From which Sentinel? (1/2/both):')
        answer = question.lower()
        if answer == '1':
            extract_info_from_sar(images, output)
        elif answer == '2':
            extract_info_from_optic(images, output)
        elif answer == 'both':
            extract_info_from_optic(images, output)
            extract_info_from_sar(images, output)
        else:
            print("command not recognized!")
            pass
        print(f'\nProcess finished. The output files is in {output}')
    if answer == 'n':
        "Skipping process of collecting information's"

    question = input('\nDo you want to aggregate images per scene into one record? (Y/n):')
    answer = question.lower()
    if answer == 'y':
        for root, dirs, files in os.walk(output):
            for file in files:
                if file == 'optic.csv':
                    s2_merge_images_per_scene(os.path.join(root,file))
                    print('check')
                elif file == 'sar.csv':
                    s1_merge_images_per_scene(os.path.join(root,file))
                else:
                    print(
                        f"Unrecognized csv file: {os.path.join(root,file)} in {output}")
        print("\nThank You. Your Images and Information's are extracted.")
    elif answer == 'n':
        print("\nThank You. Your Images and Information's are extracted.")



'''
EPSG is constant: 32633
spatial resolution is constant: 5m/px
'glacier' will be updated in QGIS based on TopoSvalbard.
'''

if __name__ == "__main__":
    main()
