import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import datetime
from database_connection import connect_to_azure_postgresql

def single_player_or_multi_player(steamid):
    """
    This function will give a pie chart consisting of the percentage single-player and multi-player games.
    It also shows the total owned games.
    It gets the percentages by using the Azure database and Steam API.
    """
    # Set Steam API key and Steam ID
    steam_api_key = '36FBD6438CC015CDEBDEFA4FF12E1256'

    # Function to get owned app IDs from the Steam API
    def get_owned_app_ids(steam_api_key, steamid):
        """
        This function returns the appid from the owned games of the steam user.
        It does that by using Steam API
        """
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steamid}&format=json'
        response = requests.get(url)
        # If the API request was succesful, so HTTP status code equals 200
        if response.status_code == 200:
            data = response.json()
            # Get the app Ids of owned games
            owned_appids = [game['appid'] for game in data['response']['games']]
            # Calculate the total amount of games
            total_games = len(owned_appids)
            # Return the owned appids and the total amount
            return owned_appids, total_games
        # If the API request was not successful
        # Print an error message
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    def check_game_mode(appid, cursor, counts_dict):
        """
        This function checks the game mode via the database and Steam API.
        First it checks if the game is in the database.
        If that is the case it looks if the game is single-player or multi-player.
        If that isn't the case it checks if the game is single-player or multi-player via steam API.
        The amount of single-player and multi-player are counted up in this function.
        """
        # check if the game is in the database
        cursor.execute("SELECT appid FROM gameproperties WHERE appid = %s", (appid,))
        result = cursor.fetchone()
        # if the game is in the database, check if it is single-player or multi-player
        if result:
            cursor.execute("SELECT appid, categories FROM gameproperties WHERE appid = %s AND categories LIKE %s",
                           (appid, '%Single-player%'))
            result_single = cursor.fetchone()
            cursor.execute("SELECT appid, categories FROM gameproperties WHERE appid = %s AND categories LIKE %s",
                           (appid, '%Multi-player%'))
            result_multi = cursor.fetchone()

            if result_single:
                counts_dict['Single-player'] += 1
            elif result_multi:
                counts_dict['Multi-player'] += 1

        elif not result:
            # Get the categories from the Steam API
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            response = requests.get(url)
            categories = response.json().get(str(appid), {}).get("data", {}).get("categories", {})
            # Check if the game is single-player or multi-player
            for category in categories:
                # If the category is Single-player add one to Single-player
                if category['description'] == 'Single-player':
                    counts_dict['Single-player'] += 1
                # If the category is Multi-player add one to Multi-player
                elif category['description'] == 'Multi-player':
                    counts_dict['Multi-player'] += 1

    def percentage_calc(steamid, cursor):
        """
        This function will calculate the percentage of single-player and multi-player games.
        """
        # Get the list of owned app IDs and the total number of games
        owned_appids, total_games = get_owned_app_ids(steam_api_key, steamid)
        # Make a dictionary to store the counts of Single-player and Multi-player games
        counts_dict = {'Single-player': 0, 'Multi-player': 0}
        # For each app ID in owned_appids check its game mode
        for app_id in owned_appids:
            check_game_mode(app_id, cursor, counts_dict)

        # Calculate the percentage of Single-player games and Multi-player games
        valid_games_count = total_games
        percentage_single = (counts_dict['Single-player'] / valid_games_count) * 100 if valid_games_count > 0 else 0
        percentage_multi = (counts_dict['Multi-player'] / valid_games_count) * 100 if valid_games_count > 0 else 0
        # The function returns the percentage of single and multi-player games
        return percentage_single, percentage_multi, valid_games_count

    def piechart(steamid):
        """
        The function will make a piechart representing the percentage of single-player and multi-player games.
        The total owned games will also be shown with the piechart.
        """
        # Connect to te Azure database
        conn = connect_to_azure_postgresql()
        cursor = conn.cursor()

        percentage_single, percentage_multi, valid_games_count = percentage_calc(steamid, cursor)
        # Define the labels, sizes and explode for the pie chart
        labels = ['Single-player', 'Multi-player']
        sizes = [percentage_single, percentage_multi]
        explode = (0.1, 0)
        # Give the chart a background- and textcolor
        background_color = "#0E131A"
        text_color = "white"
        colors = ["#08306B", "#84BCDB"]

        # Create a figure and exes for the chart
        fig, ax = plt.subplots(figsize=(3.60, 4.35))
        fig.set_facecolor(background_color)
        ax.set_facecolor(background_color)
        # Plot the chart with specified properties
        plt.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90,
                textprops={'color': text_color})

        # Display the total number of games as annotation in the top left corner
        total_games = valid_games_count
        plt.annotate(f'Total Games: {total_games}', xy=(-0.036, 0.9), xycoords='axes fraction',
                     fontsize=10, color=text_color)

        plt.axis("equal")
        # Give the pie chart the title: "Single-player vs Multi-player Games"
        plt.title("Single-player vs Multi-player Games", color=text_color, fontsize=13, y=1.02)
        # Add a legend to the pie chart
        plt.legend(labels, loc="lower center", bbox_to_anchor=(0.5, -0.15),
                   fontsize=10, mode='expand', ncol=2, frameon=False, labelcolor=text_color,
                   borderpad=0.5, handletextpad=0.5, columnspacing=0.5, handlelength=1.5, labelspacing=0.5)
        # Get the current date
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        # Cave the pei chart as an image file
        plt.savefig(f"analytics/singleplayerormultiplayer_{steamid}_{date}.png")

        # Close database connection
        cursor.close()
        conn.close()

    # get the date
    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")

    file_name = f"analytics/singleplayerormultiplayer_{steamid}_{date}.png"

    # Check if the file exists, if not, generate the pie chart
    if os.path.exists(file_name):
        filepath = file_name
    else:
        piechart(steamid)

