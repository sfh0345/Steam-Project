import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import datetime


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


def get_game_name(appid):
    # Haal de naam van een game op
    game_name_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(game_name_url)
    if response.status_code == 200:
        game_name = response.json().get(str(appid), {}).get("data", {}).get("name", "")
        return game_name
    else:
        print(f"Failed to retrieve game name. Status Code: {response.status_code}")
        return None


def most_played_games(steamid):
    # Haal de meest gespeelde games op van een user
    most_played_games_url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=B5A67039860C1613632C4795B6C36245&steamid={steamid}&format=json"
    response = requests.get(most_played_games_url)
    if response.status_code == 200:
        most_played_games = response.json().get("response", {}).get("games", [])
        # Sorteer de games op basis van playtime
        most_played_games.sort(key=lambda x: x.get("playtime_2weeks", 0), reverse=True)
        # hou alleen de top 5 games over
        most_played_games = most_played_games[:5]
        return most_played_games
    else:
        print(f"Failed to retrieve most played games. Status Code: {response.status_code}")
        return {}


def vergelijk_games_played(steamid):
    # haal de vrienden van een user op
    friends_list = get_friend_usernames(steamid)
    # haal de meest gespeelde games op van de vrienden en zet ze in een dictionary
    friends_most_played_games = {}
    for friend in friends_list:
        friends_most_played_games[friend] = most_played_games(friends_list[friend])
        # geef alleen de username, de playtime en de naam van de game terug
        for game in friends_most_played_games[friend]:
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
    # tel de playtime van de vrienden die dezelfde game spelen bij elkaar op
        # tel de playtime van de vrienden die dezelfde game spelen bij elkaar op
        aggregated_playtime = {}
        for friend in friends_most_played_games:
            for game in friends_most_played_games[friend]:
                # Check if the "name" key is present in the game dictionary
                game_name = game.get("name")
                if game_name is not None:
                    if game_name in aggregated_playtime:
                        aggregated_playtime[game_name] += game["playtime_2weeks"]
                    else:
                        aggregated_playtime[game_name] = game["playtime_2weeks"]

    # sorteer de games op basis van playtime
    aggregated_playtime = sorted(aggregated_playtime.items(), key=lambda x: x[1], reverse=True)
    # geef alleen de top 5 games terug
    aggregated_playtime = aggregated_playtime[:5]

    return aggregated_playtime

def barchart_most_played_games(steamid):
    # maak een barchart van de meest gespeelde games van de vrienden
    games = vergelijk_games_played(steamid)
    names = []
    playtime = []
    for game in games:
        names.append(game[0])
        # zet de playtime om van minuten naar uren
        playtime.append(game[1] / 60)

    # maak de barchart
    plt.figure(figsize=(580 / 100, 900 / 100), facecolor='#0E131A')
    y_pos = np.arange(len(names))
    plt.bar(y_pos, playtime, align='center', alpha=0.5, color='#6AACF3')
    plt.xticks(y_pos, names, rotation=45, ha="right", color='#FFFFFF')
    # zet de font naar motiva sans bold
    plt.ylabel('Playtime (Hours)', fontdict={'fontname': 'Arial', 'fontsize': 12},labelpad=10, color='#FFFFFF')

    plt.title('Most played games the last 2 weeks (By friends)', fontsize=14, pad=20, color='#FFFFFF')
    plt.tight_layout()

    # geef de ticks de juiste kleur
    plt.tick_params(axis='y', colors='#FFFFFF')
    plt.tick_params(axis='x', colors='#FFFFFF')

    # geef de spines de juiste kleur (de randen van de grafiek)
    plt.gca().spines['bottom'].set_color('#FFFFFF')
    plt.gca().spines['top'].set_color('#FFFFFF')
    plt.gca().spines['left'].set_color('#FFFFFF')
    plt.gca().spines['right'].set_color('#FFFFFF')

    # maak de achtergrond van de grafiek de juiste kleur
    plt.gca().set_facecolor('#152330')

    # maak een raster achter de grafiek
    plt.grid(color='#FFFFFF', linestyle= '--', linewidth=0.5, axis='y')

    # haal de datum op
    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")

    # sla de grafiek op
    plt.savefig(f'chart_most_played_games_{steamid}_{date}.png')

    # toon de grafiek (dit weghalen voor eind product)
    plt.show()

steamID = "76561197960435530"
barchart_most_played_games(steamID)

