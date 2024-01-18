import psycopg2

def connect_to_azure_postgresql():
    try:
        # Replace the placeholder values with your actual Azure PostgreSQL connection details
        connection_params = {
            "database": "DBsrv",
            "user": "postgres",
            "password": "Steam2023!@#",
            "host": "51.11.163.195",
            "port": 5432,  # Default PostgreSQL port
            "sslmode": "require",
        }

        connection = psycopg2.connect(**connection_params)
        print("Connected to the database!")

        return connection

    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        raise

def close_connection(connection):
    try:
        if connection:
            connection.close()
            print("Connection closed.")
    except Exception as e:
        print(f"Error: Unable to close the connection. {e}")
        raise