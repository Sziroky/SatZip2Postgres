import psycopg2
import configparser


def postgresql_connection(config_file):
    # Read and get values from config file
    config = configparser.ConfigParser()
    config.read(config_file)

    # Create DB conection
    conn = psycopg2.connect(
        database=config['postgresql_conn']['dbname'],
        user=config['postgresql_conn']['user'],
        password=config['postgresql_conn']['password'],
        host=config['postgresql_conn']['host'],
        port=config['postgresql_conn'].getint('port', fallback=5432)  # Default port 5432
    )
    if conn:
        print(
            f"Successfully connected user: {config['postgresql_conn']['user']} to postgresql database {config['postgresql_conn']['dbname']} at port: {config['postgresql_conn']['port']} {config['postgresql_conn']['host']}\n")
    else:
        print('Something went wrong check config file.')
    return conn


def execute_queries(conn, list_of_queries):
    cur = conn.cursor()

    try:
        # Execute each query in the list
        n = 0
        for query in list_of_queries:
            cur.execute(query)
            n = n+1

        # Commit the transaction
        conn.commit()
        print(f"Executed {n} transactions in total. ")

    except Exception as e:
        print("Error:", e)
        conn.rollback()

    finally:
        # Close connection
        cur.close()

