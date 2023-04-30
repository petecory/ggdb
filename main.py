from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from func import *

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "23KDSJ2j2SJSJSI3u9skadjoawkdjahsdjkn2lkjn3kjjklhdiujh3mnk2l1"

conn = sqlite3.connect('user.db')
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

            conn = sqlite3.connect('games.db')
            c = conn.cursor()
            c.execute("UPDATE games SET game_title=?, site=?, game_key=?, redemed=?, claimed=?, notes=? WHERE id=?",
                      (game_title, site, game_key, redeemed, claimed, notes, id))
            conn.commit()
            conn.close()
            return redirect(url_for('games'))
        else:
            conn = sqlite3.connect('games.db')
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
