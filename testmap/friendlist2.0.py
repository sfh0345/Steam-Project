import requests


def get_friend_usernames(api_key, steam_id):
    # Get the friend list
    friend_list_url = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
    params = {
        'key': api_key,
        'steamid': steam_id,
        'relationship': 'all'
    }
    response = requests.get(friend_list_url, params=params)

    if response.status_code == 200:
        friend_data = response.json()

        # Extracting steam IDs from the response
        friend_ids = [friend['steamid'] for friend in friend_data['friendslist']['friends']]

        # Get usernames and online status for all friends at once
        steamids_str = ','.join(map(str, friend_ids))
        player_summaries_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamids_str}"
        response = requests.get(player_summaries_url)

        if response.status_code == 200:
            player_data = response.json()

            online_friends = []
            for player in player_data['response']['players']:
                # Check if the friend is online
                if player['personastate'] == 1 or player['personastate'] == 2 or player['personastate'] == 3 or player['personastate'] == 4:
                    online_friends.append(player['personaname'])

            if online_friends:
                print("Online Friends:")
                for friend in online_friends:
                    print(f"Friend: {friend}")
            else:
                print("No online friends.")

        else:
            print(f"Error: {response.status_code}")
    else:
        print(f"Error: {response.status_code}")


# Replace with your API key and the Steam ID of the user
api_key = "B5A67039860C1613632C4795B6C36245"
steam_id = "76561199022018738"

get_friend_usernames(api_key, steam_id)
