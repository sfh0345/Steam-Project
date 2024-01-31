import requests
import datetime
import csv
import os
from collections import Counter

api_key = 'B5A67039860C1613632C4795B6C36245'

def getrecommendedgames(steamid64):
    steam_id = steamid64

    def get_owned_games(api_key, steam_id):
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
        response = requests.get(url)
        games = response.json().get('response', {}).get('games', [])
        return games

    def get_friend_list(api_key, steam_id):
        url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
        response = requests.get(url)
        friend_list = response.json().get('friendslist', {}).get('friends', [])
        return [friend['steamid'] for friend in friend_list]

    def get_game_name(appid):
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = requests.get(url)
        data = response.json()
        if data[str(appid)]['success']:
            gamevar = data[str(appid)]['data']['name']
            return gamevar
        else:
            return "Game name not found"

    date = datetime.datetime.now().strftime("%d-%m-%Y")
    file_name = f"analytics/recommendedgame_{steam_id}_{date}.csv"
    csv_file = file_name

    selected_game_names = []

    if os.path.exists(csv_file):
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            first_row = next(reader, None)

        if first_row:
            return first_row[0], first_row[1], first_row[2], first_row[3], first_row[4], first_row[5], first_row[6]
        else:
            print("Something went wrong. [nothing found in file]")
            return "er ging iets fout."
    else:
        my_games_data = get_owned_games(api_key, steam_id)
        owned_game_appids = {game['appid'] for game in my_games_data}

        all_games = []
        max_loops = 100
        friends = get_friend_list(api_key, steam_id)

        for index in range(min(max_loops, len(friends))):
            friend_id = friends[index]
            friend_games = get_owned_games(api_key, friend_id)
            all_games.extend([game['appid'] for game in friend_games])

        friends_unique_games = set(all_games).difference(owned_game_appids)
        game_counts = Counter(all_games)

        # Sort games based on the count of friends playing each game
        sorted_games = sorted(friends_unique_games, key=lambda x: game_counts[x], reverse=True)

        selected_game_names = [get_game_name(appid) for appid in sorted_games[:5]]

        date = datetime.datetime.now().strftime("%d-%m-%Y")
        csv_file = f"analytics/recommendedgame_{steam_id}_{date}.csv"

        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(selected_game_names + [steam_id, date])

    return tuple(selected_game_names + [steam_id, date])

# steamid64 = "76561199022018738"
# print(getrecommendedgames(steamid64))
