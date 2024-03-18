import os
import magic
import re
import pandas as pd


def extract_info_from_optic(optic_imagery_folder: str, output_dir: str):
    optic_imagery_info = []
    for root, dirs, files in os.walk(optic_imagery_folder):
        for file in files:
            if 'Sentinel-2' in file:
                print(f"Sentinel-2: started extracting information from {file}\n{'-' * 100}")
                path = os.path.join(root, file)

                # retrieving information from file name:
                acquisition_date = file[:10]
                satellite = file[34:44]
                product_level = file[45:48]
                band = file[49:52]

                # Getting scene unique id
                image_id = file[54:]

                # Retrieving information from image properties
                info = magic.from_file(os.path.join(root, file))

                pattern_h = r"height=(\d+)"
                pattern_w = r"width=(\d+)"

                match_h = re.search(pattern_h, info)
                match_w = re.search(pattern_w, info)

                im_height = match_h.group(1) if match_h else None
                im_width = match_w.group(1) if match_w else None

                # Arrange information into directory
                info_per_file = {'image_id':image_id,
                                'satellite': satellite,
                                 'acquisition_date': acquisition_date,
                                 'level': product_level,
                                 'band': band,
                                 'im_height': im_height,
                                 'im_width': im_width,
                                 'path': path}

                optic_imagery_info.append(info_per_file)
        df = pd.DataFrame(optic_imagery_info)
        csv_file = df.to_csv(f'{output_dir}\optic.csv')
        return csv_file