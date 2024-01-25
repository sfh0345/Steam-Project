import requests
import os
from database_connection import connect_to_azure_postgresql, close_connection
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import datetime

def most_played_games_user(steamid):

    STEAM_API_KEY = "B5A67039860C1613632C4795B6C36245"

    # Maak een verbinding met de PostgreSQL-database.
    conn = connect_to_azure_postgresql()

    # Maak een cursor
    c = conn.cursor()

    def get_games(steamid):
        """
        Retrieve the user's owned games from the Steam API.
        """
        try:
            url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steamid}&format=json"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            owned_games = response.json().get("response", {}).get("games", [])
            owned_games = [game for game in owned_games if game.get("playtime_forever", 0) > 0]
            return owned_games
        except requests.RequestException as e:
            print(f"Error retrieving user's owned games: {e}")
            return []

    def get_game_names(owned_games):
        """
        Retrieve names for the owned games from the database.
        """
        playtime_data = {}

        for game in owned_games:
            appid = game.get("appid")
            playtime_data[appid] = {"name": game.get("name", "Unknown"), "playtime": game.get("playtime_forever", 0)}

            # Check if the game is in the database and add the name to the list
            c.execute("SELECT name FROM gameproperties WHERE appid = %s", (appid,))
            result = c.fetchone()
            if result is not None:
                playtime_data[appid]["name"] = result[0]
            else:
                # get the name from the Steam API
                url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
                response = requests.get(url)
                if response.status_code == 200:
                    # add the name to the list if it is found in the API response set it to Unknown
                    playtime_data[appid]["name"] = response.json().get(str(appid), {}).get("data", {}).get("name", "Unknown")
                else:
                    print(f"Failed to retrieve game name. Status Code: {response.status_code}")

        return playtime_data

    def calculate_total_playtime(steamid):
        """
        Calculate the total playtime across all owned games.
        """
        owned_games = get_games(steamid)
        playtime_data = get_game_names(owned_games)
        total_playtime = sum(game["playtime"] for game in playtime_data.values())
        return total_playtime

    def create_pie_chart(steamid):
        owned_games = get_games(steamid)
        playtime_data = get_game_names(owned_games)
        total_playtime = calculate_total_playtime(steamid)

        # Check if the total playtime is greater than zero
        if total_playtime > 0:
            sorted_playtime_data = sorted(playtime_data.items(), key=lambda x: x[1]["playtime"], reverse=True)

            # Extract playtimes and game names for the pie chart
            playtimes = [entry[1]["playtime"] for entry in sorted_playtime_data]
            labels = [entry[1]["name"] for entry in sorted_playtime_data]

            # make sure the labels are not too long
            labels = [label[:20] + "..." if len(label) > 20 else label for label in labels]

            # Group items with less than 3% playtime as a single "Other" category
            threshold_percentage = 3.0
            min_playtime = total_playtime * (threshold_percentage / 100.0)

            # Calculate the total playtime of items to be grouped into "Other"
            other_playtime = sum(playtime for playtime in playtimes if playtime < min_playtime)

            # Filter out items with less than 3% playtime and add the "Other" category
            filtered_data = [(playtime, label) for playtime, label in zip(playtimes, labels) if
                             playtime >= min_playtime]
            filtered_data.append((other_playtime, "Other"))

            # Extract playtimes and game names for the corrected pie chart
            playtimes, labels = zip(*filtered_data)

            # Convert playtimes to hours and minutes format
            playtimes_hours_minutes = [f"{int(playtime // 60)}h {int(playtime % 60)}m" for playtime in playtimes]

            # Set the color scheme
            background_color = "#0E131A"
            text_color = "white"

            # Create a custom color map with the first color as the starting color and the rest getting darker
            cmap = cm.Blues_r  # "_r" reverses the color map
            colors = cmap(np.linspace(0, 0.7, len(playtimes)))

            # Set the figure and axis background color
            fig, ax = plt.subplots(figsize=(3.60, 4.35))  # set size of the figure to 360 x 435 pixels
            fig.set_facecolor(background_color)
            ax.set_facecolor(background_color)

            # Add total playtime text more to the left
            total_hours = int(total_playtime // 60)
            total_minutes = int(total_playtime % 60)
            plt.text(-1.3, 1.2, f"Total Playtime: {total_hours} Hours", fontsize=8, ha='left', va='top',
                     color=text_color)

            # Plot the pie chart with gradient slices
            wedges, texts, autotexts = plt.pie(playtimes, labels=labels, autopct=lambda pct: f'{int(pct * total_playtime / 100 // 60)} Hours',
                                               startangle=90, colors=colors,
                                               counterclock=True)  # Counter-clockwise to start darkest color on the left# Rotate the autotext labels to align with the center of the pie chart

            for i, (text, autotext) in enumerate(zip(texts, autotexts)):
                text.set_color(text_color)
                autotext.set_color(text_color)
                text.set_text(None)

            # Equal aspect ratio ensures the pie chart is circular
            plt.axis("equal")
            plt.title("Top Games Based on Playtime", color=text_color)

            # add a legend at the bottom of the pie chart
            plt.legend(labels, loc="lower center", bbox_to_anchor=(0.2, -0.15),
                       fontsize=8, mode='expand', ncol=2, frameon=False, labelcolor=text_color,
                       borderpad=0.5, handletextpad=0.5, columnspacing=0.5, handlelength=1.5, labelspacing=0.5)

            # get the date
            date = datetime.datetime.now()
            date = date.strftime("%d-%m-%Y")

            # save the plot
            plt.savefig(f'analytics/piechart_{steamid}_{date}.png')

            # close connection
            close_connection(conn)
        else:
            print("Total playtime is zero. Cannot create pie chart.")

    # get the date
    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")

    file_name = f"analytics/piechart_{steamid}_{date}.png"

    # Check if the file exists
    if os.path.exists(file_name):
        filepath = file_name
    else:
        create_pie_chart(steamid)
