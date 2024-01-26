import numpy as np
from database_connection import connect_to_azure_postgresql, close_connection


# Maak een verbinding met de PostgreSQL-database.
conn = connect_to_azure_postgresql()

# Maak een cursor
c = conn.cursor()


# haal de data op uit de database
def get_data():
    c.execute("SELECT verhouding_rating, average_playtime, total_reviews "
              "FROM gameproperties "
              "WHERE total_reviews > 8000 AND release_date > '2009-01-01' AND average_playtime < 15000 AND average_playtime > 4000")
    result = c.fetchall()
    return result


def gradient_descent(verhouding_rating, average_playtime, learning_rate, iterations):
    # verander de namen naar x en y
    x = verhouding_rating
    y = average_playtime

    # initialiseer de waarden van m en b
    m = 0
    b = 0

    # bereken de lengte van de dataset
    n = float(len(x))

    # implementeer gradient descent
    for i in range(iterations):
        y_pred = m * x + b
        dm = (-2/n) * sum(x * (y - y_pred))
        db = (-2/n) * sum(y - y_pred)
        m = m - learning_rate * dm
        b = b - learning_rate * db

    return m, b


def linear_regression(verhouding_rating):
    # Haal de data op uit de database
    data = get_data()

    # Zet de data om naar een numpy array
    x = np.array([i[0] for i in data])
    y = np.array([i[1] for i in data])

    # Bereken de m en b waarden
    m, b = gradient_descent(x, y, 0.0001, 10000)

    # Bereken de y waarden
    y_pred = m * verhouding_rating + b
    return y_pred


def voorspel_playtime(gamename):

    if isinstance(gamename, str):
        # Haal de data op uit de database
        c.execute("SELECT verhouding_rating "
                  "FROM gameproperties "
                  "WHERE name = %s", (gamename,))
    elif isinstance(gamename, int):
        c.execute("SELECT verhouding_rating "
                  "FROM gameproperties "
                  "WHERE appid = %s", (gamename,))
    else:
        print("Er is iets mis gegaan")

    result = c.fetchone()
    verhouding_rating = result[0]
    y_pred = linear_regression(verhouding_rating)
    pred_playtime = round(y_pred / 60)

    # sluit de database verbinding
    # c.close()
    # close_connection(conn)

    return pred_playtime

print(voorspel_playtime("Grand Theft Auto V"))
