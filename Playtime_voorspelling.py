import numpy as np
import requests
import psycopg2
from database_connection import connect_to_azure_postgresql
from database2_connection import connect_to_azure_postgresql2

# Connect to the PostgreSQL database.
conn = connect_to_azure_postgresql()

# Create a cursor
c = conn.cursor()

# Retrieve game data from the database
def get_data():
    """
       Retrieve game data from the database.

       Returns:
           list: List of tuples containing (rating_ratio, average_playtime, total_reviews) for selected games.
       """
    c.execute("SELECT rating_ratio, average_playtime, total_reviews "
              "FROM gameproperties "
              "WHERE total_reviews > 8000 AND release_date > '2009-01-01' AND average_playtime < 15000 AND average_playtime > 4000")
    result = c.fetchall()
    return result

def gradient_descent(rating_ratio, average_playtime, learning_rate, iterations):
    """
       Perform gradient descent to find the coefficients (m, b) for linear regression.

       Args:
           rating_ratio (numpy.ndarray): Array of rating_ratio values.
           average_playtime (numpy.ndarray): Array of average_playtime values.
           learning_rate (float): Learning rate for gradient descent.
           iterations (int): Number of iterations for gradient descent.

       Returns:
           tuple: Coefficients (m, b) for the linear regression model.
       """
    # Change variable names to x and y
    x = rating_ratio
    y = average_playtime

    # Initialize the values of m and b
    m = 0
    b = 0

    # Calculate the length of the dataset
    n = float(len(x))

    # Implement gradient descent
    for i in range(iterations):
        y_pred = m * x + b
        dm = (-2/n) * sum(x * (y - y_pred))
        db = (-2/n) * sum(y - y_pred)
        m = m - learning_rate * dm
        b = b - learning_rate * db

    return m, b

def linear_regression(rating_ratio):
    """
       Perform linear regression based on the provided rating_ratio.

       Args:
           rating_ratio (float): Rating ratio of a specific game.

       Returns:
           float: Predicted playtime based on linear regression.
       """
    # Retrieve data from the database
    data = get_data()

    # Convert the data to a numpy array
    x = np.array([i[0] for i in data])
    y = np.array([i[1] for i in data])

    # Calculate the m and b values
    m, b = gradient_descent(x, y, 0.0001, 10000)

    # Calculate the y values
    y_pred = m * rating_ratio + b
    return y_pred

def predict_playtime(gamename):
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
        # Retrieve data from the database
        c.execute("SELECT rating_ratio, name "
                  "FROM gameproperties "
                  "WHERE name ILIKE %s", ('%' + gamename + '%',))
    elif isinstance(gamename, int):
        c.execute("SELECT rating_ratio, name "
                  "FROM gameproperties "
                  "WHERE appid = %s", (gamename,))
    else:
        print("Something went wrong")

    result = c.fetchone()

    if result is None:
        # Connect to the second database
        conn = connect_to_azure_postgresql2()

        # Create a cursor
        cursor = conn.cursor()
        if isinstance(gamename, str):
            # Retrieve data from the second database
            cursor.execute("SELECT sid "
                           "FROM gameproperties "
                           "WHERE name ILIKE %s", ('%' + gamename + '%',))
            result = c.fetchone()
            if result is not None:
                # Make an API call to SteamSpy
                url = f"https://steamspy.com/api.php?request=appdetails&appid={result[0]}"
                response = requests.get(url)
                # Retrieve the name
                name = response.json().get("name", 0)
                # Retrieve positive and negative ratings
                positive_ratings = response.json().get("positive", 0)
                negative_ratings = response.json().get("negative", 0)
                # Calculate the ratio
                total = positive_ratings + negative_ratings
                rating_ratio = positive_ratings / total * 100 if total != 0 else 0
                return rating_ratio, name
            else:
                return ["--", gamename]

        elif isinstance(gamename, int):
            # Make an API call to SteamSpy
            url = f"https://steamspy.com/api.php?request=appdetails&appid={gamename}"
            response = requests.get(url)
            # Retrieve positive and negative ratings
            positive_ratings = response.json().get("positive", 0)
            negative_ratings = response.json().get("negative", 0)
            # Calculate the ratio
            total = positive_ratings + negative_ratings
            rating_ratio = positive_ratings / total * 100 if total != 0 else 0
            # Also retrieve the name
            name = response.json().get("name", 0)
            return rating_ratio, name
        else:
            print("Something went wrong")

    else:
        rating_ratio = result[0]
        name = result[1]

    y_pred = linear_regression(rating_ratio)
    pred_playtime = round(y_pred / 60)

    return pred_playtime, name

