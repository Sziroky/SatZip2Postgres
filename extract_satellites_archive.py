import os
import zipfile
import uuid


extract_folder = 'D:\Praca_magisterska\scripts\images'
zip_file = 'D:\Praca_magisterska\scripts\satellite_imagery_archives'

def extract_archives(zip_files_dir: str, extract_folder: str):
    for root, dirs, files in os.walk(zip_files_dir):
        for file in files:
            print(f"started extracting files from {file}\n{'-'*100}")
            if file.endswith('.zip'):
                with zipfile.ZipFile(os.path.join(root, file), mode='r') as archive:
                    archive.extractall(extract_folder)
                    uniqueid = str(uuid.uuid4())[:4]
                    for archive_file in os.listdir(extract_folder):
                        archive.extractall(extract_folder)
                        filename, file_extension = os.path.splitext(archive_file)
                        print(filename)
                        extracted_file_path = os.path.join(extract_folder, archive_file)
                        new_filename = f"{filename}_{uniqueid}{file_extension}"
                        print(uniqueid)
                        os.rename(extracted_file_path, os.path.join(extract_folder, new_filename))



    print(f'Successfully extracted into {extract_folder}')