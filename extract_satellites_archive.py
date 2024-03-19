import os
import zipfile
import uuid

def extract_archives(zip_files_dir: str, extract_folder: str):
    for root, dirs, files in os.walk(zip_files_dir):
        for file in files:
            print(f"started extracting files from {file}\n{'-'*100}")
            if file.endswith('.zip'):
                with zipfile.ZipFile(os.path.join(root, file), mode='r') as archive:
                    unique_id = str(uuid.uuid4())[:4]
                    extract_path = os.path.join(extract_folder, f"{file[:-4]}_{unique_id}")
                    archive.extractall(extract_path)
        for root, dirs, files in os.walk(extract_folder):
            for dir in dirs:
                id = dir[-4:]
                path_to_dir = os.path.join(root, dir)
                for file in os.listdir(os.path.join(root, dir)):
                    filename, file_extension = os.path.splitext(file)
                    new_filename = f"{filename}_{id}{file_extension}"
                    src = os.path.join(path_to_dir, file)
                    dst = os.path.join(extract_folder, new_filename)
                    # print(f'{src}\n--> {dst}')
                    os.rename(src, dst)
        for root,dirs,files in os.walk(extract_folder):
            for dir in dirs:
                os.rmdir(os.path.join(root,dir))