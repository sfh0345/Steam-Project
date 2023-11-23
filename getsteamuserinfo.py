import requests

def get_player_summaries(steamid64):
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B5A67039860C1613632C4795B6C36245&steamids={steamid64}'
    response = requests.get(url)
    return response.json()

def getsteamuserinfo(steamid64):

    player_data = get_player_summaries(steamid64)

    if 'response' in player_data and 'players' in player_data['response']:
        players_info = player_data['response']['players']

        if players_info:  # Check if there are players in the list
            for player in players_info:
                name = player['personaname']
                avatarurl = player['avatarfull']
                status = player['personastate']
                return name, avatarurl, status

        else:
            return 1
    else:
        return 0

