
def create_tables(conn):
    cur = conn.cursor()
    # Sentinel-2 tables
    table_s2_images = 'create table SENTINEL_02_IMAGES(IMAGE_ID serial, SCENE_ID varchar(5), IMG_HEIGHT integer, IMG_WIDTH integer, IMG_PATH varchar(200));'
    table_s2_info = 'create table SENTINEL_02_INFO(INFO_ID serial, SCENE_ID varchar(5), ACQUISITION_DATE date, LEVEL varchar(5), SPATIAL_RES float, EPSG integer);'
    table_s2_raster = 'create table SENTINEL_02_RASTER(RASTER_ID serial, SCENE_ID varchar(5), BAND varchar(3), RASTER_PATH  varchar(200),  SCENE raster);'
    table_s2_geometry = 'create table SENTINEL_02_GEOMETRY(GEOM_ID serial,SCENE_ID varchar(5),EPSG integer,BBOX geometry);'

    # Sentinel-1 tables
    table_s1_image = 'CREATE TABLE SENTINEL_01_IMAGES(IMAGE_ID serial,SCENE_ID varchar(5), IMG_HEIGHT integer, IMG_WIDTH integer, IMG_PATH varchar(200));'
    table_s1_info = 'CREATE TABLE SENTINEL_01_INFO(INFO_ID serial, SCENE_ID varchar(5), ACQUISITION_DATE date, POLARIZATION varchar(50), UNIT varchar(10), CORRECTION_TYPE varchar(50), SPATIAL_RESOLUTION float, EPSG integer);'
    table_s1_raster = 'create table SENTINEL_01_RASTER(RASTER_ID serial, SCENE_ID varchar(5), CODE varchar(50),RASTER_PATH  varchar(200),  SCENE raster);'
    table_s1_geometry = 'CREATE TABLE SENTINEL_01_GEOMETRY(GEOM_ID serial, SCENE_ID varchar, EPSG integer, BBOX geometry, CENTROID POINT);'

    list_of_queries = [table_s1_geometry,table_s1_raster,table_s1_info,table_s1_image,table_s2_geometry,table_s2_info,table_s2_raster,table_s2_images]
    try:
        # Execute each query in the list
        n = 0
        for query in list_of_queries:
            cur.execute(query)
            n = n+1

        # Commit the transaction
        conn.commit()
        print(f"Executed {n} transactions in total. Tables created. ")

    except Exception as e:
        print("Error:", e)
        conn.rollback()

def remove_s2info_duplicates(conn):
    query = ('delete from sentinel_02_info where info_id not in (select min (info_id) from sentinel_02_info group by '
             'scene_id);')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

def remove_s1info_duplicates(conn):
    query = ('delete from sentinel_01_info where info_id not in (select min (info_id) from sentinel_01_info group by '
             'scene_id);')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()