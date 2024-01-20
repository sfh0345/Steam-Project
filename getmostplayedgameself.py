import requests
def getmostplayedgamemyself(steam_id64):
    def get_top_games(steam_id, api_key):
        owned_games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"

        # Make a request to get the list of owned games
        response = requests.get(owned_games_url)
        owned_games_data = response.json()

        # Check if the request was successful
        if response.status_code == 200 and owned_games_data.get("response", {}).get("games"):
            # Extract the list of game IDs from the response
            game_ids = [game["appid"] for game in owned_games_data["response"]["games"]]

            # Steam API endpoint for player's playtime in the last 2 weeks
            playtime_url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"

            # Make a request to get the recently played games
            response = requests.get(playtime_url)
            playtime_data = response.json()

            # Check if the request was successful
            if response.status_code == 200 and playtime_data.get("response", {}).get("games"):
                # Sort games by playtime in the last 2 weeks
                top_games = sorted(playtime_data["response"]["games"], key=lambda x: x.get("playtime_2weeks", 0), reverse=True)[:5]

                # Extract game details for the top games
                top_game_details = []
                for game in top_games:
                    game_id = game["appid"]
                    playtime_2weeks = game.get("playtime_2weeks", 0)

                    # Get game details using the Steam store API
                    game_details_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
                    game_details_response = requests.get(game_details_url)
                    game_details_data = game_details_response.json()

                    # Check if the request was successful
                    if game_details_response.status_code == 200 and game_details_data.get(str(game_id), {}).get("success"):
                        game_name = game_details_data[str(game_id)]["data"]["name"]
                        top_game_details.append({"game_id": game_id, "game_name": game_name, "playtime_2weeks": playtime_2weeks})

                return top_game_details
            else:
                # print("Error fetching recently played games.")
                pass
        else:
            # print("Error fetching owned games.")
            pass

    api_key = 'B5A67039860C1613632C4795B6C36245'

    top_games_result = get_top_games(steam_id64, api_key)

    lijst = []

    if top_games_result:
        for game in top_games_result:
            lijst.append([game['game_name'], game['playtime_2weeks']])
        return lijst
    else:
        # print("Failed to fetch top games.")
        return "Het ophalen van de favoriete game is niet gelukt."



# print(getmostplayedgamemyself(76561198220095232))