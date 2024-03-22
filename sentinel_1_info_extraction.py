import os
import magic
import re
import pandas as pd
import rasterio


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
                # Getting scene unique id
                image_id = file[-9:-5]

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
                elif 'orthorectified' in correction_type:
                    correction_type = 'orthorectified'
                else:
                    correction_type = 'not_corrected'

                code = polarization + '_' + unit + '_' + correction_type

                # Retrieving information from image properieties
                info = magic.from_file(os.path.join(root, file))

                pattern_h = r"height=(\d+)"
                pattern_w = r"width=(\d+)"

                match_h = re.search(pattern_h, info)
                match_w = re.search(pattern_w, info)

                im_height = match_h.group(1) if match_h else None
                im_width = match_w.group(1) if match_w else None

                # Retrieving information from image metadata
                with rasterio.open(os.path.join(root, file)) as src:
                    crs = src.crs
                    scale_x, rotation_x, translation_x, rotation_y, scale_y, translation_y, coord_1, coord2, coord3 = src.transform
                    bbox = str(src.bounds)

                    epsg = re.findall(r'\d+', str(crs))
                    epsg = int(epsg[0])  # because line above is returning list

                    spt_res = round((scale_x + (scale_y * -1)) / 2, 2)

                    # converting bounding box to WKT format
                    left = bbox[17:30].replace(',', '').replace(')', '')
                    bottom = bbox[39:53].replace(',', '').replace(')', '')
                    right = bbox[61:75].replace(',', '').replace(')', '')
                    top = bbox[80:94].replace(',', '').replace(')', '')

                    wkt = f"POLYGON(({left} {bottom}, {right} {bottom}, {right} {top}, {left} {top}, {left} {bottom}))"

                # Arrange information into directory
                info_per_file = {'scene_id': image_id,
                                 'satellite': satellite,
                                 'acquisition_date': acquisition_date,
                                 'acq_mode': acq_mode,
                                 'polarization': polarization,
                                 'unit': unit,
                                 'correction_type': correction_type,
                                 'code': code,
                                 'epsg': epsg,
                                 'spatial_resolution': spt_res,
                                 'bbox': wkt,
                                 'im_height': im_height,
                                 'im_width': im_width,
                                 'path': path,
                                 'glacier':'unknown'}

                sar_imagery_info.append(info_per_file)
        df = pd.DataFrame(sar_imagery_info)
        csv_file = df.to_csv(f'{output_dir}\sar.csv',index=False)
        return csv_file