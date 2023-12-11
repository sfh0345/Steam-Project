import requests
import random
import datetime
import csv
import os

api_key = 'B5A67039860C1613632C4795B6C36245'

def getrecommendedgames(steamid64):
    steam_id = steamid64
    # Function to get owned games for a given Steam ID
    def get_owned_games(api_key, steam_id):
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
        response = requests.get(url)
        games = response.json().get('response', {}).get('games', [])
        return games



    # Function to get friend list for a given Steam ID
    def get_friend_list(api_key, steam_id):
        url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
        response = requests.get(url)
        friend_list = response.json().get('friendslist', {}).get('friends', [])
        return [friend['steamid'] for friend in friend_list]

    def pick_and_get_game_names(api_key, game_set, number_of_games=20):
        def get_game_name(appid):
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            response = requests.get(url)
            data = response.json()
            if data[str(appid)]['success']:
                return data[str(appid)]['data']['name']
            else:
                return "Game name not found"

        game_list = list(game_set)
        if len(game_list) >= number_of_games:
            selected_games = random.sample(game_list, number_of_games)
        else:
            print("Not enough games to pick from. Returning all available games.")
            selected_games = game_list

        gameslist = []
        gamescount = 0
        for appid in selected_games:
            if gamescount <=4:
                game_name = get_game_name(appid)
                if game_name == "Game name not found" or len(game_name) > 20:
                    pass
                else:
                    gameslist.append(game_name)
                    gamescount = gamescount + 1
            else:
                return gameslist

    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")

    file_name = f"analytics/recommendedgame_{steam_id}_{date}.csv"
    csv_file = file_name

    selected_game_names = []  # Initialize the variable

    # Check if the file exists
    if os.path.exists(csv_file):
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            first_row = next(reader, None)

        # Print the first row
        if first_row:
            return first_row[0], first_row[1], first_row[2], first_row[3], first_row[4], first_row[5], first_row[6]
        else:
            print("Something went wrong. [nothing found in file]")
            return "er ging iets fout."


    else:
        # Get your own games
        my_games_data = get_owned_games(api_key, steam_id)
        owned_game_appids = {game['appid'] for game in my_games_data}

        # Get games owned by friends
        all_games = set()
        max_loops = 5
        friends = get_friend_list(api_key, steam_id)
        # for friend_id in friends:
        #     friend_games = get_owned_games(api_key, friend_id)
        #     all_games.update({game['appid'] for game in friend_games})
        for index in range(min(max_loops, len(friends))):
            friend_id = friends[index]
            friend_games = get_owned_games(api_key, friend_id)
            all_games.update({game['appid'] for game in friend_games})

        # Find games that your friends own but you don't
        friends_unique_games = all_games.difference(owned_game_appids)

        selected_game_names = pick_and_get_game_names(api_key, friends_unique_games)

        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")

        csv_file = f"analytics/recommendedgame_{steam_id}_{date}.csv"
        filepathname = csv_file

        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([selected_game_names[0], selected_game_names[1], selected_game_names[2], selected_game_names[3], selected_game_names[4], steam_id, date])

    return selected_game_names[0], selected_game_names[1], selected_game_names[2], selected_game_names[3], selected_game_names[4], steam_id, date



# steamid64 = "76561197960435530"
# print(getrecommendedgames(steamid64))
