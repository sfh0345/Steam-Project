import requests
from collections import Counter

def get_friends_online_hours(api_key, steam_id):
    def get_friend_list(api_key, steam_id):
        url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
        response = requests.get(url)
        friend_list = response.json().get('friendslist', {}).get('friends', [])
        return [friend['steamid'] for friend in friend_list]

    def get_player_summary(api_key, steam_id):
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
        response = requests.get(url)
        player_data = response.json().get('response', {}).get('players', [])
        return player_data[0].get('personastate', -1)

    friends = get_friend_list(api_key, steam_id)

    online_hours = []
    for friend_id in friends:
        online_status = get_player_summary(api_key, friend_id)

        games_response = None  # Initialize the variable outside the if block

        if online_status == 1:
            games_response = requests.get(f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={api_key}&steamid={friend_id}&format=json")

        if games_response and games_response.status_code == 200:
            games_data = games_response.json().get('response', {}).get('games', [])
            if games_data:
                playtime_2weeks = games_data[0].get('playtime_2weeks', 0)
                online_hours.append(playtime_2weeks)

    friend_count_per_hour = Counter(online_hours)

    online_hours_dict = {}
    for hour, count in friend_count_per_hour.items():
        hours, minutes = divmod(hour, 60)
        hours %= 24
        online_hours_dict[f"{hours:02d}"] = count

    return online_hours_dict

api_key = '36FBD6438CC015CDEBDEFA4FF12E1256'
steam_id = '76561198075040510'

resultaat = get_friends_online_hours(api_key, steam_id)
print(resultaat)
