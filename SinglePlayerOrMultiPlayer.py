import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import datetime
from database_connection import connect_to_azure_postgresql

def single_player_or_multi_player(steamid):
    # Set Steam API key and Steam ID
    steam_api_key = '36FBD6438CC015CDEBDEFA4FF12E1256'

    # Function to get owned app IDs from the Steam API
    def get_owned_app_ids(steam_api_key, steamid):
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steamid}&format=json'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            owned_appids = [game['appid'] for game in data['response']['games']]
            return owned_appids
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    def check_game_mode(appid, cursor, counts_dict):
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

    def percentage_calc(steamid, cursor):
        owned_appids = get_owned_app_ids(steam_api_key, steamid)
        counts_dict = {'Single-player': 0, 'Multi-player': 0}
        for app_id in owned_appids:
            check_game_mode(app_id, cursor, counts_dict)

        valid_games_count = counts_dict['Single-player'] + counts_dict['Multi-player']
        percentage_single = (counts_dict['Single-player'] / valid_games_count) * 100 if valid_games_count > 0 else 0
        percentage_multi = (counts_dict['Multi-player'] / valid_games_count) * 100 if valid_games_count > 0 else 0

        return percentage_single, percentage_multi

    def piechart(steamid):
        conn = connect_to_azure_postgresql()
        cursor = conn.cursor()

        percentage_single, percentage_multi = percentage_calc(steamid, cursor)

        labels = ['Single-player', 'Multi-player']
        sizes = [percentage_single, percentage_multi]
        explode = (0.1, 0)

        background_color = "#0E131A"
        text_color = "white"

        colors = ["#08306B", "#84BCDB"]


        fig, ax = plt.subplots(figsize=(3.60, 4.35))
        fig.set_facecolor(background_color)
        ax.set_facecolor(background_color)

        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90,
                textprops={'color': text_color})

        # Display the total number of games as annotation in the top left corner
        total_games = round(sum(sizes))
        plt.annotate(f'Total Games: {total_games}', xy=(-0.036, 0.9), xycoords='axes fraction',
                     fontsize=10, color=text_color)

        plt.axis("equal")
        plt.title("Single-player vs Multi-player Games", color=text_color, fontsize=13, y=1.02)

        plt.legend(labels, loc="lower center", bbox_to_anchor=(0.2, -0.15),
                   fontsize=8, mode='expand', ncol=2, frameon=False, labelcolor=text_color,
                   borderpad=0.5, handletextpad=0.5, columnspacing=0.5, handlelength=1.5, labelspacing=0.5)

        date = datetime.datetime.now().strftime("%d-%m-%Y")
        plt.savefig(f"analytics/singleplayerormultiplayer_{steamid}_{date}.png")


        cursor.close()
        conn.close()

    # get the date
    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")

    file_name = f"analytics/singleplayerormultiplayer_{steamid}_{date}.png"

    # Check if the file exists
    if os.path.exists(file_name):
        filepath = file_name
    else:
        piechart(steamid)

single_player_or_multi_player(76561199022018738)