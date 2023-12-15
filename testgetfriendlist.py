def get_friend_usernames(steamid64):
    import requests
    # Get the friend list
    friend_list_url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=B5A67039860C1613632C4795B6C36245&steamid={steamid64}&relationship=all"

    response = requests.get(friend_list_url)

    if response.status_code == 200:
        friend_data = response.json()

        # Extracting steam IDs from the response
        friend_ids = [friend['steamid'] for friend in friend_data['friendslist']['friends']]

        # Get usernames, online status, and game information for all friends at once
        steamids_str = ','.join(map(str, friend_ids))
        player_summaries_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B5A67039860C1613632C4795B6C36245&steamids={steamids_str}"
        response = requests.get(player_summaries_url)

        if response.status_code == 200:
            player_data = response.json()

            friend_info = []

            for player in player_data['response']['players']:
                # Check if the friend is online
                status_code = player['personastate']
                if status_code != 0:  # Exclude offline friends
                    online_status = ""
                    if status_code == 1:
                        online_status = "Online"
                    elif status_code == 2:
                        online_status = "Busy"
                    elif status_code == 3:
                        online_status = "Away"
                    elif status_code == 4:
                        online_status = "Snooze"

                    # Check if the friend is in-game
                    if 'gameid' in player and player['gameid'] != "0":
                        game_name = player['gameextrainfo']
                        friend_info.append((player['personaname'], online_status, game_name))
                    else:
                        friend_info.append((player['personaname'], online_status, None))

            return friend_info
        else:
            print(f"Error 1: {response.status_code}")
    else:
        return 10
        print(f"Error 2: {response.status_code}")

# Replace with your API key and the Steam ID of the user
# var = get_friend_usernames("76561198343709779")
# print(var[0][0])
