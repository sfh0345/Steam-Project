import psycopg2

def connect_to_azure_postgresql():
    try:
        # Replace the placeholder values with your actual Azure PostgreSQL connection details
        connection_params = {
            "database": "DBsrv",
            "user": "DBsrv",
            "password": "your_password",
            "host": "your_server_name.postgres.database.azure.com",
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


    except psycopg2.Error as e:
        print(f"Error: Unable to execute the query. {e}")
        raise

if __name__ == "__main__":
    azure_postgresql_connection = connect_to_azure_postgresql()

    example_query = "SELECT * FROM your_table_name;"
    execute_query(azure_postgresql_connection, example_query)

    # Close the connection when done
    close_connection(azure_postgresql_connection)