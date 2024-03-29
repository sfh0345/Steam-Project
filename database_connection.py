import psycopg2

def connect_to_azure_postgresql():
    try:
        connection_params = {
            "database": "DBsrv",
            "user": "postgres",
            "password": "Steam2023!@#",
            "host": "51.11.163.195",
            "port": 5432,  # Default PostgreSQL port
            "sslmode": "require",
        }

        connection = psycopg2.connect(**connection_params)


        return connection

    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        raise

def close_connection(connection):
    # pass the close connection because of different screens and multiple uses of the database
    pass