import psycopg2

from sentinel_1_info_extraction import extract_info_from_sar
from sentinel_2_info_extraction import extract_info_from_optic
from extract_satellites_archive import extract_archives
from aggregation_of_scene import s1_merge_images_per_scene, s2_merge_images_per_scene
import os
from Postgis_integration import postgresql_connection, execute_queries


class SatelliteError(Exception):
    pass


def main():
    global conn, s2queries
    # PATHS
    path_to_zip_archives = r'D:\Praca_magisterska\scripts\satellite_imagery_archives'
    images = r'D:\Praca_magisterska\scripts\images'
    output = r'D:\Praca_magisterska\scripts\output'
    config_file = r'D:\Praca_magisterska\scripts\conf.ini'

    # GREETING
    print("Welcome, some details here...\n\n")

    # UNPACKING
    question = input('Do you want to unpack satellite images? (Y/n):')
    answer = question.lower()
    if answer == 'y':
        print('Starting the Proces of Satellite Image Archive Information Extraction...\n\n')
        extract_archives(path_to_zip_archives, images)
        print(
            f"Files extracted successfully into: {images}\n\nAcquisition of Files Information Started...\n{'v' * 100}\n")
    elif answer == 'n':
        print('Skipping process of extracting archives\n')

    # CONNECTING
    question = input("Connect to PosgreSQL database? (Y/n)")
    answer = question.lower()
    if answer == 'y':
        conn = postgresql_connection(config_file)
    elif answer == 'n':
        conn = None
        print('Skip Connection\n')
    else:
        print("command not recognized!")
        pass

    # COLLECTING
    question = input('Do you want to collect file information? (Y/n):')
    answer = question.lower()
    if answer == 'y':
        question = input('From which Sentinel? (1/2/both):')
        answer = question.lower()
        if answer == '1':
            s1queries = extract_info_from_sar(images, output)
        elif answer == '2':
            s2queries = extract_info_from_optic(images, output)
        elif answer == 'both':
            s2queries = extract_info_from_optic(images, output)
            s1queries = extract_info_from_sar(images, output)
        else:
            print("command not recognized!")
            pass
        print(f'\nProcess finished. The output files is in {output}')
    if answer == 'n':
        "Skipping process of collecting information's"

    # TRANSACTIONS
    question = input("Insert data into PosgreSQL database? (Y/n)")
    answer = question.lower()
    if answer == 'y':
        execute_queries(conn, s2queries)
    elif answer == 'n':
        print('Skip Transactions\n')
    else:
        print("command not recognized!")
        pass

    # AGGREGATING
    question = input('\nDo you want to aggregate images per scene into one record? (Y/n):')
    answer = question.lower()
    if answer == 'y':
        for root, dirs, files in os.walk(output):
            for file in files:
                if file == 'optic.csv':
                    s2_merge_images_per_scene(os.path.join(root, file))
                elif file == 'sar.csv':
                    s1_merge_images_per_scene(os.path.join(root, file))
                else:
                    print(
                        f"Unrecognized csv file: {os.path.join(root, file)} in {output}")
        print("\nThank You. Your Images and Information's are extracted.")
    elif answer == 'n':
        print("\nThank You. Your Images and Information's are extracted.")

    # END CONNECTION
    if conn is not None:
        conn.close()


if __name__ == "__main__":
    main()
