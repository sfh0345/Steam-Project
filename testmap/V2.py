import requests

# Function to get owned games for a given Steam ID
def get_owned_games(api_key, steam_id):
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
    response = requests.get(url)
    games = response.json().get('response', {}).get('games', [])
    return games

api_key = 'B5A67039860C1613632C4795B6C36245'
steam_id = '76561198075040510'

# Get your own games
my_games_data = get_owned_games(api_key, steam_id)
owned_game_appids = {game['appid'] for game in my_games_data}

# Function to get friend list for a given Steam ID
def get_friend_list(api_key, steam_id):
    url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
    response = requests.get(url)
    friend_list = response.json().get('friendslist', {}).get('friends', [])
    return [friend['steamid'] for friend in friend_list]

# Get games owned by friends
all_games = set()
friends = get_friend_list(api_key, steam_id)
for friend_id in friends:
    friend_games = get_owned_games(api_key, friend_id)
    all_games.update({game['appid'] for game in friend_games})

# Find games that your friends own but you don't
friends_unique_games = all_games.difference(owned_game_appids)

print("Games my friends own that I don't:", friends_unique_games)

import random
import requests

def pick_and_get_game_names(api_key, game_set, number_of_games=10):
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

    return {appid: get_game_name(appid) for appid in selected_games}

api_key = 'B5A67039860C1613632C4795B6C36245'
# Assume friends_unique_games is defined earlier in your code
selected_game_names = pick_and_get_game_names(api_key, friends_unique_games)
print("Randomly selected game names:", selected_game_names)
import tkinter as tk

def display_game_names(game_names):
    root = tk.Tk()
    root.title("Selected Game Names")

    # Create a listbox to display the game names
    listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    listbox.pack()

    # Insert each game name into the listbox
    for appid, name in game_names.items():
        listbox.insert(tk.END, f"Game Name: {name}")

    root.mainloop()

# Assuming selected_game_names is a dictionary with AppID as key and game name as value
display_game_names(selected_game_names)

