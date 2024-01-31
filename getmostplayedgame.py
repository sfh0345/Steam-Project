import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

def get_most_played(steamID):
    def get_username(steamid):
        profile_url = f"https://steamcommunity.com/profiles/{steamid}/?xml=1"
        response = requests.get(profile_url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            username = root.find("steamID").text
            return username
        else:
            print(f"Failed to retrieve username for {steamid}. Status Code: {response.status_code}")
            return None

    def get_friend_usernames(steamid64):
        # Get the friend list
        friend_list_url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=B5A67039860C1613632C4795B6C36245&steamid={steamid64}&relationship=all"

        response = requests.get(friend_list_url)

        if response.status_code == 200:
            friend_list = response.json().get("friendslist", {}).get("friends", [])

            # Get the username of each friend
            friend_dict = {}
            for friend in friend_list:
                friend["username"] = get_username(friend['steamid'])
                friend_dict[friend["username"]] = friend["steamid"]

            return friend_dict
        else:
            print(f"Failed to retrieve friend list. Status Code: {response.status_code}")
            return {}

    def most_played_games(steamid):
        # Retrieve the most played games of a user
        most_played_games_url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=B5A67039860C1613632C4795B6C36245&steamid={steamid}&format=json"
        response = requests.get(most_played_games_url)
        if response.status_code == 200:
            most_played_games = response.json().get("response", {}).get("games", [])
            # Sort the games based on playtime
            most_played_games.sort(key=lambda x: x.get("playtime_2weeks", 0), reverse=True)
            # Keep only the top 5 games
            most_played_games = most_played_games[:5]
            return most_played_games
        else:
            print(f"Failed to retrieve most played games. Status Code: {response.status_code}")
            return {}

    def compare_games_played(steamid):
        plt.rcParams['font.family'] = 'Motiva Sans'
        plt.rcParams['font.weight'] = '600'  # Use 'bold' for bold text

        # Get the friends of a user
        friends_list = get_friend_usernames(steamid)

        # Initialize aggregated_playtime dictionary
        aggregated_playtime = {}

        # Get the most played games of the friends and store them in a dictionary
        for friend in friends_list:
            friends_most_played_games = most_played_games(friends_list[friend])
            # Return only the username, playtime, and the name of the game
            for game in friends_most_played_games:
                keys_to_remove = [
                    "playtime_forever",
                    "img_icon_url",
                    "img_logo_url",
                    "has_community_visible_stats",
                    "playtime_windows_forever",
                    "playtime_mac_forever",
                    "playtime_linux_forever",
                ]
                for key in keys_to_remove:
                    game.pop(key, None)
                try:
                    # Use the initialized aggregated_playtime dictionary
                    if game["name"] in aggregated_playtime:
                        aggregated_playtime[game["name"]] += game["playtime_2weeks"]
                    else:
                        aggregated_playtime[game["name"]] = game["playtime_2weeks"]
                except KeyError:
                    print("Warning: 'name' key not found in game data:", game)
                    pass

        # Sort the games based on playtime
        aggregated_playtime = sorted(aggregated_playtime.items(), key=lambda x: x[1], reverse=True)
        # Return only the top 5 games
        aggregated_playtime = aggregated_playtime[:5]

        return aggregated_playtime

    def bar_chart_most_played_games(steamid):
        # Create a bar chart of the most played games of the friends
        games = compare_games_played(steamid)
        names = []
        playtime = []
        for game in games:
            names.append(game[0])
            # Convert playtime from minutes to hours
            playtime.append(game[1] / 60)

        # Create the bar chart
        plt.figure(figsize=(580 / 100, 900 / 100), facecolor='#0E131A')
        y_pos = np.arange(len(names))
        plt.bar(y_pos, playtime, align='center', alpha=0.9, color='#6AACF3')
        plt.xticks(y_pos, names, fontsize=10, rotation=45, ha="right", color='#FFFFFF')
        plt.ylabel('Hours played', fontsize=14, labelpad=10, color='#FFFFFF')
        plt.title('Most played games in the last 2 weeks by friends', fontsize=13, pad=17, color='#FFFFFF')
        plt.tight_layout()

        # Set the ticks to the correct color
        plt.tick_params(axis='y', colors='#FFFFFF')
        plt.tick_params(axis='x', colors='#FFFFFF')

        # Set the spines to the correct color (the edges of the graph)
        plt.gca().spines['bottom'].set_color('#FFFFFF')
        plt.gca().spines['top'].set_color('#FFFFFF')
        plt.gca().spines['left'].set_color('#FFFFFF')
        plt.gca().spines['right'].set_color('#FFFFFF')

        # Set the background of the graph to the correct color
        plt.gca().set_facecolor('#152330')

        # Add a grid behind the graph
        plt.grid(color='#FFFFFF', linestyle= '--', linewidth=0.5, axis='y')

        # Get the date
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")

        # Save the graph
        plt.savefig(f'analytics/mostplayed_{steamID}_{date}.png')


    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")

    file_name = f"analytics/mostplayed_{steamID}_{date}.png"

    # Check if the file exists
    if os.path.exists(file_name):
        filepath = file_name
    else:
        bar_chart_most_played_games(steamID)
