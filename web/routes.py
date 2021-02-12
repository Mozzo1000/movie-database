from web import app
from flask import request, jsonify, abort, render_template, flash, redirect, url_for, session
import requests
from web.controllers import pwa


@app.route('/', methods=['GET', 'POST'])
def index():
    showcase = None
    if 'username' in session:
        if request.method == 'GET':
            access = 'Bearer {}'.format(session['access_token'])
            header = {'Accept': 'application/json', 'Content-Type': 'application/json',
                      'Authorization': access}
            showcase = requests.get(app.config['MOVIE_API_URL'] + 'v1/showcase', headers=header).json()

    return render_template('index.html', showcase_list=showcase)


@app.route('/watchlist/watched', methods=['GET', 'POST'])
def watchlist():
    if not 'username' in session:
        return redirect(url_for('login'))
    access = 'Bearer {}'.format(session['access_token'])
    header = {'Accept': 'application/json', 'Content-Type': 'application/json',
              'Authorization': access}

    if request.method == "POST":
        add_movie = requests.post(app.config['MOVIE_API_URL'] + 'v1/movie/watched/' + request.form['movie_id'], headers=header,
                                   json={"date": request.form['date'], "user_rating": request.form['rating']})

        if add_movie.status_code == 200:
            flash(add_movie.json()['message'])
            return redirect(url_for('watchlist'))

    return render_template('watchlist.html')


@app.route('/movie/<id>', methods=['GET', 'POST'])
def movie(id):
    if not 'username' in session:
        return redirect(url_for('login'))
    access = 'Bearer {}'.format(session['access_token'])
    header = {'Accept': 'application/json', 'Content-Type': 'application/json',
              'Authorization': access}
    movie = requests.get(app.config['MOVIE_API_URL'] + 'v1/movie/' + id, headers=header)

    if request.method == "POST":
        add_movie = requests.post(app.config['MOVIE_API_URL'] + 'v1/movie/watched/' + request.form['movie_id'], headers=header,
                                   json={"date": request.form['date'], "user_rating": request.form['rating']})

        if add_movie.status_code == 200:
            flash(add_movie.json()['message'])

    return render_template('movie.html', movie=movie.json()[0])


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not 'username' in session:
        return redirect(url_for('login'))
    query = request.args.get('q', None)
    return render_template('search.html', link=query)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/settings/showcase', methods=['GET', 'POST'])
def settings_showcase():
    if not 'username' in session:
        return redirect(url_for('login'))
    access = 'Bearer {}'.format(session['access_token'])
    header = {'Accept': 'application/json', 'Content-Type': 'application/json',
              'Authorization': access}
    showcase = requests.get(app.config['MOVIE_API_URL'] + 'v1/showcase', headers=header)

    if request.method == 'POST':
        add_showcase_movie = requests.post(app.config['MOVIE_API_URL'] + 'v1/showcase/' + request.form['movie_id'],
                                           headers=header)

        if add_showcase_movie.status_code == 200:
            flash(add_showcase_movie.json()['message'])

    return render_template('settings/settings_showcase.html', showcase_list=showcase.json())


@app.route('/settings', methods=['GET'])
def settings():
    if not 'username' in session:
        return redirect(url_for('login'))
    return render_template('settings/settings.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    header = {'Content-type': 'application/json'}
    if request.method == "POST":
        login_user = requests.post(app.config['MOVIE_API_URL'] + 'v1/user/login', headers=header,
                                   json={"username": request.form['username'], "password": request.form['password']})
        if login_user.status_code == 201:
            print(login_user.json())
            session['username'] = login_user.json()['logged_in_as']
            session['access_token'] = login_user.json()['access_token']
            session['refresh_token'] = login_user.json()['refresh_token']
            session['display_name'] = login_user.json()['display_name']
            return redirect(url_for('index'))

        else:
            print("Something went wrong")
            flash(login_user.json()['message'])

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    header = {'Content-type': 'application/json'}

    if request.method == "POST":
        print(request.form['username'])
        register_user = requests.post(app.config['MOVIE_API_URL'] + 'v1/user/register', headers=header,
                                      json={"username": request.form['username'], "password": request.form['password'],
                                            "email": request.form['email'], 'name': request.form['name']})
        print(register_user.status_code)
        if register_user.status_code == 201:
            print(register_user.json())
            flash(register_user.json()['message'])
            return redirect(url_for('register'))
        else:
            print(register_user.json())

    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user_access = requests.post(app.config['MOVIE_API_URL'] + 'v1/user/logout/access')
    logout_user_refresh = requests.post(app.config['MOVIE_API_URL'] + 'v1/user/logout/refresh')
    session.pop('username', None)
    session.pop('access_token', None)
    session.pop('refresh_token', None)
    return redirect(url_for('index'))


app.register_blueprint(pwa.blueprint)