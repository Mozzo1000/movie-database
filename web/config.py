import os


class Config(object):
    MOVIE_API_URL = os.environ.get('MD_MOVIE_API_URL')
    WEB_DISPLAY_NAME = os.environ.get('MD_WEB_DISPLAY_NAME')
    OMDB_API_KEY = os.environ.get('MD_OMDB_API_KEY')
