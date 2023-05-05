from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from func import *
from dotenv import load_dotenv
import os
import shutil
import secrets


# Path to .env file
env_path = 'data/.env'
# Path to .env_template file
env_template_path = '.env_template'


# Check if .env file exists, if not, copy .env_template to .env
if not os.path.exists(env_path):
    shutil.copyfile(env_template_path, env_path)


# Load environment variables
load_dotenv('data/.env')


# Check the value of the SECRET_KEY variable and replace it with a new key if it is "changeme"
key_check = os.getenv('SECRET_KEY')
if key_check == 'changeme' or key_check == '':
    new_secret_key = secrets.token_hex(16)
    with open(env_path, 'r') as f:
        lines = f.readlines()
    with open(env_path, 'w') as f:
        for line in lines:
            if line.startswith('SECRET_KEY='):
                line = f'SECRET_KEY="{new_secret_key}"\n'
            f.write(line)
        os.environ["SECRET_KEY"] = new_secret_key


games_database_url = os.getenv("GAMES_DATABASE_URL")
user_database_url = os.getenv("USER_DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG")


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = secret_key


conn = sqlite3.connect(user_database_url)
c = conn.cursor()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            session['username'] = username  # store the username in the session
            user_info = get_user(username)
            session['status'] = user_info['status']

            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid username or password.")
    else:
        return render_template('login.html')


# Define a route for the dashboard page
@app.route('/dashboard')
def dashboard():
    if 'username' in session:  # check if the username is stored in the session
        return render_template('dashboard.html', username=session['username'], status=session['status'])
    else:
        return redirect('/')


@app.route('/gamedetail')
def gamedetail():
    if 'username' in session and session['status'] != 'pending':  # check if the username is stored in the session

        return render_template('gamedetail.html', username=session['username'], status=session['status'])
    elif session['status'] == 'pending':
        flash('Your status is pending, contact an Admin')
        return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/games')
def games():
    if 'username' in session and session['status'] != 'pending':  # check if the username is stored in the session
        username = session['username']
        # call DB function to get all games.
        games_data = all_games()
        # Render the games template with the games data
        return render_template('games.html', games=games_data, username=username, status=session['status'])
    elif session['status'] == 'pending':
        flash('Your status is pending, contact an Admin')
        return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if session['status'] == 'admin':
        game = gamebyid(id)
        if request.method == 'POST':
            game_title = request.form['game_title']
            site = request.form['site']
            game_key = request.form['game_key']
            redeemed = request.form.get('redeemed') == 'on'
            claimed = request.form['claimed']
            notes = request.form['notes']

            conn = sqlite3.connect(games_database_url)
            c = conn.cursor()
            c.execute("UPDATE games SET game_title=?, site=?, game_key=?, redemed=?, claimed=?, notes=? WHERE id=?",
                      (game_title, site, game_key, redeemed, claimed, notes, id))
            conn.commit()
            conn.close()
            return redirect(url_for('games'))
        else:
            conn = sqlite3.connect(games_database_url)
            c = conn.cursor()
            game = c.execute("SELECT * FROM games WHERE id=?", (id,)).fetchone()
            conn.close()

        return render_template('edit.html', id=id, games=game, status=session['status'])
    else:
        return redirect('/')


@app.route('/admin')
def admin():
    if 'username' in session and session['status'] == 'admin':
        users = get_all_users()
        return render_template('admin.html', users=users, status=session['status'])
    else:
        return redirect('/dashboard')


@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        status = request.form['status']
        add_user_to_db(username, password, status)
        flash('User added successfully', 'success')
        return redirect(url_for('admin'))
    else:
        return render_template('add-user.html')


@app.route('/admin/edit-user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    if 'username' in session and session['status'] == 'admin':
        user_info = get_user(username)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            status = request.form['status']
            update_user(username, password, status)
            flash('User updated successfully', 'success')
            return redirect(url_for('admin'))
        else:
            return render_template('edit-user.html', user=user_info, status=session['status'])
    else:
        return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
