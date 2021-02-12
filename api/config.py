import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('MD_API_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'secret-key-change-this-later'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = False
    #JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    POSTER_FOLDER = os.environ.get('MD_POSTER_FOLDER')
