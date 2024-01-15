import psycopg2

def connect_to_azure_postgresql():
    try:
        connection_params = {
            "database": "DBsrv",
            "user": "postgres",
            "password": "Steam2023!@#",
            "host": "51.11.163.195",
            "port": 5432,
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

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        for row in results:
            print(row)

        cursor.close()

    except psycopg2.Error as e:
        print(f"Error: Unable to execute the query. {e}")
        raise

if __name__ == "__main__":
    azure_postgresql_connection = connect_to_azure_postgresql()

    example_query = "SELECT genres FROM gameproperties"
    execute_query(azure_postgresql_connection, example_query)

    # Close the connection when done
    close_connection(azure_postgresql_connection)