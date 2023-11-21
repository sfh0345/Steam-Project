import requests

# Replace 'YOUR_API_KEY' with the actual API key you obtained from Steam

def get_player_summaries(steam_ids):
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B5A67039860C1613632C4795B6C36245&steamids={",".join(steam_ids)}'
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    # Replace 'STEAM_ID' with the actual Steam ID you want to retrieve information for
    steam_ids = ['76561199478010920']

    player_data = get_player_summaries(steam_ids)

    if 'response' in player_data and 'players' in player_data['response']:
        players_info = player_data['response']['players']

        if players_info:  # Check if there are players in the list
            for player in players_info:
                print(f"Steam ID: {player['steamid']}")
                print(f"Name: {player['personaname']}")
                print(f"Profile URL: {player['profileurl']}")
                print(f"Avatar: {player['avatarfull']}")
                print(f"Status: {player['personastate']}")
                print()
        else:
            print("No player found with the provided Steam ID.")
    else:
        print("Error fetching player data.")
