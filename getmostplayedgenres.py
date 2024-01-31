import requests
import psycopg2
from database_connection import connect_to_azure_postgresql, close_connection
""" 
    This function returns the top 5 genres of a user based on the playtime of their played games.
"""

# Connect to the PostgreSQL database
conn = connect_to_azure_postgresql()

# Create a cursor
c = conn.cursor()


def meest_gespeelde_genres(steamid):
    """
    Retrieve the top 5 genres of a user based on the playtime of their played games.
    """
    try:
        # Retrieve playtime of all games played by the user
        playtime_games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=B5A67039860C1613632C4795B6C36245&steamid={steamid}&format=json"
        response = requests.get(playtime_games_url)

        if response.status_code == 200:
            # Retrieve playtime, genre, name, and appid for each game and store them in a dictionary
            most_played_games = {}
            for game in response.json().get("response", {}).get("games", []):
                playtime = game["playtime_forever"]
                if playtime > 0:  # Exclude games with zero playtime
                    most_played_games[game["appid"]] = playtime

            # Add genres and name for each game to the dictionary using parameterized queries
            for appid in most_played_games:
                c.execute("SELECT genres FROM gameproperties WHERE appid = %s", (appid,))
                result = c.fetchone()

                # Check if the result is not None before accessing its elements
                if result is not None:
                    genres = result[0]
                    most_played_games[appid] = {"playtime": most_played_games[appid], "genres": genres.split(';') if genres else []}
                else:
                    # Handle the case where no genres are found
                    most_played_games[appid] = {"playtime": most_played_games[appid], "genres": []}

            # Filter games with zero playtime
            most_played_games = {appid: details for appid, details in most_played_games.items() if details["playtime"] > 0}

            # Sort games based on playtime
            most_played_games = sorted(
                most_played_games.items(),
                key=lambda x: x[1]["playtime"],
                reverse=True
            )

            # Create a dictionary with the total playtime per genre
            genres = {}
            for game in most_played_games:
                for genre in game[1]["genres"]:
                    if genre in genres:
                        genres[genre] += game[1]["playtime"]
                    else:
                        genres[genre] = game[1]["playtime"]
            # Sort genres based on playtime
            genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
            # Create a dictionary with the top 5 genres
            genres = genres[:5]

            return genres
        else:
            print(f"Failed to retrieve most played games. Status Code: {response.status_code}")
            return {}

    except psycopg2.Error as e:
        print(f"Error with PostgreSQL: {e}")
        return {}
    finally:
        close_connection(conn)
