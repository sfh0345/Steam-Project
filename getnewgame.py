# import all necessary Modules and Libraries
import requests
import datetime
import csv
import os
from collections import Counter

api_key = 'B5A67039860C1613632C4795B6C36245'
# Function to get recommended games
def getrecommendedgames(steamid64):
    """
    This function returns 5 games that the user does not own but their friends does.
    It does that by utilizing Steam Web API to gather the owned games by the user and their friends.
    The recommendations are then stored in a CSV file.
    The function will return a tuple containing the recommended games, Steam ID of the user and the current date

    """
    steam_id = steamid64
    # Function to get the list of owned games by the steam user
    def get_owned_games(api_key, steam_id):
        """"
        The function get_owned_games retrieves the list of owned games by the Steam user
        while using Steam API
        """
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
        response = requests.get(url)
        games = response.json().get('response', {}).get('games', []) # Extract the games data from the response
        return games # Returns the list of owned games
    # Function that gives a list of friends of a Steam user
    def get_friend_list(api_key, steam_id):
        """
        This function makes a request using Steam API to retrieve the list containing the
        friends of that user.
        """
        url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
        response = requests.get(url)
        # Extract the friend list from the response
        friend_list = response.json().get('friendslist', {}).get('friends', [])
        # Returns a list of steamids from the steam user friends
        return [friend['steamid'] for friend in friend_list]

    # Function that gets the name from an appid
    def get_game_name(appid):
        """
        Get_game_name is a function that makes a request using Steam Store API.
        And returns the game name from the Appid.

        """
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = requests.get(url)
        data = response.json()
        # If the request is succesfull
        if data[str(appid)]['success']:
            # Extract and return the game name from the response data
            gamevar = data[str(appid)]['data']['name']
            return gamevar
        else:
            # If the game name was not found
            # Return with 'Game name not found'
            return "Game name not found"
    # Get the current date by using the module datetime
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    # Make a file name for storing analytics
    file_name = f"analytics/recommendedgame_{steam_id}_{date}.csv"
    # Change the name to csv_file
    csv_file = file_name

    # An empty list for storing recommended games
    selected_game_names = []
    # If the csv file exists
    if os.path.exists(csv_file):
        # Read the rows and return the data
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            first_row = next(reader, None)
        if first_row:
            return first_row[0], first_row[1], first_row[2], first_row[3], first_row[4], first_row[5], first_row[6]
        else:
            print("Something went wrong. [nothing found in file]")
            return "er ging iets fout."
    # If the file does not exist, continue with getting the game recommendation
    else:

        my_games_data = get_owned_games(api_key, steam_id)
        owned_game_appids = {game['appid'] for game in my_games_data}

        all_games = [] # An empty list that stores all game appids
        max_loops = 100 # A maximum of 100 loops for iterating through friends
        friends = get_friend_list(api_key, steam_id)
        # For loop a subset of friends up to max_loops
        for index in range(min(max_loops, len(friends))):
            # Get the steam ID of the friend
            friend_id = friends[index]
            # Get a list of games owned by that friend
            friend_games = get_owned_games(api_key, friend_id)
            # Extent the list of all games with the App Ids
            # of games owned by the current friend
            all_games.extend([game['appid'] for game in friend_games])
        # Find the games that the user does not own but their friends do own
        friends_unique_games = set(all_games).difference(owned_game_appids)
        game_counts = Counter(all_games)


        # Sort games based on the count of friends playing each game
        sorted_games = sorted(friends_unique_games, key=lambda x: game_counts[x], reverse=True)
        # Get names of the top 5 recommended games by using slicing
        selected_game_names = [get_game_name(appid) for appid in sorted_games[:5]]

        date = datetime.datetime.now().strftime("%d-%m-%Y")
        csv_file = f"analytics/recommendedgame_{steam_id}_{date}.csv"
        # Open the csv_file in writing mode
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write in the top row the selected game names, steam id and date
            writer.writerow(selected_game_names + [steam_id, date])
    # return a tuple that consists of the top 5 recommended games, steam_id and date
    return tuple(selected_game_names + [steam_id, date])

#steamid64 = "76561199022018738"
#print(getrecommendedgames(steamid64))
