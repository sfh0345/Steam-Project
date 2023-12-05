def get_friend_usernames(steamid64):
    import requests
    # Get the friend list
    friend_list_url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=B5A67039860C1613632C4795B6C36245&steamid={steamid64}&relationship=all"

    response = requests.get(friend_list_url)

    if response.status_code == 200:
        friend_data = response.json()

        # Extracting steam IDs from the response
        friend_ids = [friend['steamid'] for friend in friend_data['friendslist']['friends']]

        # Get usernames and online status for all friends at once
        steamids_str = ','.join(map(str, friend_ids))
        player_summaries_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B5A67039860C1613632C4795B6C36245&steamids={steamids_str}"
        response = requests.get(player_summaries_url)

        if response.status_code == 200:
            player_data = response.json()

            online_friends = []

            for player in player_data['response']['players']:
                # Check if the friend is online
                if player['personastate'] == 1 or player['personastate'] == 2 or player['personastate'] == 3 or player['personastate'] == 4:
                    online_friends.append(player['personaname'])

            friendsonline = []
            if online_friends:
                for i, friend in enumerate(online_friends[:8]):
                    friendsonline.append(friend)
                remaining_count = len(online_friends) - 8
                if remaining_count >= 0:
                    remaining = remaining_count
                else:
                    remaining = 0
                return friendsonline, remaining
            else:
                return 0
        else:
            print(f"Error 1: {response.status_code}")
    else:
        return 10
        print(f"Error 2: {response.status_code}")

# Replace with your API key and the Steam ID of the user

# get_friend_usernames("76561199022018738")
