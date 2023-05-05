import sqlite3
import random
from dotenv import load_dotenv
import os

load_dotenv()

games_database_url = os.getenv("GAMES_DATABASE_URL")
user_database_url = os.getenv("USER_DATABASE_URL")

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
