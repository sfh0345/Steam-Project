import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Maak een verbinding met de PostgreSQL-database. Staat op localhost!!

conn = psycopg2.connect(
    database="steam",
    user="postgres",
    password="@Hilversum02@",
    port="5432"
)

# Maak een cursor
c = conn.cursor()

# haal de data op uit de database
def get_data():
    c.execute("SELECT verhouding_rating, average_playtime, total_reviews "
              "FROM gameproperties "
              "WHERE total_reviews > 8000 AND release_date > '2009-01-01' AND average_playtime < 15000 AND average_playtime > 4000")
    result = c.fetchall()
    return result


def gradien_descent(verhouding_rating, average_playtime, learning_rate, Iterations):
    # verander de de namen naar x en y
    x = verhouding_rating
    y = average_playtime

    # initaliseer de waarden van m en b
    m = 0
    b = 0

    # bereken de lengte van de dataset
    n = float(len(x))

    # implementeer gradient descent
    for i in range(Iterations):
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
    total_reviews = np.array([i[2] for i in data])

    # Bereken de m en b waarden
    m, b = gradien_descent(x, y, 0.0001, 10000)

    # Bereken de y waarden
    y_pred = m * verhouding_rating + b
    return y_pred

def voorspel_playtime(gamename):
    # Haal de data op uit de database
    c.execute("SELECT verhouding_rating "
              "FROM gameproperties "
              "WHERE name = %s", (gamename,))
    result = c.fetchone()
    verhouding_rating = result[0]
    y_pred = round(linear_regression(verhouding_rating))

    # sluit de database verbinding
    c.close()
    conn.close()

    print(f"De verwachte speeltijd is {y_pred} minuten.")
    return y_pred




