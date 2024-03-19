import os
import magic
import re
import pandas as pd
import rasterio


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
                image_id = file[-9:-5]

                # Retrieving information from image properties
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
                    epsg = int(epsg[0]) # because line above is returning list

                    spt_res = round((scale_x+(scale_y*-1))/2,2)

                    # converting bounding box to WKT format
                    left = bbox[17:30].replace(',', '').replace(')', '')
                    bottom = bbox[39:53].replace(',', '').replace(')', '')
                    right = bbox[61:75].replace(',', '').replace(')', '')
                    top = bbox[80:94].replace(',', '').replace(')', '')

                    wkt = f"POLYGON(({left} {bottom}, {right} {bottom}, {right} {top}, {left} {top}, {left} {bottom}))"
                    print(left)


                # Arrange information into directory
                info_per_file = {'scene_id': image_id,
                                 'satellite': satellite,
                                 'acquisition_date': acquisition_date,
                                 'level': product_level,
                                 'band': band,
                                 'epsg':epsg,
                                 'spatial_resolution':spt_res,
                                 'bbox':wkt,
                                 'im_height': im_height,
                                 'im_width': im_width,
                                 'path': path}

                optic_imagery_info.append(info_per_file)
        df = pd.DataFrame(optic_imagery_info)
        csv_file = df.to_csv(f'{output_dir}\optic.csv',index=False)
        return csv_file
