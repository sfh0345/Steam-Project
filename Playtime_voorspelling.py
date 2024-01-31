import numpy as np
import requests
import psycopg2
from database_connection import connect_to_azure_postgresql
from database2_connection import connect_to_azure_postgresql2


# Make a connection to the database
conn = connect_to_azure_postgresql()

# Make a cursor
c = conn.cursor()


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
    # change the name to x and y
    x = verhouding_rating
    y = average_playtime

    # initialize m and b
    m = 0
    b = 0

    # calculate the length of the array
    n = float(len(x))

    # perform gradient descent
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
    # get the data
    data = get_data()

    # change the data to numpy arrays
    x = np.array([i[0] for i in data])
    y = np.array([i[1] for i in data])

    # calculate m and b
    m, b = gradient_descent(x, y, 0.0001, 10000)

    # calculate the predicted y
    y_pred = m * verhouding_rating + b
    return y_pred


def voorspel_playtime(gamename):
    """
       Predict playtime for a given game.

       Args:
           gamename (str or int): Name or app ID of the game.

       Returns:
           int or None: Predicted playtime in hours or None if prediction failed.
       """

    if isinstance(gamename, str):
        # make connection to the database
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
        # make connection to the database
        conn = connect_to_azure_postgresql2()

        # make a cursor
        cursor = conn.cursor()
        if isinstance(gamename, str):
            # get the appid of the game
            cursor.execute("SELECT sid "
                           "FROM gameproperties "
                           "WHERE name ILIKE %s", ('%' + gamename + '%',))
            result = c.fetchone()
            if result is not None:
                # make a api call to steamspy
                url = f"https://steamspy.com/api.php?request=appdetails&appid={result[0]}"
                response = requests.get(url)
                # get the name of the game
                name = response.json().get("name", 0)
                # get the positive and negative ratings
                positive_ratings = response.json().get("positive", 0)
                negative_ratings = response.json().get("negative", 0)
                # calculate the ratio
                totaal = positive_ratings + negative_ratings
                verhouding_rating = positive_ratings / totaal * 100 if totaal != 0 else 0
                return verhouding_rating, name
            else:
                return ["--", gamename]

        elif isinstance(gamename, int):
            # make a api call to steamspy
            url = f"https://steamspy.com/api.php?request=appdetails&appid={gamename}"
            response = requests.get(url)
            # get the positive and negative ratings
            positive_ratings = response.json().get("positive", 0)
            negative_ratings = response.json().get("negative", 0)
            # calculate the ratio
            totaal = positive_ratings + negative_ratings
            verhouding_rating = positive_ratings / totaal * 100 if totaal != 0 else 0
            # also get the name of the game
            name = response.json().get("name", 0)
            return verhouding_rating, name
        else:
            print("Er is iets mis gegaan")

    else:
        verhouding_rating = result[0]
        name = result[1]

    y_pred = linear_regression(verhouding_rating)
    pred_playtime = round(y_pred / 60)

    return pred_playtime, name


print(voorspel_playtime(1979280))
