import psycopg2
import os

from extract_satellites_archive import extract_archives

from sentinel_1_info_extraction import extract_info_from_sar
from sentinel_2_info_extraction import extract_info_from_optic

from aggregation_of_scene import s1_merge_images_per_scene, s2_merge_images_per_scene

from Postgis_integration import postgresql_connection, execute_queries
from sql_queries import create_tables, remove_s2info_duplicates, remove_s1info_duplicates


class SatelliteError(Exception):
    pass


def main():
    global conn, s2queries, s1queries, s2rasters, s1rasters


    # GREETING
    print(f"\n{'*'*50}  SatZip2Postgres(GDOFO)   {'*'*50}\n\nDear User, This program can be used for extracting Satellite images from zip archives, "
          "extract scenes information as .csv file \nand for creating of Postgis Database with Extracted and transform info.\n\n"
          "NOTICE!!! For now this program extract good quality info from Sentinel-1 & Sentinel-2 Satellites\n"
          "Program Still in development state. Glad You using it :D.\n"
          )
    #PATH DECLARING

    path_to_zip_archives = input("Type Full Path where your .zip archives are:")
    images = input("Type Full Path where you want your images to be unpacked:")
    output = input("Type Full Path where you want to store .csv files:")
    config_file = input("Type Full Path where you have your config.ini file with Postgis credentials:")

    # UNPACKING
    question = input("\n\nLet's start!\nDo you want to unpack satellite images? (Y/n):")
    answer = question.lower()
    if answer == 'y':
        print('Starting the Proces of Satellite Image Archive Information Extraction...\n\n')
        extract_archives(path_to_zip_archives, images)
        print(
            f"Files extracted successfully into: {images}\n\n")
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

    # CREATING
    question = input("Create (N)ew Tables in database or use (E)xisting tables? (N/E)")
    answer = question.lower()
    if answer == 'n':
        create_tables(conn)
    elif answer == 'e':
        print('Using Existing tables. \nWARNING! names of the tables are hardcoded check names of tables before inserting the data.\n')
    else:
        print("command not recognized!")
        pass

    # COLLECTING
    question = input('\nDo you want to collect file information? (Y/n):')
    answer = question.lower()
    if answer == 'y':
        question = input('From which Sentinel? (1/2/both):')
        answer = question.lower()
        if answer == '1':
            s1queries,  s1rasters = extract_info_from_sar(images, output)
        elif answer == '2':
            s2queries, s2rasters = extract_info_from_optic(images, output)
        elif answer == 'both':
            s2queries, s2rasters = extract_info_from_optic(images, output)
            s1queries, s1rasters = extract_info_from_sar(images, output)
        else:
            print("command not recognized!")
            pass
        print(f'\nProcess finished. The output .csv files is in {output}\n')
    if answer == 'n':
        "Skipping process of collecting information's"

    # TRANSACTIONS
    question = input("Insert data into PosgreSQL database? (Y/n)")
    answer = question.lower()
    if answer == 'y':
        execute_queries(conn, s2queries)
        execute_queries(conn, s1queries)
        remove_s2info_duplicates(conn)
        remove_s1info_duplicates(conn)
    elif answer == 'n':
        print('Skip Transactions\n')
    else:
        print("command not recognized!")
        pass


    # AGGREGATING
    question = input('\nDo you want to aggregate images per scene into one record (in csv file) ? (Y/n):')
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
    print('\nThanks for using SatZip2postgres (GDOFO)!')
    # END CONNECTION
    if conn is not None:
        conn.close()


if __name__ == "__main__":
    main()
