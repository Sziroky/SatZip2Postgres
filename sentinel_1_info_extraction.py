import os
import magic
import re
import pandas as pd


def extract_info_from_sar(sar_imagery_folder: str, output_dir: str):
    sar_imagery_info = []
    for root, dirs, files in os.walk(sar_imagery_folder):
        for file in files:
            if 'Sentinel-1' in file:
                print(f"Sentinel-1: started extracting informations from {file}\n{'-' * 100}")
                path = os.path.join(root, file)
                # retrieving information from file name:
                acquisition_date = file[:10]
                acq_mode = file[49:51]
                satellite = file[34:44]
                polarization = file[57:59]

                # retrieving information about units
                unit = file[62:75]
                if 'linear_gamma0' in unit:
                    unit = 'linear'
                if 'decibel_gamma' in unit:
                    unit = 'decibel'

                # retrieving information about correction type:
                correction_type = file[78:]
                if 'radiometric_terrain_corrected' in correction_type:
                    correction_type = 'radiometric'
                if 'orthorectified' in correction_type:
                    correction_type = 'orthorectified'

                # Retrieving information from image properieties
                info = magic.from_file(os.path.join(root, file))

                pattern_h = r"height=(\d+)"
                pattern_w = r"width=(\d+)"

                match_h = re.search(pattern_h, info)
                match_w = re.search(pattern_w, info)

                im_height = match_h.group(1) if match_h else None
                im_width = match_w.group(1) if match_w else None

                # Arrange information into directory
                info_per_file = {'satellite': satellite,
                                 'acquisition_date': acquisition_date,
                                 'acq_mode': acq_mode,
                                 'polarization': polarization,
                                 'unit': unit,
                                 'im_height': im_height,
                                 'im_width': im_width,
                                 'path': path}

                sar_imagery_info.append(info_per_file)
        df = pd.DataFrame(sar_imagery_info)
        csv_file = df.to_csv(f'{output_dir}\sar.csv')
        return csv_file

# extract_info_from_sar('D:\Praca_magisterska\scripts\images','D:\Praca_magisterska\scripts\output')

# for filename in os.listdir('D:\Praca_magisterska\scripts\images'):
#     if 'Sentinel-1' in filename:
#         extract_info_from_sar('D:\Praca_magisterska\scripts\images','D:\Praca_magisterska\scripts\output')
#
#     else:
#         print('Sentinel-2 file')
