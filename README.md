Following script is used to extract files and information about satellite images, 
sort them and insert them to PostgresSql(PostGIS) database.

replace variables with your paths bellow, to extract information from files downloaded via SentinelHub:
- path_to_zip_archives: in this directory should be .zip files that you downloaded from SentinelHub (should have .zip files in it).
- images: specify directory in which the extracted images will be stored (can be empty).
- output: specify directory where the csv files will be generated (should be empty).

!For now, it works only on Sentinel-1 and Sentinel-2 download!

The extraction part works well and the output of the process is .csv files for optic and sar imagery.
Data came from filenames but some of them should be extract from metadata.

   csv 'optic' structure:
   scene_id | satellite | acquisition_date | level | band | im_height | im_width | path

   csv 'sar' structure:
   scene_id | satellite | acquisition_date | acq_mode | polarization | unit | correction_type | code | im_height | im_width | path