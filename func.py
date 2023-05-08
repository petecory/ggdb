import sqlite3
import random
from dotenv import load_dotenv
import os
import requests
import csv

load_dotenv('data/.env')

games_database_url = os.getenv("GAMES_DATABASE_URL")
user_database_url = os.getenv("USER_DATABASE_URL")
owner = os.getenv("OWNER")
rawg_key = os.getenv("RAWG_KEY")


def verify_user(username, password):
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


def authenticate_user(username, password, status):
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=? AND status=?", (username, password, status))
    result = c.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


def get_user(username):
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    row = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row:
        return {
            'username': row[1],
            'password': row[2],
            'status': row[3]
        }
    else:
        return None


def all_games():
    conn = sqlite3.connect(games_database_url)
    c = conn.cursor()

    # Execute a query to retrieve the games data
    c.execute("SELECT game_title, site, redemed, claimed, id FROM games")

    # Fetch all the rows of data
    rows = c.fetchall()
    conn.close()
    # Create a list of dictionaries from the rows of data
    games_data = []
    for row in rows:
        game = {
            'game_title': row[0],
            'site': row[1],
            'redemed': row[2],
            'claimed': row[3],
            'id': row[4],
        }
        games_data.append(game)
    return games_data


def gamebyid(id):
    conn = sqlite3.connect(games_database_url)
    c = conn.cursor()

    # Execute a query to retrieve the games data
    row = c.execute("SELECT * FROM games WHERE id = ?", (id,)).fetchone()
    conn.close()
    return row


def adduser():
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    status = input('Select the status: 1 - Pending, 2 - Member, 3 - Admin: ')
    if status in ['1', '2', '3']:
        if status == '1': status = 'pending'
        if status == '2': status = 'member'
        if status == '3': status = 'admin'

        c.execute("INSERT INTO users (username, password, status) VALUES (?, ?, ?)", (username, password, status))
        conn.commit()
        print("User added successfully!")
    else:
        print("Select a valid Status Option")


def get_user_by_id(user_id):
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    row = c.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return {'id': row[0], 'username': row[1], 'password': row[2], 'status': row[3]}
    else:
        return None


def update_user(username, password, status):
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    c.execute("UPDATE users SET username = ?, password = ?, status = ? WHERE username = ?", (username, password, status, username))
    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM users").fetchall()
    conn.close()
    users = []
    for row in rows:
        user = {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'status': row[3]
        }
        users.append(user)
    return users


def generate_password():
    alphabet = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet',
                'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango',
                'Uniform', 'Victor', 'Whiskey', 'Xray', 'Yankee', 'Zulu']

    first_letter = random.choice(alphabet)
    second_letter = random.choice(alphabet)
    digits = ''.join(random.choices('0123456789', k=3))

    return f"{first_letter}{digits}{second_letter}"


def add_user_to_db(username, password, status):
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, status) VALUES (?, ?, ?)", (username, password, status))
    conn.commit()
    conn.close()


def delete_user_db(username):
    if username != owner:
        conn = sqlite3.connect(user_database_url)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()


def add_game_to_db(game_title, site, game_key, redemed, claimed, notes):
    conn = sqlite3.connect(games_database_url)
    c = conn.cursor()
    if game_key == 'key':
        return
    # Check for duplicates
    c.execute("SELECT game_key FROM games WHERE game_key=?", (game_key,))
    result = c.fetchone()
    if result:
        return

    c.execute("INSERT INTO games (game_title, site, game_key, redemed, claimed, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (game_title, site, game_key, redemed, claimed, notes))
    conn.commit()
    conn.close()
    return


def update_password(username, current_password, new_password, confirm_password):
    conn = sqlite3.connect(user_database_url)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if not user:
        conn.close()
        return False, "User not found"
    elif user[2] != current_password:
        conn.close()
        return False, "Current password is incorrect"
    elif new_password != confirm_password:
        conn.close()
        return False, "New password and confirm password do not match"
    else:
        c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        conn.commit()
        conn.close()
        return True, "Password updated successfully"


def get_store_info(api_response):
    store_id_to_name = {
        1: "Steam",
        2: "Xbox Store",
        3: "PlayStation Store",
        4: "Apple App Store",
        5: "GOG",
        6: "Nintendo Store",
        7: "Xbox 360 Store",
        8: "Google Play",
        9: "itch.io",
        11: "Epic Games"
    }

    store_info = []
    for store in api_response['results'][0]:
        store_entry = {}
        if 'url' in store:
            store_entry['url'] = api_response['results'][0]['url']
            if api_response['results'][0]['store_id'] in store_id_to_name:
                store_entry['name'] = store_id_to_name[api_response['results'][0]['store_id']]


        if store_entry:
            store_info.append(store_entry)
    return store_info


def get_game_details_by_id(rawg_id):
    url = f"https://api.rawg.io/api/games/{rawg_id}?key={rawg_key}"
    response = requests.get(url)

    if response.status_code == 200:
        game_data = response.json()
        return game_data
    else:
        print(f"Error: Request to rawg.io API failed with status code {response.status_code}")
        return None


def get_game_stores(rawg_id):
    url = f"https://api.rawg.io/api/games/{rawg_id}/stores?key={rawg_key}"
    response = requests.get(url)
    if response.status_code == 200:
        store_data = response.json()
        return store_data
    else:
        print(f"Error: Request to rawg.io API failed with status code {response.status_code}")
        return None


def get_game_details(id):
    conn = sqlite3.connect(games_database_url)
    c = conn.cursor()
    game = c.execute("SELECT * FROM games WHERE id=?", (id,)).fetchone()
    conn.close()

    # Create a new dictionary for game details
    game_details = {
        'id': game[0],
        'game_title': game[1],
        'site': game[2],
        'redemed': game[4],
        'claimed': game[5],
        'notes': game[6]
    }

    # Prepare the rawg.io API endpoint
    rawg_api_endpoint = f"https://api.rawg.io/api/games?key={rawg_key}"
    search_query = game[1]  # game_title is in the second position in the list
    request_url = f"{rawg_api_endpoint}&search={search_query}&search_exact=True"
    # Make a request to the rawg.io API
    response = requests.get(request_url)
    if response.status_code == 200:
        base_data = response.json()
        if len(base_data['results']) > 0:
            rawg_id = base_data['results'][0]['id']
            api_game_details = get_game_details_by_id(rawg_id)
            api_game_store = get_game_stores(rawg_id)

            # Add additional game details to the game_details dictionary
            game_details['website'] = api_game_details['website']
            game_details['released'] = api_game_details['released']
            game_details['background_image'] = api_game_details['background_image']
            game_details['rawg_id'] = api_game_details['id']
            game_details['description'] = api_game_details['description']
            game_details['screenshot_urls'] = [screenshot['image'] for screenshot in base_data['results'][0]['short_screenshots']]
            game_details['stores'] = get_store_info(api_game_store)
    else:
        print(f"Error: Request to rawg.io API failed with status code {response.status_code}")

    return game_details
