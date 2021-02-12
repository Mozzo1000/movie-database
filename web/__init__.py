from flask import Flask
from web.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "set-this-to-something-secret"

from web import routes
