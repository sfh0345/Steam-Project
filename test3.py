import requests
import matplotlib.pyplot as plt
from database_connection import connect_to_azure_postgresql

# Function to get owned app IDs from the Steam API
def get_owned_app_ids(steam_api_key, steam_id):
    # Construct the URL for the Steam API
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_id}&format=json'

    # Make a request to the Steam API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response and extract owned app IDs
        data = response.json()
        owned_appids = [game['appid'] for game in data['response']['games']]
        return owned_appids
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return None


# Function to check game mode from the PostgreSQL database
def check_game_mode(app_id, cursor):
    # Execute SQL queries to check for single-player and multi-player modes
    cursor.execute("SELECT appid, categories FROM gameproperties WHERE appid = %s AND categories LIKE %s",
                   (app_id, '%Single-player%'))
    result_single = cursor.fetchone()

    cursor.execute("SELECT appid, categories FROM gameproperties WHERE appid = %s AND categories LIKE %s",
                   (app_id, '%Multi-player%'))
    result_multi = cursor.fetchone()

    # Determine the game mode based on the SQL query results
    if result_single:
        return 'Single-player'
    elif result_multi:
        return 'Multi-player'
    else:
        return 'Mode not found'

# Set Steam API key and Steam ID
steam_api_key = '36FBD6438CC015CDEBDEFA4FF12E1256'
steam_id = '76561198066243767'

# Connect to the PostgreSQL database
conn = connect_to_azure_postgresql()
cursor = conn.cursor()

# Call the function to get owned app IDs from Steam API
owned_app_ids = get_owned_app_ids(steam_api_key, steam_id)

# Count the number of single-player and multi-player games
counts_dict = {'Single-player': 0, 'Multi-player': 0}
for app_id in owned_app_ids:
    mode = check_game_mode(app_id, cursor)
    if mode in counts_dict:
        counts_dict[mode] += 1

# Close the database connection
cursor.close()
conn.close()

# Calculate the percentage of single-player and multi-player games (excluding games with 'Mode not found')
valid_games_count = counts_dict['Single-player'] + counts_dict['Multi-player']
percentage_single = (counts_dict['Single-player'] / valid_games_count) * 100 if valid_games_count > 0 else 0
percentage_multi = (counts_dict['Multi-player'] / valid_games_count) * 100 if valid_games_count > 0 else 0


# Define a function to calculate the position plot
def position_plot(percentage_single, percentage_multi):
    if percentage_single > percentage_multi:
        return percentage_single - percentage_multi
    elif percentage_single < percentage_multi:
        return percentage_single - percentage_multi
    else:
        return 0

# Call the position_plot function
positie = position_plot(percentage_single, percentage_multi)
print(positie)

# Display the results
print("Counts:", counts_dict)
print(f"Percentage of Single-player games: {percentage_single:.2f}%")
print(f"Percentage of Multi-player games: {percentage_multi:.2f}%")

# Set the values for the left end, center, and right end
percentage_singleplayergames = -100
center = 0
percentage_multiplayergames = 100

# Plot the graph
plt.figure(figsize=(10, 2))
plt.hlines(y=0, xmin=percentage_singleplayergames, xmax=percentage_multiplayergames, color='gray')
plt.text(percentage_singleplayergames, 1, '100% Singleplayer Games', ha='center', va='bottom', color='black')  # Label for xmin
plt.text(percentage_multiplayergames, 1, '100% Multiplayer Games', ha='center', va='bottom', color='black')  # Label for xmax
plt.scatter(percentage_singleplayergames, 0, color='red', marker='o', label='100% Singleplayer Dot')
plt.scatter(center, 0, color='black', marker='o', label='Center')
plt.scatter(percentage_multiplayergames, 0, color='blue', marker='o', label='100% Multiplayer')
plt.scatter(positie, 0, color='green', marker='o', label='Positie')

plt.title('Spectrum singleplayer vs multiplayer')
plt.xlabel('Position')

plt.yticks([])
plt.legend()
plt.show()
