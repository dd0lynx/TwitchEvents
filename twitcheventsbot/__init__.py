from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from twitcheventsbot.discord.client import Discord

app = Flask(__name__)
app.secret_key = "b74071df4b0fe527ea96d213464469ee0ed1135490395b9d60af3680cfb45e1f"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap =Bootstrap5(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# "state": "expiration time"
oauth_states = {}

discord = Discord()

from twitcheventsbot.routes import *
from twitcheventsbot.users import User

