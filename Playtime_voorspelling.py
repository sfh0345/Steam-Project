import numpy as np
import requests
import psycopg2
from database_connection import connect_to_azure_postgresql
from database2_connection import connect_to_azure_postgresql2


# Maak een verbinding met de PostgreSQL-database.
conn = connect_to_azure_postgresql()

# Maak een cursor
c = conn.cursor()


# haal de data op uit de database
def get_data():
    """
       Retrieve game data from the database.

       Returns:
           list: List of tuples containing (verhouding_rating, average_playtime, total_reviews) for selected games.
       """
    c.execute("SELECT verhouding_rating, average_playtime, total_reviews "
              "FROM gameproperties "
              "WHERE total_reviews > 8000 AND release_date > '2009-01-01' AND average_playtime < 15000 AND average_playtime > 4000")
    result = c.fetchall()
    return result


def gradient_descent(verhouding_rating, average_playtime, learning_rate, iterations):
    """
       Perform gradient descent to find the coefficients (m, b) for linear regression.

       Args:
           verhouding_rating (numpy.ndarray): Array of verhouding_rating values.
           average_playtime (numpy.ndarray): Array of average_playtime values.
           learning_rate (float): Learning rate for gradient descent.
           iterations (int): Number of iterations for gradient descent.

       Returns:
           tuple: Coefficients (m, b) for the linear regression model.
       """
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
    """
       Perform linear regression based on the provided verhouding_rating.

       Args:
           verhouding_rating (float): Verhouding rating of a specific game.

       Returns:
           float: Predicted playtime based on linear regression.
       """
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
    """
       Predict playtime for a given game.

       Args:
           gamename (str or int): Name or app ID of the game.

       Returns:
           int or None: Predicted playtime in hours or None if prediction failed.

       Raises:
           ValueError: If no data is found for the given gamename or appid.
       """

    if isinstance(gamename, str):
        # Haal de data op uit de database
        c.execute("SELECT verhouding_rating,name "
                  "FROM gameproperties "
                  "WHERE name ILIKE %s", ('%' + gamename + '%',))
    elif isinstance(gamename, int):
        c.execute("SELECT verhouding_rating,name "
                  "FROM gameproperties "
                  "WHERE appid = %s", (gamename,))
    else:
        print("Er is iets mis gegaan")

    result = c.fetchone()

    if result is None:
        # maak connectie met de database
        conn = connect_to_azure_postgresql2()

        # maak een cursor
        cursor = conn.cursor()
        if isinstance(gamename, str):
            # Haal de data op uit de database
            cursor.execute("SELECT sid "
                           "FROM gameproperties "
                           "WHERE name ILIKE %s", ('%' + gamename + '%',))
            result = c.fetchone()
            if result is not None:
                # doe een api call naar steamspy
                url = f"https://steamspy.com/api.php?request=appdetails&appid={result[0]}"
                response = requests.get(url)
                # haal de naam op
                name = response.json().get("name", 0)
                # haal positive en negative ratings op
                positive_ratings = response.json().get("positive", 0)
                negative_ratings = response.json().get("negative", 0)
                # bereken de verhouding
                totaal = positive_ratings + negative_ratings
                verhouding_rating = positive_ratings / totaal * 100 if totaal != 0 else 0
                return verhouding_rating, name
            else:
                return ["--", gamename]

        elif isinstance(gamename, int):
            # doe een api call naar steamspy
            url = f"https://steamspy.com/api.php?request=appdetails&appid={gamename}"
            response = requests.get(url)
            # haal positive en negative ratings op
            positive_ratings = response.json().get("positive", 0)
            negative_ratings = response.json().get("negative", 0)
            # bereken de verhouding
            totaal = positive_ratings + negative_ratings
            verhouding_rating = positive_ratings / totaal * 100 if totaal != 0 else 0
            # haal ook de naam op
            name = response.json().get("name", 0)
            return verhouding_rating, name
        else:
            print("Er is iets mis gegaan")

    else:
        verhouding_rating = result[0]
        name = result[1]

    y_pred = linear_regression(verhouding_rating)
    pred_playtime = round(y_pred / 60)

    return f"{pred_playtime} Hours", name


# print(voorspel_playtime(1979280))
