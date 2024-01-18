import requests
import psycopg2
from database_connection import connect_to_azure_postgresql, close_connection
""" 
    Deze functie geeft de top 5 genres van een gebruiker terug op basis van de speeltijd van hun gespeelde games.
"""

# Maak een verbinding met de PostgreSQL-database. Staat op localhost!!
conn = connect_to_azure_postgresql()

# Maak een cursor
c = conn.cursor()

def meest_gespeelde_genres(steamid):
    try:
        # Haal de speeltijd op van alle games die door de gebruiker zijn gespeeld
        playtime_games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=B5A67039860C1613632C4795B6C36245&steamid={steamid}&format=json"
        response = requests.get(playtime_games_url)

        if response.status_code == 200:
            # Haal de speeltijd, genre, naam en appid op van elke game en plaats deze in een dictionary
            meest_gespeelde_games = {}
            for game in response.json().get("response", {}).get("games", []):
                speeltijd = game["playtime_forever"]
                if speeltijd > 0:  # Games met nul speeltijd uitsluiten
                    meest_gespeelde_games[game["appid"]] = speeltijd

            # Voeg de genres en naam toe voor elke game aan de dictionary met behulp van geparametriseerde queries
            for appid in meest_gespeelde_games:
                c.execute("SELECT genres FROM gameproperties WHERE appid = %s", (appid,))
                result = c.fetchone()

                # Controleer of het resultaat niet None is voordat de elementen worden benaderd
                if result is not None:
                    genres = result[0]
                    meest_gespeelde_games[appid] = {"speeltijd": meest_gespeelde_games[appid], "genres": genres.split(';') if genres else []}
                else:
                    # Behandel het geval waarin geen genres zijn gevonden
                    meest_gespeelde_games[appid] = {"speeltijd": meest_gespeelde_games[appid], "genres": []}

            # Games met nul speeltijd filteren
            meest_gespeelde_games = {appid: details for appid, details in meest_gespeelde_games.items() if details["speeltijd"] > 0}

            # Games sorteren op speeltijd
            meest_gespeelde_games = sorted(
                meest_gespeelde_games.items(),
                key=lambda x: x[1]["speeltijd"],
                reverse=True
            )

            # Maak een dictionary met de totale speeltijd per genre
            genres = {}
            for game in meest_gespeelde_games:
                for genre in game[1]["genres"]:
                    if genre in genres:
                        genres[genre] += game[1]["speeltijd"]
                    else:
                        genres[genre] = game[1]["speeltijd"]
            # Sorteer de genres op speeltijd
            genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
            # Maak een dictionary met de top 5 genres
            genres = genres[:5]

            return genres
        else:
            print(f"Het ophalen van meest gespeelde games is mislukt. Status Code: {response.status_code}")
            return {}

    except psycopg2.Error as e:
        print(f"Fout met PostgreSQL: {e}")
        return {}

    finally:
        # Sluit de cursor en de databaseverbinding
        c.close()
        close_connection(conn)

# Druk het resultaat van de functie af
print(meest_gespeelde_genres("76561199022018738"))