from api import app
from api.models import Movies, MovieSchema, User, RevokedTokenModel, WatchedMovies, \
    WatchedMoviesSchema, Showcase, ShowcaseSchema
from flask import request, jsonify, send_from_directory
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


@app.route('/v1/showcase', methods=['GET'])
@jwt_required
def get_all_showcase():
    showcase_schema = ShowcaseSchema(many=True)
    showcase = Showcase.query.all()
    return jsonify(showcase_schema.dump(showcase))


@app.route('/v1/showcase/<id>', methods=['POST'])
@jwt_required
def add_showcase_movie(id):
    new_showcase_movie = Showcase(movie_id=id)
    print(id)
    try:
        new_showcase_movie.save_to_db()
        return jsonify({'message': 'Movie {} added to showcase'.format(id)})
    except:
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/v1/showcase/<id>', methods=['DELETE'])
@jwt_required
def delete_showcase_movie(id):
    showcase_movie = Showcase(movie_id=id)
    try:
        showcase_movie.delete()
        return jsonify({'message': 'Movie {} deleted from showcase'.format(id)})
    except:
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/v1/poster/<path:filename>', methods=["GET"])
def cached_image_file(filename):
    return send_from_directory(app.config['POSTER_FOLDER'], filename=filename)


@app.route('/v1/movie/<id>', methods=['GET'])
@jwt_required
def get_movie(id):
    movie_schema = MovieSchema(many=True)
    movie = Movies.query.filter_by(id=id)
    return jsonify(movie_schema.dump(movie))


@app.route('/v1/movie/watched', methods=['GET'])
@jwt_required
def get_watched_movies():
    watched_movie_schema = WatchedMoviesSchema(many=True)
    watched_movies = WatchedMovies.query.filter_by(added_by=get_jwt_identity()).all()
    return jsonify(watched_movie_schema.dump(watched_movies))


@app.route('/v1/movie/watched/<id>', methods=['POST'])
@jwt_required
def add_watched_movie(id):
    new_watched_movie = WatchedMovies(movie_id=id, added_by=get_jwt_identity(),
                                      date=request.json['date'], user_rating=request.json['user_rating'])
    print(request.json)
    try:
        new_watched_movie.save_to_db()
        return jsonify({'message': 'Movie {} added to watched list'.format(id)})
    except:
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/v1/user/register', methods=['POST'])
def user_registration():
    if User.find_by_username(request.json['username']):
        return jsonify({'message': 'User {} already exists'.format(request.json['username'])}), 409

    new_user = User(username=request.json['username'], password=User.generate_hash(request.json['password']),
                    email=request.json['email'], name=request.json['name'])
    try:
        new_user.save_to_db()
        access_token = create_access_token(identity=request.json['username'])
        refresh_token = create_refresh_token(identity=request.json['username'])
        return jsonify({'message': 'User {} was created'.format(request.json['username']),
                        'access_token': access_token, 'refresh_token': refresh_token}), 201
    except:
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/v1/user/login', methods=['POST'])
def user_login():
    current_user = User.find_by_username(request.json['username'])
    if not current_user:
        return jsonify({'message': 'User {} doesn\'t exist'.format(request.json['username'])}), 404

    if User.verify_hash(request.json['password'], current_user.password):
        access_token = create_access_token(identity=request.json['username'])
        refresh_token = create_refresh_token(identity=request.json['username'])

        return jsonify({'logged_in_as': current_user.username, 'display_name': current_user.name,
                        'access_token': access_token, 'refresh_token': refresh_token}), 201
    else:
        return jsonify({'message': 'Wrong credentials'}), 401


@app.route('/v1/user/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def token_refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 201


@app.route('/v1/user/logout/access', methods=['POST'])
@jwt_required
def user_logout_access():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return jsonify({'message': 'Access token has been revoked'}), 201
    except:
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/v1/user/logout/refresh', methods=['POST'])
@jwt_refresh_token_required
def user_logout_refresh():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return jsonify({'message': 'Refresh token has been revoked'}), 201
    except:
        return jsonify({'message': 'Something went wrong'}), 500