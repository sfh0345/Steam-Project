import requests

def get_all_time_top_games(steam_id, api_key):
    # Steam API endpoint for player's playtime in all time
    playtime_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"

    # Make a request to get the list of owned games
    response = requests.get(playtime_url)
    playtime_data = response.json()

    # Check if the request was successful
    if response.status_code == 200 and playtime_data.get("response", {}).get("games"):
        # Sort games by playtime in all time
        top_games = sorted(playtime_data["response"]["games"], key=lambda x: x.get("playtime_forever", 0), reverse=True)[:5]

        # Extract game details for the top games
        top_game_details = []
        for game in top_games:
            game_id = game["appid"]
            playtime_forever = game.get("playtime_forever", 0)

            # Get game details using the Steam store API
            game_details_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
            game_details_response = requests.get(game_details_url)
            game_details_data = game_details_response.json()

            # Check if the request was successful
            if game_details_response.status_code == 200 and game_details_data.get(str(game_id), {}).get("success"):
                game_name = game_details_data[str(game_id)]["data"]["name"]
                top_game_details.append({"game_id": game_id, "game_name": game_name, "playtime_forever": playtime_forever})

        return top_game_details
    else:
        print("Error fetching owned games.")

steam_id64 = '76561198414336852'
api_key = 'B5A67039860C1613632C4795B6C36245'

all_time_top_games_result = get_all_time_top_games(steam_id64, api_key)

if all_time_top_games_result:
    print("All-time top 5 most played games:")
    for game in all_time_top_games_result:
        print(f"{game['game_name']} (App ID: {game['game_id']}) - Playtime: {int(game['playtime_forever'] / 60)} hours")
else:
    print("Failed to fetch all-time top games.")
