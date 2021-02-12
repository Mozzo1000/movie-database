from api import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

"""
    TABLES IMPORTED FROM RACKFOCUS
"""


class Movies(db.Model):
    __tablename__ = 'title_basics'
    id = db.Column('tconst', db.String, primary_key=True)
    type = db.Column('titleType', db.String)
    title = db.Column('primaryTitle', db.String)
    originalTitle = db.Column(db.String)
    isAdult = db.Column(db.Integer)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer, nullable=True)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.String)
    rating = db.relationship("Rating", uselist=False, backref="title_basics")
    poster = db.relationship("MoviePoster", backref="title_basics")


class Rating(db.Model):
    __tablename__ = 'title_ratings'
    id = db.Column('tconst', db.String, db.ForeignKey('title_basics.tconst'), primary_key=True)
    average_rating = db.Column('averageRating', db.String)
    num_votes = db.Column('numVotes', db.Integer)


class MoviePoster(db.Model):
    id = db.Column(db.String, db.ForeignKey(
                         'title_basics.tconst'), primary_key=True)
    url = db.Column(db.String, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class PosterSchema(ma.SQLAlchemySchema):
    url = ma.String()


class RatingSchema(ma.SQLAlchemySchema):
    average_rating = ma.String()
    num_votes = ma.Integer()


class MovieSchema(ma.SQLAlchemySchema):
    id = ma.String(data_key='imdb_id')
    title = ma.String()
    type = ma.String()
    startYear = ma.Integer()
    runtimeMinutes = ma.Integer()
    genres = ma.String()
    rating = ma.Nested(RatingSchema)
    poster = ma.Nested(PosterSchema, many=True)


class WatchedMovies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String, db.ForeignKey(
                         'title_basics.tconst'), nullable=True)
    movie = db.relationship("Movies", backref="watched_movies")

    added_by = db.Column(db.String)
    date = db.Column(db.String)
    user_rating = db.Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class WatchedMoviesSchema(ma.SQLAlchemySchema):
    movie_id = ma.String()
    added_by = ma.String()
    movie = ma.Nested(MovieSchema)


class Showcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String, db.ForeignKey(
                         'title_basics.tconst'), nullable=True)
    movie = db.relationship("Movies", backref="showcase")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ShowcaseSchema(ma.SQLAlchemySchema):
    movie_id = ma.String()
    movie = ma.Nested(MovieSchema)

"""
    USER TABLES
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return check_password_hash(hash, password)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
