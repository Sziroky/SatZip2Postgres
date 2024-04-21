The following script can be used to extract files and information about satellite images, downloaded directly from Sentinel Hub, sort them and insert them to PostgresSql(PostGIS) database.

WORK IN PROGRESS! For now, it works only on Sentinel-1 and Sentinel-2 Satellite archives!

How to use it briefly:

1. Download this repo on your local computer and install the required packages.
2. Create the config.ini file with Postgres credentials. For structure look at the template.
3. Execute the main script and then you decide what you want to be done:
   
      Only extract Satelite archives, or extract archives and info from files to get the .csv file,
      create a database, or insert extracted information into an existing one?
      It's up to You. 
      

The extraction part works well and one of the outputs of the process is .csv files for optic and sar imagery.
Data came from filenames, metadata, and Postgis functions.

Where are You using SatZip2Postgres for extracting information from images CSV files will be created for each satellite that you define.

CSV 'optic' (Sentinel-2) structure:

   scene_id | satellite | acquisition_date | level | band | im_height | im_width | path

CSV 'sar' (Sentinel-1) structure:

   scene_id | satellite | acquisition_date | acq_mode | polarization | unit | correction_type | code | im_height | im_width | path

This repository is part of a bigger project that combines AI and Satellite Imagery.
Using SatZip2Postgres could be very helpful in organizing files, giving the images specific IDs, and analyzing the data.

One of the features of SatZIP2Postgres is that you can insert extracted information into the Postgres Database.
If You do not have Tables in DB:

Four tables will be created for each Satellite:

(Satelite)_IMAGES - this table stores information about image properties like width height path

(Satelite)_INFO - this table stores information about Metadata like spatial resolution, EPSG, and Acquisition date.

(Satelite)_GEOMETRY - in this table you will find Bounding boxes in WKT format that represent the Raster boundaries

(Satelite)_RASTER - This table is supposed to store raster in raster type format but for now, it is storing paths to images. Rasters can be imported using raster2pgsql and it works but not in the code right now.

If You have the tables already check the names of them. Table names are Hardcoded so the program won't work if the table names are different.

